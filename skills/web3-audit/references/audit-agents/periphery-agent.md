# Periphery Agent

**Domain:** External protocol integration, callback security, trust boundaries, ERC hook exploitation, third-party contract assumptions

Read `shared-rules.md` first. Then execute this analysis.

---

## Step 1 — Map External Dependencies

Find all imported interfaces and external calls:
```bash
grep -n "import.*interface\|import.*I[A-Z]\|IERC\|IUniswap\|IAave\|IChainlink\|ICompound\|ICurve\|ILido" --include="*.sol" -r .
grep -n "interface I" --include="*.sol" -r .
```

Build a trust map:
| External Contract | Trust Level | What it can do |
|------------------|-------------|----------------|
| Chainlink oracle | High | Return price data |
| Uniswap pool | Medium | Execute swaps, return reserves |
| User-supplied token | LOW | Malicious ERC-20/777 hooks |
| User-supplied address | ZERO | Arbitrary code execution |

---

## Step 2 — Callback Security

Find all callback entry points that external contracts can call INTO this protocol:
```bash
grep -n "onFlashLoan\|uniswapV3SwapCallback\|uniswapV2Call\|pancakeCall\|hook\|callback\|onERC" --include="*.sol" -r .
```

For each callback:
1. **Authentication:** Is the caller verified? (e.g., `require(msg.sender == pool)`)
2. **Initiator verification:** Is `initiator` checked? (flash loan callbacks)
3. **Reentrancy protection:** Is `nonReentrant` applied?
4. **State assumption:** Does the callback assume state that may have changed between initiation and callback?

---

## Step 3 — Flash Loan Callback Verification

```bash
grep -n "onFlashLoan\|executeOperation\|receiveFlashLoan" --include="*.sol" -r .
```

For each flash loan callback:
```solidity
// ✅ Safe pattern
function onFlashLoan(address initiator, ...) external {
    require(msg.sender == address(lender)); // verify caller is the pool
    require(initiator == address(this));    // verify we initiated the loan
    // ... do work
    return keccak256("ERC3156FlashBorrower.onFlashLoan"); // return magic value
}
```

Missing caller verification = anyone can call the callback and manipulate state.

---

## Step 4 — Uniswap v3 Callback Verification

```bash
grep -n "uniswapV3SwapCallback\|uniswapV3MintCallback\|uniswapV3FlashCallback" --include="*.sol" -r .
```

Must verify pool address via `PoolAddress.computeAddress(factory, poolKey)`. Without this:
- Attacker deploys fake Uniswap pool
- Calls `swap()` on fake pool
- Protocol's callback is called by attacker
- Callback sends tokens to "repay" without verifying the loan was legitimate

---

## Step 5 — ERC-20 Token Trust Boundaries

Find all token interactions:
```bash
grep -n "IERC20\|token\.transfer\|token\.transferFrom\|token\.approve\|SafeERC20\|safeTransfer" --include="*.sol" -r .
```

Check: does the protocol accept arbitrary user-supplied token addresses?

If yes, check for:
- **Fee-on-transfer:** Is balance delta measured? Or amount assumed?
- **Rebasing:** Is stored amount vs. current balance difference handled?
- **Reentrancy hooks:** ERC-777 `tokensReceived`, transfer callbacks
- **Return value:** `transfer()` returns bool — wrapped in `SafeERC20`?
- **Weird tokens:** tokens that revert on zero-amount transfers, tokens with blocklists (USDC), tokens that change decimals

---

## Step 6 — Cross-Protocol Integration Risk

For protocols integrated with lending (Aave, Compound), DEXs (Uniswap), or yield (Yearn):

```bash
grep -n "Aave\|Compound\|Uniswap\|Curve\|Convex\|Yearn\|Lido\|Pendle\|EigenLayer" --include="*.sol" -r .
```

Check:
- **Protocol upgrade compatibility:** If Aave/Compound upgrades, does this integration break?
- **Return value assumptions:** Does this protocol assume `deposit()` always succeeds?
- **Price assumptions:** Does this protocol use AMM price that the integrated protocol can manipulate?
- **Liquidity risk:** Does this protocol assume external liquidity is always available?

---

## Step 7 — Governance & Timelock Integration

```bash
grep -n "Governor\|Timelock\|propose\|execute\|queue" --include="*.sol" -r .
```

Check:
- Can a malicious governance proposal drain the protocol?
- Is there a guardian/veto role that can cancel malicious proposals?
- Is the timelock delay sufficient for users to exit if a malicious proposal passes?

---

## Step 8 — Cross-Chain Message Verification

If bridge or cross-chain messaging is present:
```bash
grep -n "LayerZero\|Wormhole\|CCIP\|Axelar\|lzReceive\|receiveMessage\|_anyExecute\|handle(" --include="*.sol" -r .
```

For each message receiver:
1. Is the source chain ID verified?
2. Is the source contract address (trusted remote) verified?
3. Is there replay protection (nonce)?
4. Is the message data sanitized before execution?

---

## Output Template

```
FINDING | contract: Router | function: uniswapV3SwapCallback | bug_class: missing-callback-auth | severity: CRITICAL
path: attacker → deploys FakePool → FakePool.swap() → Router.uniswapV3SwapCallback() → router sends tokens to FakePool
proof: callback lacks msg.sender == computedPool check; attacker's FakePool contract triggers callback; Router sends amountOwed in tokens to attacker
description: Missing Uniswap v3 callback authentication allows any contract to trigger the swap callback and steal tokens
fix: Verify msg.sender == PoolAddress.computeAddress(factory, PoolAddress.PoolKey(token0, token1, fee)) in the callback
```
