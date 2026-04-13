# Mars Poolin — Audit Findings (2026-04-13)

**Source:** Direct analysis of https://github.com/MarsFi/POWToken
**Methodology:** Pashov 8-agent parallel, 4-gate validation
**Report:** `audit-output/mars-poolin-audit-20260413.md`

## Finding Index

| ID | Sev | Contract | Line | Title | Status |
|----|-----|----------|------|-------|--------|
| M-01 | HIGH | POWToken.sol | 307 | inCaseTokensGetStuck — no guard on incomeToken/rewardsToken | OPEN |
| M-02 | HIGH | Staking.sol / LpStaking.sol | 60 / 72 | stakeWithPermit CEI violation | OPEN |
| M-03 | MEDIUM | Staking.sol / LpStaking.sol | 93 / 102 | exit() missing nonReentrant | OPEN |
| M-04 | MEDIUM | BTCParamV2.sol | 66 | updateBtcPrice() unlimited frequency — TWAP bypass | OPEN |
| M-05 | MEDIUM | LpStaking.sol | 65 | calculateLpStakingIncomeRate SafeMath underflow DoS | OPEN |
| M-06 | MEDIUM | TokenDistribute.sol | 84 | exchange() whitelist on `to` not `msg.sender` | OPEN |
| L-01 | LOW | POWToken.sol | 181 | getCurWorkingRate() bare multiplication | OPEN |
| L-02 | LOW | POWToken.sol | 113 | addHashRate() precision truncation | OPEN |
| L-03 | LOW | POWERC20.sol | 77 | uint(-1) deprecated sentinel | OPEN |
| I-01–04 | INFO | Various | — | TWAP window, typo, compiler bugs, proxy pattern | OPEN |

## Key Systemic Risk

Single-EOA control of owner + paramSetter + minter with no timelock. M-01 is the most acute consequence of this — owner can drain wBTC income pool with one tx.

## Audit Quality Notes

All findings are from real source code (not bytecode or summary analysis).
Every HIGH/MEDIUM includes exact line numbers, vulnerable code snippets, PoC sequences, and industry-standard fixes.
