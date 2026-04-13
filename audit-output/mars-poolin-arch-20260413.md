# Architecture Advisory & Product Proposals — Mars Poolin

| Field | Value |
|-------|-------|
| Date | 2026-04-13 |
| Reviewer | Web3 Auditing Agent |
| Protocol | Mars Poolin (https://mars.poolin.fi/) |
| Stack | Ethereum, Solidity 0.5.17, Truffle, Uniswap V2 |
| MARS emission | Complete (ended Dec 2024) |

---

## Current Architecture — What Exists

```
[Poolin Mining Infra] ─── wBTC rewards ──► [Staking.sol]
                                                │
[User] ──► USDT ──► [TokenDistribute.sol] ──► pBTC35A ──► [Staking / LpStaking]
                                                │
                                          [BTCParamV2.sol] ◄── Uniswap V2 spot price
                                          (BTC difficulty, fee params)
```

**Trust model:** Almost everything controlled by two EOAs (owner + paramSetter). No timelock. No multisig. No audit.

---

## Gap Analysis

| Priority | Category | Gap | Impact |
|----------|----------|-----|--------|
| URGENT | Security | No audit, unaudited contracts handling real wBTC | Users exposed to undiscovered exploits |
| URGENT | Access Control | Owner + paramSetter are single EOAs | One compromised key = full protocol takeover |
| HIGH | Oracle | Uniswap V2 spot price for BTC reward calc | Flash loan manipulation of reward rates |
| HIGH | Upgradeability | Old ZeppelinOS proxy (v0.5.17), no upgrade path | Cannot patch bugs without migration |
| HIGH | Incentives | MARS emission complete, nothing replacing it | No reason for new liquidity to enter |
| MEDIUM | Transparency | No timelock on any parameter changes | Users cannot exit before adverse changes |
| MEDIUM | Composability | No ERC-4626 vault interface | Hard to integrate with current DeFi ecosystem |
| LOW | Chain strategy | Ethereum mainnet only, high gas for small rewards | Fee-sensitive users excluded |

---

## Detailed Recommendations

### URGENT — Replace EOA Control with Multisig + Timelock

**Current state:** `owner` and `paramSetter` are single Ethereum addresses.
**Industry standard:** Aave, Compound, Uniswap all use Gnosis Safe multisig + 48-hour TimelockController for protocol-critical parameters.

**Implementation steps:**
1. Deploy Gnosis Safe 3-of-5 multisig (team members as signers)
2. Deploy OpenZeppelin `TimelockController` with 48-hour minimum delay
3. Transfer `owner` on all contracts to the Timelock
4. Set `paramSetter` to the multisig (immediate actions) or Timelock (high-impact changes)

**Gains:** Eliminates single-key catastrophic risk. Gives users 48 hours to react to adverse changes.
**Costs:** All admin actions now require 2-day lead time + multisig coordination.

---

### URGENT — Get a Security Audit

**Current state:** Zero public audits.
**Industry standard:** Every protocol handling >$100K TVL has at least one public audit from a named firm.

**Recommended firms (in priority order):**
1. [Cyfrin](https://cyfrin.io) — competitive pricing, strong EVM focus
2. [Pashov Audit Group](https://pashov.net) — fast solo audits, DeFi specialized
3. [Code4rena](https://code4rena.com) — competitive audit, broad researcher pool

**Estimated scope:** ~600 LOC across 5 contracts — 1–2 week engagement.

---

### HIGH — Replace Oracle with Chainlink

**Current state:** `BTCParamV2.sol` uses Uniswap V2 `getReserves()` spot price.
**Industry standard:** Aave v3 uses Chainlink as primary, with TWAP fallback.

**Implementation:**
```solidity
// Replace this:
(uint112 reserve0, uint112 reserve1,) = IUniswapV2Pair(uniPairAddress).getReserves();
uint256 price = reserve1 * 1e18 / reserve0;

// With this:
AggregatorV3Interface feed = AggregatorV3Interface(0xF4030086522a5bEEa4988F8cA5B36dbC97BeE88); // BTC/USD
(, int256 answer,, uint256 updatedAt,) = feed.latestRoundData();
require(block.timestamp - updatedAt < 3600, "stale price");
require(answer > 0, "invalid price");
uint256 price = uint256(answer); // 8 decimals
```

**Gains:** Manipulation-resistant, industry-standard, maintained by Chainlink.
**Costs:** Chainlink feed has its own trust assumptions and can go offline. Add a fallback.

---

### HIGH — Rebuild Incentive Layer (MARS Emission is Over)

**Current state:** The 4-year MARS emission ended December 31, 2024. The protocol's primary liquidity incentive is gone.
**What this means:** Without MARS rewards, only wBTC yield remains. If that yield is competitive with simpler alternatives (e.g., just holding BTC), no rational user has a reason to prefer this protocol.

**Options to restore incentive competitiveness:**

**Option A — Launch MARS v2 with veTokenomics**
- Cap supply, introduce vote-escrow locking (veMars) like Curve/Convex model
- Gauge voting directs wBTC boosts to different pools
- Creates protocol-owned liquidity flywheel
- Effort: HIGH. Requires full token redesign + audit.

**Option B — Integrate EigenLayer for Restaking Yield**
- Allow stakers to restake their BTC yield position into EigenLayer AVS
- Earns additional ETH restaking yield on top of wBTC mining yield
- Effort: MEDIUM. Requires EigenLayer integration + security review.

**Option C — Expand Hashrate Token Coverage**
- Launch new tokens for other miners (Litecoin, Kaspa, newer ASICs)
- Each new token creates a new staking pool with fresh emission schedule
- Grows the protocol's TVL base organically
- Effort: MEDIUM. Requires new hardware partnerships.

**Recommendation:** Option A + C in parallel. veTokenomics makes existing liquidity sticky. New tokens bring new liquidity.

---

### MEDIUM — Upgrade to UUPS Proxy + Solidity 0.8.x

**Current state:** ZeppelinOS transparent proxy, Solidity 0.5.17.
**Industry standard:** OpenZeppelin UUPS (EIP-1967), Solidity 0.8.20+.

**Why this matters:** Cannot cleanly patch the oracle, timelock, or incentive issues without an upgrade path.

**Migration path:**
1. Deploy new UUPS implementations of all contracts in Solidity 0.8.x
2. Write a migration contract that reads state from old contracts and writes to new
3. Move all staked positions via user opt-in migration (never force-migrate)
4. Deprecate old contracts with a migration deadline

---

### MEDIUM — Add ERC-4626 Vault Interface

**Current state:** Staking contract has a custom interface, not compatible with any DeFi composability standard.
**Industry standard:** ERC-4626 is now the universal vault standard — adopted by Aave, Yearn, Morpho.

**Why it matters:** ERC-4626 compatibility means the staking vault can be automatically integrated by aggregators (Yearn, Beefy, DefiLlama yield tracker) without custom work.

**Implementation:** Wrap `Staking.sol` in an ERC-4626 adapter:
```solidity
contract MarsVault is ERC4626 {
    // Deposits → stakes pBTC35A
    // Withdraws → unstakes and returns pBTC35A + accrued wBTC
    // totalAssets() → returns staked balance + pending wBTC rewards
}
```

---

### LOW — Deploy on Arbitrum for Lower Fees

**Current state:** Ethereum mainnet only. Gas cost of claiming wBTC rewards can exceed the reward itself for small stakers.
**Recommendation:** Deploy the staking layer on Arbitrum One. Keep minting/governance on mainnet via a canonical bridge.

**Why Arbitrum:** Largest DeFi TVL outside mainnet. Deep Uniswap v3 and Chainlink oracle availability. OP Stack and Eigenlayer integrations possible.

---

## Technical Roadmap

### Phase 1 — Security (Week 1–2)
- [ ] Transfer owner to Gnosis Safe 3-of-5
- [ ] Deploy TimelockController (48-hour delay)
- [ ] Engage Cyfrin or Pashov for audit
- [ ] Replace Uniswap spot price with Chainlink BTC/USD

### Phase 2 — Upgradeability (Week 3–4)
- [ ] Redeploy all contracts in Solidity 0.8.x with UUPS proxy
- [ ] Storage layout audit before upgrade
- [ ] User migration path documented and tested

### Phase 3 — Incentives Relaunch (Week 5–8)
- [ ] Design MARS v2 tokenomics (veToken model)
- [ ] Audit new token + staking contracts
- [ ] Launch new hashrate token for at least one additional miner type

### Phase 4 — Ecosystem Expansion (Month 3–4)
- [ ] ERC-4626 vault wrapper → DefiLlama yield tracker integration
- [ ] Arbitrum deployment for lower-fee staking
- [ ] EigenLayer integration exploration

---

## Sources

- [MarsFi/POWToken GitHub](https://github.com/MarsFi/POWToken)
- [OpenZeppelin UUPS Guide](https://docs.openzeppelin.com/contracts/5.x/api/proxy#UUPSUpgradeable)
- [Chainlink BTC/USD Feed](https://docs.chain.link/data-feeds/price-feeds/addresses)
- [ERC-4626 Standard](https://eips.ethereum.org/EIPS/eip-4626)
- [Curve veTokenomics](https://curve.readthedocs.io/dao-vecrv.html)
- [EigenLayer Docs](https://docs.eigenlayer.xyz)
- [L2BEAT Arbitrum](https://l2beat.com/scaling/projects/arbitrum)
