# Math Precision Agent

**Domain:** Arithmetic overflow/underflow, precision loss, rounding direction, decimal mismatch, type casting, off-by-one

Read `shared-rules.md` first. Then execute this analysis.

---

## Step 1 — Identify Solidity Version

```bash
grep -n "pragma solidity" --include="*.sol" -r .
```

- Pre-0.8.0: ALL arithmetic is unchecked — every add/sub/mul in token amounts is a potential overflow
- 0.8.0+: default is checked — focus on `unchecked` blocks only
- Mixed versions (imports pre-0.8 library into post-0.8 contract): be careful

---

## Step 2 — Unchecked Block Audit

```bash
grep -n -A 20 "unchecked {" --include="*.sol" -r .
```

For every `unchecked` block:
1. What is the stated safety assumption? (usually in comments)
2. Is that assumption actually enforced by the surrounding code?
3. Can user input affect the values inside the unchecked block?
4. If the assumption fails, what overflows/underflows?

Example red flag:
```solidity
unchecked {
    balances[user] -= amount; // ❌ if amount > balances[user], this wraps to uint256 max
}
```

---

## Step 3 — Division Before Multiplication

```bash
grep -n "/.*\*\|÷" --include="*.sol" -r .
```

Look for patterns like:
```solidity
uint result = (a / b) * c; // ❌ precision loss — divide first, then multiply
uint result = (a * c) / b; // ✅ correct order
```

This is Slither's `divide-before-multiply` detector — but verify every hit manually.

---

## Step 4 — Decimal Mismatch

Find all token interactions:
```bash
grep -n "decimals()\|DECIMALS\|1e18\|1e6\|1e8\|10\*\*" --include="*.sol" -r .
```

Check:
- If protocol handles tokens with different decimals (USDC=6, WETH=18, WBTC=8), is every arithmetic operation normalized?
- Chainlink prices come back with 8 decimals — is this accounted for in price calculations?
- Example: `price * amount` where `price` is 1e8 and `amount` is 1e18 → result is 1e26, not 1e18

---

## Step 5 — Rounding Direction

Find division operations in financial calculations:
```bash
grep -n "shares\|assets\|convertTo\|previewDeposit\|previewWithdraw\|previewMint\|previewRedeem" --include="*.sol" -r .
```

ERC-4626 and lending protocol standard:
- `convertToAssets` (rounding down) — favors protocol
- `convertToShares` (rounding up for deposits) — favors protocol
- Minting: round UP shares needed
- Burning: round DOWN assets returned

If rounding consistently favors users over protocol → accumulating dust drain vulnerability.

---

## Step 6 — Phantom Overflow

Look for intermediate values that may overflow before final division:
```solidity
// Vulnerable: a * b may overflow uint256 before / PRECISION
uint result = a * b / PRECISION;

// Safe alternative using mulDiv or 512-bit math:
uint result = FullMath.mulDiv(a, b, PRECISION);
```

Check: is `PRBMath.mulDiv` or `FullMath.mulDiv` (Uniswap v3) used where needed?

---

## Step 7 — Type Casting Audit

```bash
grep -n "uint128\|uint96\|uint64\|uint32\|uint16\|uint8\|int128\|int64\|SafeCast" --include="*.sol" -r .
```

For each downcast:
- Is the value guaranteed to fit? (e.g., storing a block.timestamp in uint32 will overflow in 2106)
- Is OpenZeppelin `SafeCast` used? If not, is the bound checked manually?
- Is `uint(-1)` or `type(uint128).max` used as a sentinel? Can it conflict with real values?

---

## Step 8 — Off-By-One Boundaries

Look at all loops, epoch boundaries, and deadline checks:
```bash
grep -n "for.*length\|while.*<\|block\.timestamp.*<=\|block\.timestamp.*<\|epoch\|period\|deadline" --include="*.sol" -r .
```

Check:
- `i < length` vs `i <= length` — is the last element processed or skipped?
- `block.timestamp >= deadline` vs `block.timestamp > deadline` — is the boundary transaction included?
- Epoch start/end: is the first or last block of an epoch credited correctly?

---

## Step 9 — Share Price Manipulation (First Depositor)

For ERC-4626 vaults or any share-based accounting:
```bash
grep -n "totalSupply\|totalAssets\|convertToShares\|convertToAssets\|_mint\|_burn" --include="*.sol" -r .
```

Check for the first-depositor inflation attack:
1. Attacker deposits 1 wei → mints 1 share
2. Attacker donates large amount directly (bypass deposit)
3. `totalAssets` now = large amount, `totalSupply` = 1
4. Next depositor's shares round to 0 (or very few), losing their deposit

Fix: virtual shares (add 1e3 to both numerator and denominator); or minimum initial deposit.

---

## Output Template

```
FINDING | contract: Vault | function: convertToShares | bug_class: share-inflation-attack | severity: HIGH
path: attacker → deposit(1) → direct transfer(1e18) → victim deposit(1e17) → 0 shares minted
proof: totalAssets=1+1e18, totalSupply=1; victim's 1e17 deposit → 1e17 * 1 / (1+1e18) = 0 shares; victim loses entire deposit
description: First-depositor share inflation attack — attacker inflates share price by direct token donation to zero-out small depositor shares
fix: Add virtual shares: shares = (assets * (totalSupply + 1e3)) / (totalAssets + 1e3)
```
