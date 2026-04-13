# Reentrancy Agent

**Domain:** All reentrancy variants — ETH, ERC-20 hooks, cross-function, cross-contract, read-only

Read `shared-rules.md` first. Then execute this analysis.

---

## Step 1 — Find All External Calls

Search for every external interaction:
```bash
grep -n "\.call\b\|\.transfer\b\|\.send\b\|\.delegatecall\b\|\.staticcall\b" --include="*.sol" -r .
grep -n "IERC20\|ERC20\|token\.\|\.transfer\|\.transferFrom\|\.safeTransfer" --include="*.sol" -r .
grep -n "onERC721Received\|onERC1155Received\|tokensReceived\|safeTransfer" --include="*.sol" -r .
```

For each external call found, map: which function contains it, what state variables are read/written before and after.

---

## Step 2 — CEI Order Check

For every external call, verify the **Checks-Effects-Interactions** pattern:

✅ Correct order:
1. Checks (require, validate)
2. Effects (state updates: balances[user] = 0, shares[user] -= amount)
3. Interactions (external call: .call, token.transfer)

❌ Wrong order (flag immediately):
- State update AFTER the external call
- Balance decrement AFTER `.call{value}()`
- Shares burned AFTER `token.transfer()`

---

## Step 3 — `nonReentrant` Audit

Find all `nonReentrant` modifiers:
```bash
grep -n "nonReentrant\|ReentrancyGuard" --include="*.sol" -r .
```

Check:
- Are ALL entry points that touch sensitive state protected?
- If function A has `nonReentrant` but function B does not, and B can be called during A's external call → cross-function reentrancy
- OpenZeppelin's `ReentrancyGuard` blocks within the same call context but NOT cross-contract calls to a different contract that calls back

---

## Step 4 — ERC-721/1155 Hook Check

Find all NFT safe transfers:
```bash
grep -n "safeTransferFrom\|safeMint\|_safeMint" --include="*.sol" -r .
```

For each: does the recipient's `onERC721Received` / `onERC1155Received` get called before state finalization? If yes, flag as reentrancy risk.

---

## Step 5 — ERC-777 / Callback Token Check

Find token transfers:
```bash
grep -n "tokensReceived\|ERC777\|IERC777" --include="*.sol" -r .
```

If protocol handles ERC-777 tokens (or does not explicitly reject them), ALL token transfers create reentrancy vectors — flag as HIGH.

---

## Step 6 — Read-Only Reentrancy

Identify any `view` or `pure` functions that read shared state:
- If another protocol could read these during a state-transitional call, the stale view creates a read-only reentrancy vector
- Particularly relevant for: LP token price calculations, vault share prices, health factor reads

Check: is this protocol integrated by others? Does it expose price or balance views that could be exploited?

---

## Step 7 — Cross-Contract Reentrancy

Map the full call graph:
- If protocol A calls protocol B, and protocol B has a callback that calls back into protocol A via a DIFFERENT function than the one with `nonReentrant`
- This bypasses the reentrancy guard entirely

Trace: does any external call in this codebase lead back to this codebase via a path not protected by `nonReentrant`?

---

## Output

For every confirmed or suspected reentrancy:

```
FINDING | contract: LendingPool | function: repay | bug_class: reentrancy-erc20 | severity: HIGH
path: user → repay(tokenAddr, amount) → token.transfer(user, amount) → tokensReceived() → repay() again
proof: if tokenAddr is ERC-777, tokensReceived fires before collateral is updated; second repay sees old collateral value and double-removes
description: ERC-777 reentrancy in repay() allows borrower to replay repayment, inflating their collateral position
fix: update collateralBalance[user] before calling token.transfer(); add nonReentrant to repay()
```
