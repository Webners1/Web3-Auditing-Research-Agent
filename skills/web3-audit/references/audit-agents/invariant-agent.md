# Invariant Agent

**Domain:** Protocol-level invariants, conservation laws, accounting consistency, state coupling, balance tracking

Read `shared-rules.md` first. Then execute this analysis.

---

## What is an Invariant?

An invariant is a property that must ALWAYS hold — no matter what sequence of transactions occurs.

**Examples:**
- "Sum of all user balances == total supply"
- "Total borrowed <= total deposited"
- "Health factor of non-liquidated positions >= 1"
- "Reserve balance >= sum of user deposits"
- "LP tokens in circulation * price per share == total assets in vault"

Your job: identify invariants, then find code paths that break them.

---

## Step 1 — Identify Protocol Invariants

Read the contract logic and enumerate every conservation law:

```bash
# Find accounting state variables
grep -n "totalSupply\|totalDeposits\|totalBorrowed\|totalAssets\|totalShares\|totalReserves\|balances\[" --include="*.sol" -r .
```

For each aggregate variable, define its invariant relationship to other variables.

---

## Step 2 — Check Each State-Changing Function

For every function that changes any accounting variable:
1. Is the invariant maintained AFTER the function completes?
2. Is there a code path (revert, exception) where the function partially updates some accounting variables but not all?

**Partial update pattern (HIGH):**
```solidity
function transfer(address to, uint amount) external {
    balances[msg.sender] -= amount;
    require(someCheck()); // ❌ if this reverts, sender lost funds but receiver didn't get them
    balances[to] += amount;
}
```

---

## Step 3 — Accounting Drift

Find all places where the contract's token balance changes:
```bash
grep -n "transfer\|transferFrom\|safeTransfer\|receive()\|fallback()\|selfdestruct\|msg\.value" --include="*.sol" -r .
```

Check: does the protocol account for ALL ways its token balance can change?
- Direct transfers (bypassing deposit function)
- `selfdestruct` ETH injection
- Fee-on-transfer tokens reducing received amount
- Rebasing tokens changing balance spontaneously

---

## Step 4 — Vault Share Accounting

For ERC-4626 or any share-based vault:
```bash
grep -n "convertToShares\|convertToAssets\|totalAssets\|totalSupply\|deposit\|withdraw\|mint\|redeem" --include="*.sol" -r .
```

Verify:
- `totalAssets()` matches actual token balance (or defined deviation is tracked)
- After deposit: `shares_minted == convertToShares(assets_deposited)` (within rounding)
- After withdraw: `assets_returned == convertToAssets(shares_burned)` (within rounding)
- Invariant: `totalShares * pricePerShare == totalAssets` (approximately, within rounding)

---

## Step 5 — Lending Protocol Accounting

```bash
grep -n "borrow\|repay\|accrue\|interest\|healthFactor\|LTV\|collateral" --include="*.sol" -r .
```

Verify:
- `totalDebt` increases by exact borrow amount plus accrued interest
- `totalLiquidity` decreases by exact borrow amount
- After repay: debt decreases, liquidity increases by same amount
- Interest accrual: is it applied consistently? Can it be skipped?

---

## Step 6 — AMM Invariant

For AMM/DEX contracts:
```bash
grep -n "reserve0\|reserve1\|k =\|x \* y\|getReserves\|_update\|sync\|skim" --include="*.sol" -r .
```

Verify constant product invariant `k = x * y` (or equivalent):
- After swap: `(x + amountIn) * (y - amountOut) >= x * y` (fee consideration)
- After liquidity add: `k` increases proportionally
- After liquidity remove: `k` decreases proportionally
- `sync()` and `skim()` edge cases: can these be exploited to artificially inflate/deflate reserves?

---

## Step 7 — Token Supply Invariant

```bash
grep -n "mint\|burn\|_mint\|_burn\|totalSupply" --include="*.sol" -r .
```

Check:
- Can `totalSupply` go negative? (only matters pre-0.8.0)
- Can tokens be minted without proper accounting?
- Can tokens be burned that don't exist? (double-burn if no check)
- Do minting/burning events accurately reflect the balance change?

---

## Step 8 — Governance Token Invariants

For voting/governance:
```bash
grep -n "votes\|checkpoints\|delegate\|getPastVotes\|getPastTotalSupply" --include="*.sol" -r .
```

Check:
- Delegating multiple times: does voting power double-count?
- Flash minting: can someone mint tokens, vote, and burn in one transaction?
- `getPastVotes` at block N: is the snapshot mechanism tamper-proof?

---

## Output Template

```
FINDING | contract: LendingPool | function: borrow | bug_class: accounting-invariant-break | severity: HIGH
path: user → borrow(1000 USDC) → totalDebt += 1000 → but totalLiquidity not decremented if transfer fails
proof: if USDC.transfer() fails silently (returns false, not revert), totalDebt increases but user never receives funds and totalLiquidity stays unchanged; a subsequent borrow uses wrong liquidity
description: borrow() increments totalDebt before verifying token transfer success, breaking the invariant totalLiquidity + totalDebt == totalDeposits
fix: use SafeERC20 (reverts on failure) and update totalLiquidity only after confirmed transfer
```
