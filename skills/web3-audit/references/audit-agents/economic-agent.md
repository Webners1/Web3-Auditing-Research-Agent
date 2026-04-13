# Economic Security Agent

**Domain:** Flash loan attacks, oracle manipulation, MEV/sandwich, price impact, liquidation mechanics, incentive alignment

Read `shared-rules.md` first. Then execute this analysis.

---

## Step 1 — Identify Economic Attack Surface

Find all value-sensitive operations:
```bash
grep -n "swap\|liquidate\|borrow\|repay\|flashLoan\|flashSwap\|arbitrage\|price\|rate\|fee\|reward\|mint\|redeem" --include="*.sol" -r .
```

Map: which operations are profitable to attack? What would an adversary extract?

---

## Step 2 — Oracle Dependency Audit

Find all price oracle reads:
```bash
grep -n "latestRoundData\|latestAnswer\|getPrice\|getReserves\|slot0\|observe\|TWAP\|twap\|oracle" --include="*.sol" -r .
```

For each oracle call check:
1. **Spot price?** `getReserves()` from Uniswap v2 = instantly manipulable → HIGH
2. **Staleness check?** `require(block.timestamp - updatedAt < threshold)` missing → MEDIUM
3. **Answer > 0 check?** `require(answer > 0)` missing → MEDIUM
4. **Single oracle?** No fallback if oracle is down → MEDIUM
5. **Round completeness?** `require(answeredInRound >= roundId)` missing → LOW

---

## Step 3 — Flash Loan Attack Vectors

Flash loans can manipulate any value that changes within a transaction. For each spot oracle or AMM-based price:

Can an attacker:
1. Flash borrow large amount
2. Manipulate the price/rate/ratio
3. Execute a profitable action against this protocol
4. Repay the flash loan

Protocols most vulnerable:
- Lending protocols with AMM-based collateral pricing
- Protocols with `getReserves()`-based pricing
- Governance protocols with ERC-20-based voting power

---

## Step 4 — Liquidation Mechanism

```bash
grep -n "liquidat\|healthFactor\|collateralFactor\|LTV\|undercollateral" --include="*.sol" -r .
```

Check:
- **Liquidation incentive too high?** Liquidators extract more than needed → bad debt for protocol
- **Liquidation incentive too low?** No one liquidates → protocol accumulates bad debt silently
- **Flash loan liquidation?** Can attacker liquidate by first manipulating price downward?
- **Full vs partial liquidation?** Full liquidation on large positions creates MEV opportunity and bad UX
- **Cascading liquidations?** Can one liquidation trigger another in the same protocol?

---

## Step 5 — MEV & Front-Running

Identify transactions that are profitable to front-run:
```bash
grep -n "amountOutMin\|minAmountOut\|slippage\|deadline\|minOut\|minReturn" --include="*.sol" -r .
```

Check:
- Does every swap have a `minAmountOut` parameter AND is it checked?
- Does every swap have a deadline parameter?
- Are `approve` + `transferFrom` in separate transactions? (classic front-run)
- Can price-sensitive transactions be delayed by block stuffing?

---

## Step 6 — Reward/Incentive Manipulation

```bash
grep -n "reward\|emission\|distribute\|claimReward\|stake\|unstake\|epoch\|accRewardPerShare" --include="*.sol" -r .
```

Check:
- **Just-in-time liquidity:** Can attacker stake just before reward snapshot and unstake immediately after?
- **Reward calculation overflow:** Does `accRewardPerShare * userShares` overflow?
- **Reward front-running:** Is there a block between reward announcement and distribution?
- **Pool weight manipulation:** Can attacker inflate their pool weight before snapshot?

---

## Step 7 — Token Economic Design

- **Inflationary mint:** Is there a cap on total supply? Can infinite tokens be minted?
- **Fee accumulation:** Do fees accumulate in the contract without withdrawal path? → DoS via gas griefing
- **Protocol fee bypass:** Can users avoid fees through a sequence of small transactions?
- **Vampire attack surface:** Can a fork drain liquidity via identical interface with higher rewards?

---

## Step 8 — Sandwich Attack Verification

For AMM-integrated protocols:
- Can any swap or liquidity operation be sandwiched?
- Specifically: deposit → sandwich → user gets fewer LP tokens; withdraw → sandwich → user gets fewer tokens
- Fix: slippage protection on all liquidity operations, not just swaps

---

## Output Template

```
FINDING | contract: LendingPool | function: liquidate | bug_class: flash-loan-oracle-manipulation | severity: CRITICAL
path: attacker → flashLoan(USDC, 10M) → Uniswap.swap(depress ETH price) → LendingPool.liquidate(victim) → profit → repay flash loan
proof: ETH collateral priced from getReserves() — attacker depresses price from $2000 to $1500, triggering victim liquidation at 25% bonus; attacker nets $500/ETH on 10M USDC borrowed
description: Flash loan oracle manipulation enables attacker to artificially trigger liquidations and extract liquidation bonus at victim's expense
fix: Replace getReserves()-based pricing with Chainlink ETH/USD with 30-min TWAP fallback
```
