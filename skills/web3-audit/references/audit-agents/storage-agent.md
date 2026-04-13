# Storage Layout Agent

**Domain:** Proxy storage collisions, slot packing bugs, delegatecall storage context, storage gaps in upgradeable contracts

Read `shared-rules.md` first. Then execute this analysis.

---

## Step 1 — Detect Proxy Pattern

```bash
grep -rn "delegatecall\|Proxy\|UUPS\|TransparentUpgradeable\|upgradeable\|EIP1967\|Diamond\|IDiamondCut" --include="*.sol" .
```

Identify which proxy pattern is in use:
- **Transparent Proxy** (OZ): admin slot at `0xb5..`, implementation at `0x36..`
- **UUPS**: `upgradeTo()` in implementation, not proxy
- **Beacon**: implementation address from a beacon contract
- **Diamond (EIP-2535)**: multiple facets, `diamondStorage()` slot
- **Custom**: any `delegatecall` not matching above patterns

---

## Step 2 — EIP-1967 Slot Verification

For any proxy-based contract, verify standardized storage slots:
- Implementation: `0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc`
- Admin: `0xb53127684a568b3173ae13b9f8a6016e243e63b6e8ee1178d6a717850b5d6103`
- Beacon: `0xa3f0ad74e5423aebfd80d3ef4346578335a9a72aeaee59ff6cb3582b35133d50`

If a custom proxy uses different slots or stores anything at overlapping slots with the implementation → storage collision risk.

---

## Step 3 — Implementation Contract Storage Layout

Map the first 20 storage slots of every upgradeable implementation:
```solidity
// Slot 0: inherited variable 1
// Slot 1: inherited variable 2
// ...
```

Check:
- Does the current upgrade's storage layout match the previous version?
- Are new state variables ONLY added at the end?
- Does every base contract in the inheritance chain have a `uint256[N] __gap`?

---

## Step 4 — Storage Gap Audit

```bash
grep -n "__gap\|StorageGap\|uint256\[.*\] __gap" --include="*.sol" -r .
```

For each upgradeable base contract:
- Is there a `uint256[N] __gap` at the end of the state variables?
- Is the gap size correct? (total slots in base = state vars + gap should be a round number, e.g., 50)
- If a new state variable was added without reducing the gap → slots shifted → storage corruption

---

## Step 5 — delegatecall Misuse

```bash
grep -n "delegatecall" --include="*.sol" -r .
```

For every `delegatecall`:
1. Is the target address trusted and immutable? (user-supplied target = CRITICAL)
2. Does the called function modify `msg.sender`-related storage in a way that conflicts with the proxy's storage?
3. Is the return value checked?

---

## Step 6 — Diamond Storage Check

If Diamond pattern (EIP-2535):
```bash
grep -n "diamondStorage\|DiamondStorage\|LibDiamond\|IDiamondLoupe" --include="*.sol" -r .
```

Check:
- Does each facet use its own namespaced storage struct? (`bytes32 constant STORAGE_POSITION = keccak256("protocol.facet.storage")`)
- Are facets accessing global storage directly? (slot collision between facets)
- Does `diamondCut` have proper access control?
- Are selector collisions checked before adding facets?

---

## Step 7 — Packed Slot Security

```bash
grep -n "uint128\|uint96\|uint64\|uint32\|bool\|address.*uint" --include="*.sol" -r .
```

For tightly packed slots containing critical values:
- Can an operation on one field in the slot corrupt an adjacent field?
- Are packed booleans and addresses used in a way that creates unexpected aliasing?
- Are `bool` storage variables used as reentrancy guards? (ReentrancyGuard should use uint256, not bool)

---

## Step 8 — Mapping and Array Slot Collisions

For custom storage layouts:
- `keccak256(slot)` for mappings, `keccak256(slot) + index` for arrays
- Are any hardcoded storage slots colliding with OZ-standard proxy slots?
- Does any library use `assembly` to write to a hardcoded slot?

```bash
grep -n "sstore\|sload\|assembly" --include="*.sol" -r .
```

For every `sstore` / `sload` in assembly: verify the slot is not a standard EIP-1967 slot or another contract's slot.

---

## Output Template

```
FINDING | contract: VaultV2 | function: (storage layout) | bug_class: missing-storage-gap | severity: HIGH
path: VaultV2 inherits BaseVault → BaseVault adds new state variable in upgrade → all VaultV2 slots shift by 1
proof: BaseVault slot 0=owner, slot 1=paused (added in v2); VaultV2 expected owner at slot 0, totalAssets at slot 1 — now totalAssets reads paused value
description: BaseVault added a new state variable without a storage gap, shifting all derived contract storage slots and corrupting VaultV2 state
fix: Add `uint256[49] __gap` to BaseVault; state variables only appended to end of derived contracts
```
