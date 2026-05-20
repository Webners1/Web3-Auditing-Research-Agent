# Mycelium Perpetual Pools — Security Findings
Date: 2026-05-20

## Summary
- CRITICAL: 0
- HIGH: 1
- MEDIUM: 3
- LOW: 1

---

[FINDING-001] HIGH | OracleWrapper.sol + PoolKeeper.sol | Missing Arbitrum L2 Sequencer Health Check

**Proof sequence:**
1. Protocol is deployed exclusively on Arbitrum L2
2. Chainlink's official L2 guidance requires checking the Sequencer Uptime Feed before consuming price data (docs.chain.link/data-feeds/l2-sequencer-feeds)
3. `PoolKeeper.performUpkeepSinglePool()` calls `pool.getUpkeepInformation()` → `OracleWrapper.getPrice()` → Chainlink `latestRoundData()` — no sequencer health check in this path
4. When Arbitrum sequencer goes offline: Chainlink oracle stops updating but PoolKeeper can still be called by any keeper address
5. Keeper receives `latestPrice` = last stale price before outage; `checkUpkeepSinglePool()` only checks `intervalPassed()` (time-based, not oracle freshness)
6. `pool.poolUpkeep(lastExecutionPrice, latestPrice)` executes with stale delta — pool balances update incorrectly
7. When sequencer restores, market price diverges from last-used price; arbitrageurs can deposit into favorable side and drain the other side

**Evidence:** GitHub Discussion #284 (Dec 2021) explicitly acknowledges this gap. Team discussion remains UNRESOLVED — no fix was merged.

**Industry fix:** Add Chainlink Sequencer Uptime Feed check (Arbitrum feed: `0xFdB631F5EE196F0ed6FAa767959853A9F217697D`) at the top of `OracleWrapper.getPrice()`:
```solidity
(, int256 answer, uint256 startedAt, , ) = sequencerUptimeFeed.latestRoundData();
require(answer == 0, "Sequencer offline");
require(block.timestamp - startedAt > GRACE_PERIOD, "Sequencer grace period not passed");
```
Comparable protocols: Synthetix Perps V2, GMX — both implement sequencer health checks on Arbitrum.

---

[FINDING-002] MEDIUM | PoolKeeper.sol | Keeper reward miscalculation creates keeper centralization risk

**From Code4rena M-01 (Oct 2021) — fix status unconfirmed in current deployed code**

Proof:
1. `payKeeper()` computes reward using WAD units for one value and Quad units for another
2. Division by `1e18` instead of `100` makes keeper rewards approximately zero
3. With zero economic incentive, permissionless keepers don't run upkeep
4. Pool updates rely on protocol team running a centralized keeper or altruistic operators
5. If that keeper goes down, pool state freezes — users cannot exit at fair prices

**Impact:** Keeper liveness failure. With $183k TVL, prolonged keeper absence traps user funds at incorrect valuations.

**Fix:** Correct keeper reward formula to use consistent units.

---

[FINDING-003] MEDIUM | LeveragedPool.sol | No price circuit breaker for extreme oracle movements

Proof:
1. `executePriceChange()` calls `PoolSwapLibrary.calculatePriceChange(leverage, longBalance, shortBalance, oldPrice, newPrice)`
2. No maximum price-change-per-period cap exists
3. With 3x leverage pools on BTC/USD: a 30% price move (within normal crypto volatility over a missed upkeep window) completely drains the losing side
4. Combined with FINDING-001 (sequencer outage → stale prices → multi-hour missed updates): when sequencer restores, the accumulated price delta hits in one upkeep cycle
5. Example: Sequencer offline 8 hours, BTC moves 25%. 3x pool losers lose 75% of balance in one cycle.

**Industry fix:** Max price-change-per-upkeep cap (e.g., 15% per cycle). If exceeded, skip balance transfer and emit event. GMX and Perp Protocol both implement circuit breakers for this scenario.

---

[LEAD-001] MEDIUM | PoolSwapLibrary.sol | Division-before-multiplication precision loss in fee calculation

**Observation (not yet proven at current TVL scale):**
- Fee computation: `convertDecimalToUInt(multiplyDecimalByUInt(fee, balance)) / WAD_PRECISION`
- Converts to uint256 before final WAD division
- At small balance values (→$0 as TVL declines), fee can round to zero, fee receiver gets nothing
- Not a fund-loss finding at $183k TVL but becomes critical in low-TVL wind-down
- Status: verified at code level, impact depends on current fee rate × balance combination

**Fix:** Keep full decimal precision until final conversion step.

---

[FINDING-004] LOW | PoolFactory.sol | No timelock on fee and feeReceiver changes

Proof:
1. `setFee()` and `setFeeReceiver()` callable immediately by owner with no delay
2. Owner can front-run large deposits by raising fee to max, then restoring
3. Governance transfer is two-step (good) but fee changes are single-step (inconsistent)

**Fix:** Add 48-hour timelock on fee parameter changes (standard for DeFi governance).

---

## Audit Gap Assessment

| Audit | Date | Version | Gap |
|---|---|---|---|
| Code4rena | Oct 2021 | V2 | 3+ years unaudited |
| Sigma Prime | ~2021 | V1 | Predecessor only |

**No public audit covers the current production contracts.** The L2 Sequencer finding (FINDING-001) was introduced after the audit period. The keeper reward bug (FINDING-002) was found in C4 but may not have been fixed in the deployed version.

## Phase Handoff
- Protocol: Mycelium Perpetual Pools
- Chain: Arbitrum One
- Key finding: Missing Arbitrum L2 Sequencer Health Check (HIGH) — documented gap, unresolved since Dec 2021
- Open question for next phase: Is this protocol in wind-down? Should pitch focus on remediation consulting rather than full audit?
- Skip next phase? No — architecture review will determine pitch angle (full audit vs. targeted fix)
