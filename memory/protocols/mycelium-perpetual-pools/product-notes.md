# Mycelium Perpetual Pools — Product Notes
Date: 2026-05-20

## Protocol Identity
- **Name:** Mycelium Perpetual Pools (formerly Tracer Perpetual Pools)
- **Slug:** mycelium-perpetual-pools
- **Chain:** Arbitrum One
- **Category:** Derivatives — leveraged tokenized pool exposure
- **TVL:** ~$183k (declining; peak was higher during 2022)
- **Website:** pools.mycelium.xyz (still accessible, "Close Pools Positions" UI)
- **GitHub:** https://github.com/mycelium-ethereum/perpetual-pools-contracts
- **Twitter:** @mycelium_xyz

## What It Does
Users deposit a settlement token (USDC) and receive long or short pool tokens representing leveraged exposure to price pairs (BTC/USD, ETH/USD). A permissionless keeper network periodically calls upkeep functions that update oracle prices and rebalance pool balances — losers' capital flows to winners based on a leverage multiplier.

Leverage is encoded into the pool at deploy time (1x, 3x, etc.). There is no liquidation mechanism; instead, the entire pool rebalances on each keeper cycle.

## Contract Architecture
| Contract | Address (Arbitrum) | Function |
|---|---|---|
| PoolFactory | 0x98C58c1cEb01E198F8356763d5CbA8EB7b11e4E2 | Deploys pool clones via minimal proxy |
| PoolKeeper | 0x759E817F0C40B11C775d1071d466B5ff5c6ce28e | Permissionless upkeep trigger + keeper rewards |
| OracleWrapper (BTC) | 0xE973E6400B44fd20fc4752c03D112274A1374bA0 | Wraps Chainlink BTC/USD |
| OracleWrapper (ETH) | 0xeceaea7e0408606714b2559ac9b1d3d51a327afe | Wraps Chainlink ETH/USD |
| LeveragedPool | (per pool, cloned) | Holds long/short balances, executes price changes |
| PoolSwapLibrary | (library) | Leveraged math, fee calculations, WAD arithmetic |
| PoolToken | (per pool side) | ERC20 representing long or short pool position |

Upgrade pattern: **minimal proxy (Clones)** — contracts are NOT upgradeable after deployment.

## Trust Model
- **Owner/Gov:** Controls fee settings, maxLeverage, fee receiver address, pool deployment authorization
- **Keepers:** Permissionless — anyone can call upkeep. Economic incentive: keeper reward paid from pool fees
- **Oracle:** Chainlink price feeds wrapped in OracleWrapper contracts
- **No multisig or timelock found** in documented architecture

## Audit History
| Audit | Date | Version | Severity |
|---|---|---|---|
| Sigma Prime | ~2021 | V1 | Unknown — V1 codebase |
| Code4rena | Oct 2021 | V2 (pre-mainnet) | 0 HIGH, 3 MEDIUM, 4 LOW |

**Key C4 findings (Oct 2021):**
- M-01: Keeper reward computation mixes WAD/Quad units → rewards ~0
- M-02: Fee-on-transfer token deposits break pool balance accounting
- M-03: `uncommit` sends tokens to pool contract instead of user (user loses funds)

**Gap:** No public audit after October 2021. The contracts have been live for 3+ years with no re-audit.

## Protocol Status
- Pools UI accessible but shows "Close Pools Positions" — suggests the team is winding down Perpetual Pools
- Mycelium Perpetual **Swaps** is the active product (separate protocol, likely higher TVL)
- TVL declining: $183k remaining is likely residual positions that haven't been exited
- 26 open GitHub issues, last meaningful commits appear to be 2022

## UX Observations
- "Close Pools Positions" as the homepage CTA suggests the protocol is in wind-down mode
- No new pools being deployed
- Docs at pools.docs.mycelium.xyz still up

## Phase Handoff
- Protocol: Mycelium Perpetual Pools
- Chain: Arbitrum One
- Key finding from this phase: Protocol appears to be in wind-down (TVL declining, UI shows "Close Pools Positions"). No re-audit since Oct 2021. Core oracle staleness risk noted.
- Open question for next phase: Are the oracle staleness protections in PoolKeeper sufficient? Is M-03 (uncommit bug) fixed?
- Skip next phase? No — security findings are the primary pitch hook here
