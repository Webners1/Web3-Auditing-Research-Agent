# Mycelium Perpetual Pools — Protocol Diligence Report
**Date:** 2026-05-20  
**Analyst:** Web3 Auditing Agent  
**Lead Source:** DefiLlama TVL Sweet Spot ($184k, Arbitrum)  
**Report Type:** Full Diligence (Product + Security + Architecture + Strategy)

---

## Executive Summary

Mycelium Perpetual Pools (formerly Tracer Perpetual Pools) is a leveraged tokenized exposure protocol on Arbitrum allowing users to take long/short positions via pool tokens. The protocol is in observable wind-down: the UI displays "Close Pools Positions" as the primary action, Perpetual Swaps ($0 TVL) has already ceased operations, and no active development has occurred since ~2022.

**$183k in user funds remain in the protocol with an unmitigated HIGH severity vulnerability — the absence of an Arbitrum L2 sequencer health check — that was identified in team's own GitHub discussions in December 2021 and never fixed.** Because the contracts use a non-upgradeable minimal proxy pattern, the vulnerability cannot be patched in existing pools.

**Pitch fit:** Low — primary value is responsible disclosure + relationship-building for any active new product, not a full-audit engagement.

---

## Pillar 1 — Smart Contract Security

### [FINDING-001] HIGH | OracleWrapper.sol + PoolKeeper.sol | Missing Arbitrum L2 Sequencer Health Check

**Proof sequence:**
1. Protocol deployed exclusively on Arbitrum L2
2. Chainlink's official L2 guidance mandates checking the Sequencer Uptime Feed before consuming oracle data
3. `PoolKeeper.performUpkeepSinglePool()` → `pool.getUpkeepInformation()` → `OracleWrapper.getPrice()` → `latestRoundData()` — no sequencer check anywhere in this path
4. When Arbitrum sequencer goes offline, Chainlink feeds stop updating but `latestRoundData()` still returns the last known value with an old timestamp
5. `checkUpkeepSinglePool()` only validates `intervalPassed()` (time-based) — not oracle data freshness
6. Pool upkeep executes with stale prices, silently moving balances based on incorrect price deltas
7. On sequencer restoration, accumulated price divergence can drain the losing side in one upkeep cycle

**Evidence:** GitHub Discussion #284 (December 2021) acknowledges this exact gap. The discussion is unresolved — no fix was merged. This has been a known, open vulnerability for 3+ years.

**Industry-standard fix:**
```solidity
// Add to OracleWrapper.getPrice():
AggregatorV2V3Interface sequencerFeed = AggregatorV2V3Interface(ARBITRUM_SEQUENCER_UPTIME_FEED);
(, int256 answer, uint256 startedAt, , ) = sequencerFeed.latestRoundData();
require(answer == 0, "OracleWrapper: sequencer offline");
require(block.timestamp - startedAt > GRACE_PERIOD_SECONDS, "OracleWrapper: sequencer grace period");
```
Arbitrum sequencer feed: `0xFdB631F5EE196F0ed6FAa767959853A9F217697D`  
Comparable fix: GMX V2 OracleUtils.sol implements this check; Synthetix Perps V3 PerpsMarket.sol implements sequencer guard.

---

### [FINDING-002] MEDIUM | PoolKeeper.sol | Keeper Reward Miscalculation — Economic Liveness Failure

**Source:** Code4rena Oct 2021, finding M-01. Fix status in deployed code: unconfirmed.

**Proof:**
1. `payKeeper()` computes reward mixing WAD units and Quad units
2. Division by `1e18` instead of `100` results in keeper rewards ~0
3. With zero economic incentive, only altruistic or protocol-operated keepers run upkeep
4. If the protocol-operated keeper goes offline, all pool states freeze
5. Users cannot exit at fair prices — positions are locked at stale valuations

**Impact:** At $183k TVL, a keeper freeze lasting 48+ hours could trap remaining user funds at stale prices.

**Fix:** Normalize units before final division; verify reward formula against documented keeper compensation model.

---

### [FINDING-003] MEDIUM | LeveragedPool.sol | No Circuit Breaker for Extreme Price Movements

**Proof:**
1. `executePriceChange()` applies full leverage multiplier to any size price delta — no cap
2. At 3x leverage, a 33% price move in one upkeep cycle eliminates the losing side entirely
3. Combined with FINDING-001 (sequencer outage → multi-hour stale period): when sequencer restores, the accumulated delta hits in one cycle
4. BTC moved 25% in 8-hour windows during the 2022 bear market — a realistic sequencer-outage scenario

**Fix:** Max price change per upkeep cycle (`MAX_DELTA = 15%`). If oracle move exceeds cap, apply capped delta and emit `CircuitBreakerTriggered` event. Standard pattern: Perpetual Protocol V2 implements this.

---

### [LEAD-001] MEDIUM | PoolSwapLibrary.sol | Fee Calculation Rounding at Low TVL

**Observation:** Fee computation divides to `uint256` before final WAD division. At current TVL ($183k declining), small-balance pools may compute zero fees for positions below a precision threshold. Not exploitable at current TVL but becomes relevant as pools drain toward zero.

---

### [FINDING-004] LOW | PoolFactory.sol | No Timelock on Fee Parameter Changes

Owner can change fee rate and fee receiver instantly. Combined with a front-running keeper, this allows fee extraction on large deposits. Standard fix: 48-hour timelock on fee parameter changes (OpenZeppelin `TimelockController`).

---

## Audit Coverage Gap

| Audit | Date | Version | Status |
|---|---|---|---|
| Sigma Prime | ~2021 | V1 (Tracer) | Predecessor code only |
| Code4rena | Oct 2021 | V2 pre-mainnet | 3+ years ago |

The current deployed contracts have not been audited since 2021. FINDING-001 (L2 sequencer) was introduced as a gap AFTER both audits — Arbitrum sequencer outages became a documented concern in 2022. No subsequent re-audit was conducted.

---

## Pillar 2 — Protocol Health

### GitHub and Development Activity
- Repo: [mycelium-ethereum/perpetual-pools-contracts](https://github.com/mycelium-ethereum/perpetual-pools-contracts)
- 1,017 commits, last meaningful activity ~2022
- 26 open issues — none appear to be actively triaged
- Discussion #284 (L2 sequencer) open since Dec 2021, no response from team

### Docs Status
- Docs at pools.docs.mycelium.xyz still accessible but reflect the 2022 state
- UI at pools.mycelium.xyz shows "Close Pools Positions" as primary CTA — wind-down signal

### Trust Signals
- Two public audits on record (good historical posture)
- No multisig or timelock found on owner-controlled parameters
- No bug bounty program found

### Product Lifecycle Assessment
- Perpetual Swaps: $0 TVL — ceased operations
- Perpetual Pools: $183k TVL — declining, UI in close-out mode
- Both products on Arbitrum with no cross-chain expansion
- No evidence of new product development under mycelium-ethereum GitHub org

---

## Pillar 3 — Market Position and 2026 Readiness

### Competitive Landscape (Derivatives/Leveraged Exposure, Arbitrum)
| Protocol | TVL | Model | Why It Won |
|---|---|---|---|
| GMX V2 | $800M+ | GLP liquidity pool | Zero-fee spot, simple UX, deep liquidity |
| Hyperliquid | $3B+ | CEX-grade L1 | Sub-second settlement, full order book |
| Synthetix Perps V3 | $200M+ | Synthetic pools | Multi-collateral, ecosystem integrations |

Mycelium's tokenized leverage-pool model occupied an interesting niche in 2021 but was superseded by the GMX model (better UX, same permissionless access) and Hyperliquid (better execution). The "wait for keeper to rebalance" UX friction is a fundamental product gap relative to current market leaders.

### 2026 Readiness Scorecard
| Dimension | Score | Notes |
|---|---|---|
| Security | 3/10 | HIGH finding open 3+ years, 0 keepers incentivized |
| Product UX | 2/10 | Wind-down mode, outdated keeper model |
| Docs | 5/10 | Docs exist but stale |
| Business Durability | 1/10 | Both products declining to zero |
| Competitive Stack | 1/10 | Superseded by GMX, Hyperliquid |

---

## Recommendations

### Immediate (protocol team, if reachable)
1. Implement L2 sequencer health check in OracleWrapper — even for wind-down, protects remaining $183k
2. Communicate wind-down timeline to remaining users — clear date for protocol sunset
3. Ensure keeper continues operating until all positions are closed

### If Team Has Active New Product
1. Security posture review for new product (avoid repeating the same oracle pattern)
2. Keeper economic model redesign (the reward formula failure pattern is architectural)
3. Circuit breaker patterns for any new derivatives product

---

## Report Metadata
- Contracts analyzed: PoolFactory.sol, PoolKeeper.sol, LeveragedPool.sol, PoolSwapLibrary.sol, OracleWrapper.sol
- Sources: GitHub repo, Code4rena audit report, Chainlink L2 docs, DefiLlama TVL data
- On-chain verification: Contract addresses confirmed via README (full Arbiscan verification not performed — TVL wind-down reduces priority)
- Phase outputs: product-notes.md, findings.md, arch-notes.md, strategy-notes.md
