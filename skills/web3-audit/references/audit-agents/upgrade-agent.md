# Upgrade & Proxy Agent

**Domain:** Proxy patterns, initializer security, storage gaps, upgrade authorization, delegatecall misuse, implementation self-destruct

Read `shared-rules.md` first. Then execute this analysis.

---

## Step 1 — Detect Proxy Architecture

```bash
grep -rn "upgradeTo\|upgradeToAndCall\|_upgradeTo\|UUPSUpgradeable\|TransparentUpgradeableProxy\|ProxyAdmin\|Initializable\|BeaconProxy\|UpgradeableBeacon" --include="*.sol" .
grep -rn "Diamond\|IDiamondCut\|DiamondProxy\|FacetCut\|diamondCut" --include="*.sol" .
grep -rn "constructor.*_disableInitializers\|_disableInitializers" --include="*.sol" .
```

---

## Step 2 — Implementation Self-Destruct Risk

For every upgradeable implementation contract:

1. Does the constructor call `_disableInitializers()`?
2. If NOT: anyone can call `initialize()` on the bare implementation, become owner, then call `selfdestruct` or `upgradeTo(malicious)`
3. If implementation is destroyed: ALL proxy calls start reverting (bricked protocol)

```solidity
// ✅ Required in every implementation constructor
constructor() {
    _disableInitializers();
}
```

---

## Step 3 — Initializer Function Audit

```bash
grep -n "function initialize\|function __init\|initializer\|reinitializer" --include="*.sol" -r .
```

For each `initialize()` function:
1. **Has `initializer` modifier?** Missing = can be called again after deployment
2. **Sets all critical state?** Missing `owner`, `admin`, or critical config initialization
3. **Calls all parent `__X_init()` functions?** OZ pattern requires calling each parent initializer
4. **Emits initialization event?** Best practice for indexers

---

## Step 4 — UUPS Authorization Check

For UUPS proxies:
```bash
grep -n "_authorizeUpgrade\|upgradeTo\|upgradeToAndCall" --include="*.sol" -r .
```

Check:
- Is `_authorizeUpgrade()` overridden with an access control check?
- Missing override = anyone can call `upgradeTo(malicious)` → CRITICAL

```solidity
// ✅ Required override
function _authorizeUpgrade(address newImpl) internal override onlyOwner {}
```

---

## Step 5 — Storage Gap Completeness

For every upgradeable contract in the inheritance chain:
```bash
grep -n "contract.*Upgradeable\|contract.*Base\|contract.*Abstract" --include="*.sol" -r .
```

For each upgradeable base contract:
1. List all state variables → count slots used
2. Is there a `uint256[N] __gap` where `N + usedSlots = 50` (or another round number)?
3. If N is too small: adding state variables in a future version will overflow into the gap
4. If N is 0/missing: ANY future addition to base contract will corrupt derived contract storage

---

## Step 6 — Upgrade State Migration

When auditing a protocol ALREADY deployed with a previous version:
- Does the new implementation's storage layout exactly match the old one (slots 0..N)?
- Are new variables only added at the END?
- If the base contract added variables: did the gap get reduced accordingly?

Look for upgrade scripts:
```bash
find . -name "*.s.sol" -o -name "Upgrade*.ts" -o -name "deploy*.js" | head -20
```

---

## Step 7 — Proxy Admin Security

```bash
grep -n "ProxyAdmin\|changeAdmin\|getAdmin\|ifAdmin" --include="*.sol" -r .
```

For transparent proxy pattern:
- Is `ProxyAdmin` controlled by a multisig or timelock? Single EOA admin = HIGH risk
- Is admin separate from the contract's `owner`? (they should be)
- Can admin be changed without a timelock? (should require timelock)

---

## Step 8 — Diamond Facet Security

For Diamond pattern:
```bash
grep -n "diamondCut\|addFunctions\|removeFunctions\|replaceFunctions\|loupe" --include="*.sol" -r .
```

Check:
1. Is `diamondCut` protected by access control?
2. Are selector collisions checked before cut?
3. Does the diamond implement the loupe functions (EIP-2535 requires this)?
4. Can a facet be replaced with a malicious version by the admin without timelock?
5. Does each facet use its own namespaced storage struct (no direct slot writes)?

---

## Output Template

```
FINDING | contract: VaultImpl | function: constructor | bug_class: unprotected-implementation | severity: CRITICAL
path: attacker → VaultImpl.initialize(attacker) → VaultImpl.upgradeTo(Destroyer) → Destroyer.selfdestruct()
proof: VaultImpl constructor does not call _disableInitializers(); implementation deployed to 0xABC; attacker calls initialize(attacker) setting owner=attacker; upgrades to destructible contract; all proxies pointing to 0xABC now revert
description: Implementation contract not hardened against direct initialization — attacker can take ownership and destroy it, bricking all proxies
fix: Add _disableInitializers() to VaultImpl constructor; add onlyOwner to _authorizeUpgrade
```
