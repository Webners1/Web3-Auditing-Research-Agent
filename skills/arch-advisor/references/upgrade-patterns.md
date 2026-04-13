# Upgrade Patterns Reference

Decision guide for choosing and implementing contract upgradeability.

---

## Pattern Comparison

| Pattern | Best For | Gas Cost | Complexity | Used By |
|---------|---------|---------|-----------|---------|
| UUPS (EIP-1967) | Most protocols | Low | Medium | Aave v3, OpenSea |
| Transparent Proxy | Simpler admin separation | Medium | Low | Compound v2 |
| Beacon Proxy | Many clone instances | Low per-instance | High | Uniswap v3 pools |
| Diamond (EIP-2535) | >24KB contracts, modular | Medium | Very High | Aavegotchi, SushiSwap |
| Minimal Proxy (EIP-1167) | Gas-efficient cloning | Very Low | Low | Gnosis Safe, Uniswap v2 pairs |
| Immutable | No upgrade needed | Zero | Zero | Uniswap v2 core |

---

## UUPS — Universal Upgradeable Proxy Standard (Recommended)

**EIP-1967 storage slots. Upgrade logic lives in the implementation.**

### When to use
- New protocol that expects to iterate
- Single main contract (not dozens of instances)
- Want smallest possible proxy overhead

### Storage Layout (EIP-1967)
```solidity
// Implementation slot: keccak256('eip1967.proxy.implementation') - 1
bytes32 internal constant _IMPLEMENTATION_SLOT = 
    0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc;

// Admin slot (for admin proxies only): keccak256('eip1967.proxy.admin') - 1
bytes32 internal constant _ADMIN_SLOT = 
    0xb53127684a568b3173ae13b9f8a6016e243e63b6e8ee1178d6a717850b5d6103;
```

### Implementation Template
```solidity
import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";
import "@openzeppelin/contracts-upgradeable/proxy/utils/UUPSUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/access/OwnableUpgradeable.sol";

contract ProtocolV1 is Initializable, UUPSUpgradeable, OwnableUpgradeable {
    // ⚠️ Never use constructor for initial state — use initialize()
    /// @custom:oz-upgrades-unsafe-allow constructor
    constructor() {
        _disableInitializers(); // ← CRITICAL: prevents initializing bare implementation
    }

    function initialize(address admin) public initializer {
        __Ownable_init(admin);
        __UUPSUpgradeable_init();
        // ... other initializations
    }

    // ← MUST override — this is what prevents unauthorized upgrades
    function _authorizeUpgrade(address newImpl) internal override onlyOwner {}

    uint256[50] private __gap; // ← storage gap for future base contract additions
}
```

### Upgrade Script (Foundry)
```solidity
import "@openzeppelin/foundry-upgrades/Upgrades.sol";

// Deploy
address proxy = Upgrades.deployUUPSProxy(
    "ProtocolV1.sol",
    abi.encodeCall(ProtocolV1.initialize, (adminAddr))
);

// Upgrade to V2
Upgrades.upgradeProxy(proxy, "ProtocolV2.sol", "");
```

### Security Checklist
- [ ] `_disableInitializers()` in every implementation constructor
- [ ] `_authorizeUpgrade()` overridden with access control
- [ ] Storage layout validated before upgrade (use OZ Upgrades plugin)
- [ ] `__gap` in every base upgradeable contract
- [ ] Upgrade goes through timelock (not immediate)

---

## Transparent Proxy

**Admin calls go to proxy itself; all other calls delegated to implementation.**

### When to use
- Need clear separation between proxy admin and contract owner
- Simpler mental model for team
- Migrating from older codebase that uses this pattern

### Key Difference from UUPS
```
UUPS: upgrade logic in implementation → if implementation is bricked, can't upgrade
Transparent: upgrade logic in proxy → proxy always works even if implementation is broken
```

### Implementation
```solidity
// Deploy with OZ (recommended — don't write custom transparent proxies)
import "@openzeppelin/contracts/proxy/transparent/TransparentUpgradeableProxy.sol";
import "@openzeppelin/contracts/proxy/transparent/ProxyAdmin.sol";

// ProxyAdmin should be owned by a multisig or timelock
ProxyAdmin admin = new ProxyAdmin(timelockAddr);
TransparentUpgradeableProxy proxy = new TransparentUpgradeableProxy(
    address(implementation),
    address(admin),
    abi.encodeCall(Implementation.initialize, (params))
);
```

### Security Note
- `ProxyAdmin` owner MUST be a multisig (Gnosis Safe) or timelock — single EOA = single point of failure

---

## Beacon Proxy

**Many proxy instances all point to one "beacon" contract that holds the implementation address.**

### When to use
- Deploying many identical contracts (pools, vaults, positions)
- Need to upgrade all instances atomically with a single transaction
- Example: Uniswap v3 pools — upgrade all 10,000+ pools by updating one beacon

### Architecture
```
Beacon (holds implementation address)
  ↑ reads
BeaconProxy1 → Implementation
BeaconProxy2 → Implementation  (all updated atomically when beacon changes)
BeaconProxy3 → Implementation
```

### Implementation
```solidity
import "@openzeppelin/contracts/proxy/beacon/UpgradeableBeacon.sol";
import "@openzeppelin/contracts/proxy/beacon/BeaconProxy.sol";

// Deploy beacon (owned by multisig/timelock)
UpgradeableBeacon beacon = new UpgradeableBeacon(address(implementation), timelockAddr);

// Deploy instances
BeaconProxy pool1 = new BeaconProxy(
    address(beacon),
    abi.encodeCall(Pool.initialize, (token0, token1, fee))
);
```

---

## Diamond (EIP-2535)

**Single proxy with multiple "facets" (implementation contracts), each providing a set of functions.**

### When to use
- Contract exceeds 24KB bytecode limit
- Need to upgrade individual features independently
- Large protocol with many orthogonal modules (e.g., separate facets for lending, liquidation, oracle)

### When NOT to use
- Small/simple protocols — complexity is rarely worth it
- Team without EIP-2535 experience — high implementation risk

### Key Concepts
```solidity
// Each facet uses namespaced storage (avoid slot collisions)
library LibVaultStorage {
    bytes32 constant STORAGE_POSITION = keccak256("protocol.vault.storage");
    
    struct Storage {
        mapping(address => uint256) balances;
        uint256 totalAssets;
    }
    
    function getStorage() internal pure returns (Storage storage s) {
        bytes32 position = STORAGE_POSITION;
        assembly { s.slot := position }
    }
}
```

### Reference Implementation
- [Nick Mudge's Diamond-3 Hardhat](https://github.com/mudgen/diamond-3-hardhat)
- [Diamond Foundry template](https://github.com/FredCoen/diamond_foundry)

---

## Minimal Proxy (EIP-1167) — Clone Factory

**Ultra-cheap deployment: 45-byte proxy that clones a reference implementation.**

### When to use
- Deploying many instances where gas cost of deployment matters
- Instances DON'T need independent upgradeability (all instances share the same implementation)
- Safe accounts, Uniswap v2 pairs, Gnosis Safe modules

### Implementation
```solidity
import "@openzeppelin/contracts/proxy/Clones.sol";

contract VaultFactory {
    address public immutable implementation;
    
    constructor(address _impl) {
        implementation = _impl;
    }
    
    function deployVault(address owner) external returns (address vault) {
        vault = Clones.clone(implementation);
        IVault(vault).initialize(owner);
    }
}
```

### Gas Comparison
| Method | Deployment Cost |
|--------|----------------|
| `new Contract()` | ~800,000 gas |
| Minimal Proxy | ~45,000 gas |
| Beacon Proxy | ~250,000 gas |

---

## Immutable Contracts

### When to use
- Maximally trustless protocol (Uniswap v2 core, Chainlink price feeds)
- Simple, well-audited contracts with no expected changes
- Protocol values trustlessness over upgradeability

### Trade-offs
- **Pro:** Highest trust guarantee; users know the rules can't change
- **Con:** Cannot fix bugs; must migrate to new contracts (expensive, risky)

### Recommendation
Use immutable + factory pattern: deploy immutable core, add optional upgradeable periphery (router, fee controller).

---

## Migration Strategy: Immutable → Upgradeable

If the current protocol is immutable and needs upgradeability:

1. Deploy new UUPS implementation
2. Deploy migration contract: reads state from old contract, writes to new
3. Move liquidity in batches (if applicable)
4. Point frontend to new contract
5. Keep old contract alive indefinitely (for legacy integrators)
6. Never `selfdestruct` old contract

Example migration pattern: Compound v2 → v3, Uniswap v2 → v3.
