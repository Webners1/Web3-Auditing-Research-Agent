# Product Review - Mars Poolin

| Field | Value |
|-------|-------|
| Date | 2026-04-13 |
| Reviewer | Web3 Auditing Agent |
| Product stage | Mainnet (maintenance / low-growth) |
| Chains | Ethereum Mainnet |

## Executive Summary
Mars Poolin still delivers a clear core product: tokenized Bitcoin hashrate with mining-linked reward distribution onchain. The highest non-contract risks are concentrated trust controls (single-key governance posture), opaque offchain attestation, and weak user-facing recovery UX when flows fail. Wallet support remains EOA-first, with no concrete smart-account or ERC-4337 path evidenced in reviewed contracts and docs. Product quality is salvageable if trust hardening and composability improvements are sequenced ahead of expansion.

## Product Snapshot
| Area | Score | Notes |
|------|-------|-------|
| Product clarity | 4 | Core utility is understandable: hold/stake hashrate token to earn mining-linked rewards |
| User safety | 2 | Reward/control risk perception remains high due to governance and transparency gaps |
| App flow and UX maturity | 2 | Primary flow is navigable for crypto-native users, but failure recovery guidance is thin |
| Smart wallet / AA readiness | 1 | No visible ERC-4337/paymaster/session-key implementation path |
| Offchain trust minimization | 2 | Backing and payout assumptions depend on centralized operational trust |
| Governance maturity | 1 | Single-key privileged control pattern is materially below market standard |
| Business model clarity | 3 | Value proposition exists but is under-positioned relative to BTCfi category shifts |

## What The Product Does
Mars Poolin tokenizes BTC mining hashrate exposure and allows users to stake for mining-linked rewards. It bridges real-world mining operations into an onchain position while retaining operational dependencies offchain.

## System Map
- Frontend: mars.poolin.fi app flow for wallet connect, exchange, staking, and claims.
- Core contracts: POWToken stack, Staking, LpStaking, TokenDistribute, BTCParamV2.
- Reward path: offchain mining output translated into onchain reward distribution.
- Governance/control path: owner/param-setting authority over critical behavior.
- Market surface: Ethereum mainnet-only deployment with relatively high transaction-cost sensitivity.

## Trust Boundaries
| Boundary | Why it exists | User impact |
|----------|---------------|-------------|
| Offchain mining operations | Yield originates from real-world hashrate and operator execution | Users must trust operational integrity and reporting quality |
| Privileged parameter control | Protocol parameters and critical paths require admin authority | Concentrated control increases governance/custody risk premium |
| Oracle and update cadence | Price and economics sensitivity requires externalized update logic | Weak cadence controls can impact payout fairness |
| Frontend and flow communication | Users rely on app-level guidance for complex flows | Poor recovery messaging can convert errors into churn |

## UX Flow Audit Summary
Primary workflow sampled:
1. Connect wallet
2. Acquire pBTC35A exposure
3. Stake and monitor rewards
4. Claim rewards

Observed friction:
- Trust-critical assumptions are not surfaced with enough operational detail at decision points.
- Failure states are mostly technical reverts instead of guided user recovery prompts.
- Policy boundaries (for example around access/eligibility controls) are not self-explanatory for non-power users.

Failure-path summary:
- Transaction or policy mismatch failures lack clear in-product remediation paths.
- Recovery confidence is low when state changes fail mid-journey.

## Smart Wallet and AA Readiness
| Capability | Status | Evidence | Gap |
|------------|--------|----------|-----|
| ERC-4337 support | No | No EntryPoint/UserOperation integration identified in reviewed contracts | No smart-account execution path |
| Bundler dependency handling | No | No bundler fallback behavior evidenced | Cannot gracefully handle AA infra outages |
| Paymaster sponsorship policy | No | No sponsorship module/policy found | No controlled gasless onboarding |
| Session-key guardrails | No | No scoped delegated-key controls observed | No safe delegated automation model |
| EIP-1271 compatibility | No | No explicit contract-signature verification path found | Weak compatibility with contract-wallet signing flows |

## Non-Contract Risk Register
| Category | Severity | Issue | Recommendation |
|----------|----------|-------|----------------|
| PRODUCT-RISK | High | Product trust thesis depends on offchain proof without strong user-verifiable attestations | Prioritize proof/disclosure layer before growth expansion |
| OPS-RISK | High | Concentrated operational control path raises governance-key risk | Move to multisig + timelock with public policy and cadence |
| TRUST-ASSUMPTION | High | Users cannot independently verify all backing and payout assumptions | Publish transparent attestation and operational reporting cadence |
| GO-TO-MARKET GAP | Medium | Product is not framed in modern BTCfi composability language | Reposition around verifiable mining-yield infrastructure |
| UX-FRICTION | Medium | Failure and recovery UX is weak for non-expert users | Add flow-specific remediation guidance and trust cues |
| AA-READINESS GAP | Medium | Smart-wallet and gasless readiness claims are unsupported by implementation evidence | Keep messaging explicit (EOA-first) until AA path is delivered |

## Contract Inventory
- Core contract: POWToken / POWTokenProxy
- Core contract: Staking
- Core contract: LpStaking
- Periphery contract: TokenDistribute
- Periphery contract: BTCParamV2
- External dependency: UniswapV2-style pair/oracle inputs

## Recommended Audit Scope
In-scope priority for deep contract/security pass:
- Privileged fund/control paths in POWToken and related admin functions
- Reward accounting and staking lifecycle functions in Staking/LpStaking
- Oracle update cadence and downstream economic sensitivity in BTCParamV2
- Distribution and authorization logic in TokenDistribute

Out-of-scope for contract-only review (but must be assessed in diligence):
- Offchain mining attestation integrity process
- Operator key ceremony and governance operations process
- Frontend failure-recovery and trust communication quality

## Founder Questions
1. What exact operational and cryptographic evidence can be published to strengthen mining-backing trust?
2. What is the concrete governance migration timeline from current privilege model to multisig/timelock?
3. Should AA readiness be a near-term roadmap item or explicitly deferred while positioning remains EOA-first?

## Sources
- https://mars.poolin.fi/
- https://github.com/MarsFi/POWToken
- https://defillama.com/protocol/mars-poolin
- https://eips.ethereum.org/EIPS/eip-4337
- https://eips.ethereum.org/EIPS/eip-1271
- https://docs.openzeppelin.com/contracts/4.x/api/governance
