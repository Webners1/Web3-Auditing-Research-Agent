# Web3 Protocol Diligence - Mars Poolin

| Field | Value |
|-------|-------|
| Date | 2026-04-13 |
| Reviewer | Web3 Auditing Agent |
| Scope | Product, contracts, architecture, strategy |
| Chains | Ethereum Mainnet |
| Repositories | https://github.com/MarsFi/POWToken |

## Executive Verdict
Mars Poolin still has a real and differentiated core utility: tokenized Bitcoin hashrate with on-chain distribution of mining-linked rewards. The current deployment, however, is not institutionally investable in its present form due to single-key control, no public historical audit baseline, and multiple unresolved medium/high-severity contract issues. The strongest near-term path is not broad feature expansion; it is trust-hardening first, then composability packaging. Based on the upgraded benchmarking method (function-matched, not popularity-matched), Mars Poolin should be compared primarily to BTC wrapper and BTC yield infrastructure protocols, not generic lending or AMM leaders. If security and governance hardening are shipped quickly, the product can still occupy a defensible Bitcoin-yield niche.

## Snapshot

| Area | Status | Notes |
|------|--------|-------|
| Product clarity | Mixed | Utility is clear (hashrate token + yield), but offchain-to-onchain trust path remains opaque to outside allocators |
| App flow and UX maturity | Mixed | Core path is understandable for crypto-native users, but trust cues and failure recovery guidance are thin |
| Smart wallet / AA readiness | Weak | No explicit ERC-4337/paymaster/session-key path identified in reviewed contracts or docs |
| Offchain trust model | Weak | Mining operations and reward backing rely on operator trust with limited cryptographic attestation |
| Contract security | Weak | 2 HIGH, 4 MEDIUM findings currently open in latest audit |
| Upgrade readiness | Mixed | Upgradeable proxy exists, but stack is legacy ZeppelinOS and should be modernized |
| Market positioning | Mixed | Category fit exists, but distribution and trust posture lag BTCfi standards |

## What The Product Is
Mars Poolin packages Bitcoin mining hashrate as an on-chain asset (pBTC35A) and routes mining-linked rewards to stakers. Users obtain and stake exposure via protocol contracts, while critical mining economics and some data dependencies remain offchain. The protocol's real value proposition is not generic DeFi yield; it is Bitcoin-mining-linked yield transformation into an ERC-20-centered product.

## Case Study Selection Logic (Upgraded Method)
This report uses a function-matched case-study suite:
1. Identify protocol utility and service boundary first (hashrate tokenization + BTC reserve exposure + yield distribution).
2. Select peers by utility similarity and trust architecture, not by TVL fame.
3. Use broad protocols (Aave/Uniswap) only for specific control-pattern benchmarks (timelock, governance hardening), not for core product comparability.

Selected comparable suite used in this diligence:
- Hashrate tokenization / mining-exposure peer: BTCST
- BTC reserve wrapper baseline: WBTC
- Multi-chain BTC reserve wrappers: Function FBTC, SolvBTC
- Restaked BTC yield packaging: Lombard LBTC
- Decentralized BTC wrapping design reference: iBTC Network (and category competitor tBTC)

## Top Risks
1. Governance and custody concentration risk: single-key privileged control remains a protocol-level failure domain.
2. Contract-layer loss/DoS risk: unresolved HIGH/MEDIUM findings can directly impact user funds and payout reliability.
3. Trust discount risk: no strong reserve-attestation and control-delay layer means external allocators price in governance/custody risk.

## Top Opportunities
1. Trust-premium upgrade: multisig + timelock + reserve-attestation can convert the protocol from trust-discounted to trust-verifiable.
2. BTCfi distribution fit: ERC-4626-style packaging and integration-first roadmap can unlock aggregator and structured-yield channels.
3. Narrative advantage: few protocols combine mining-linked yield with on-chain composability; this can be a focused market story if risk posture is corrected.

## Product Review Summary
- Product objective is clear and differentiated: convert hashrate output into an on-chain yield primitive.
- Non-contract risk is dominated by trust disclosure, governance concentration, and weak failure-recovery UX.
- Smart-wallet/account-abstraction readiness is currently not evidenced; product posture remains explicitly EOA-first.

## UX and Wallet Flow Summary
Primary workflow reviewed:
1. Connect wallet
2. Acquire pBTC35A through exchange flow
3. Stake in pool contract
4. Claim mining-linked rewards

Observed friction themes:
- Trust explanation is under-specified at decision points where users must accept offchain dependencies.
- Failure handling is largely technical (transaction reverts) rather than guided (clear corrective next action).
- Role and policy semantics (for example whitelist behavior) are not obvious at user level, which increases support burden and perceived risk.

Failure-path assessment (high-level):
- Wrong-eligibility or policy mismatch paths can fail hard without clear in-product remediation cues.
- If reward pathways are disrupted, user-facing diagnostics are minimal, which can convert operational incidents into retention loss.

## Smart Wallet / Account Abstraction Readiness Summary
| Capability | Status | Evidence | Gap |
|------------|--------|----------|-----|
| ERC-4337 smart account path | No | No EntryPoint/paymaster/bundler integration surfaced in reviewed contracts | No gasless/smart-account onboarding path |
| Paymaster sponsorship policy | No | No sponsorship logic or spend policy found | Cannot support controlled gas abstraction |
| Bundler dependency handling | No | No UserOperation lifecycle handling identified | No fallback behavior for AA infrastructure failures |
| Session-key controls | No | No scoped delegated-key model observed | No low-friction delegated execution support |
| EIP-1271 contract signatures | No | No explicit contract-signature verification surfaced | Limits compatibility with smart-wallet signature flows |

Business implication:
- Current wallet posture remains EOA-first. This is acceptable for a narrow crypto-native base, but weak for broader onboarding or mobile-first distribution strategies.

## Audit Summary
Latest audit baseline (2026-04-13) found:
- 2 HIGH
- 4 MEDIUM
- 3 LOW
- 4 INFO

Most material open items:
- Owner-drain vector in token rescue path (`inCaseTokensGetStuck` guard gap)
- CEI/order-of-operations weakness in `stakeWithPermit`
- Oracle cadence control gap enabling practical manipulation windows
- Whitelist logic bypass pattern in exchange flow

Inference note: these findings are direct code-review facts from repository analysis, not market-data inferences.

## Remediation Summary
Effort-tiered remediation priority:
- Immediate (low effort, high impact): close direct fund-movement and authorization gaps; move privileged roles to multisig-backed control.
- Near-term (medium effort): harden oracle flow, complete CEI and reentrancy-safe refactors, add invariant-focused regression tests.
- Program-level (high effort): modernize upgrade stack (EIP-1967-compatible path), then ship composability wrappers and reserve-proof architecture.

## Architecture Summary
Current architecture strengths:
- Clear contract boundary around staking and distribution
- Existing upgrade surface that can be used for migration

Current architecture debt:
- Legacy proxy stack and Solidity vintage increase maintenance and upgrade risk
- Offchain dependency transparency is insufficient for institutional-grade diligence
- Mainnet-only posture constrains distribution economics for smaller users

Recommended architecture direction:
- Security control plane first (Safe + timelock + role partitioning)
- Oracle hardening with explicit cadence/staleness controls
- Standards-first composability layer for downstream integrations

## CEO Strategy Summary
Positioning recommendation:
- Compete as verifiable BTC mining-yield infrastructure, not as another generic yield farm.

Strategic sequencing:
1. Earn trust (security, controls, proofs)
2. Earn distribution (composable wrappers, integrations)
3. Then scale product surface (new BTCfi primitives, selective chain expansion)

Single biggest non-code risk:
- Market perception of governance/custody fragility can block TVL growth even if contract issues are patched.

Comparable-set strategy note:
- Use function-matched peers and one one-curve-ahead benchmark to drive roadmap choices, not generic blue-chip comparison sets.

## Positioning and Comparable Strategy Summary
- Direct functional peers (BTCST, Mars Poolin) inform product-shape and retention economics.
- Adjacent alternatives (WBTC wrappers, SolvBTC, Function FBTC) frame trust-disclosure and distribution expectations.
- One-curve-ahead benchmark (Lombard LBTC and broader restaked-BTC packaging) highlights where BTC yield products are moving: stronger composability, clearer trust architecture, and tighter integration pathways.
- Strategic takeaway: Mars Poolin should sequence trust-hardening and composability before expansion, or it will be benchmarked as legacy BTC yield infrastructure.

## 30 / 60 / 90 Day Plan

### 0-30 Days
- Patch all HIGH findings and high-leverage MEDIUM findings.
- Move privileged roles to multisig and publish control policy.
- Publish remediation changelog and external validation plan.

### 31-60 Days
- Implement oracle hardening and regression/invariant test expansion.
- Define and publish reserve transparency roadmap (attestation cadence and controls).
- Prepare proxy modernization plan and migration safety runbook.

### 61-90 Days
- Ship composability packaging for integration channels.
- Run first partner integration pilots with BTCfi-compatible venues.
- Launch measurable KPI loop: retention, integration conversion, incentive efficiency.

## Recommended Engagement Sequence
1. Remediation implementation sprint and focused re-audit.
2. Governance and trust architecture hardening rollout.
3. Integration-led growth plan with function-matched BTCfi partners.

## Function-Matched Industry Comparison (Point-in-Time)
Snapshot date: 2026-04-13 (DefiLlama point-in-time values)

## Category Signals and Sentiment
| Signal | Source | Interpretation | Confidence |
|--------|--------|----------------|------------|
| BTC wrapper and BTC-yield protocols retain meaningful aggregate capital despite volatility | DefiLlama protocol/category pages in Sources | Market still assigns value to BTC-denominated utility, but prefers stronger trust and integration layers | FACT |
| Competitive set is shifting from simple wrappers toward composable BTC yield packaging | DefiLlama plus comparable-set composition in this report | Category expectations are moving toward integration-ready primitives rather than isolated pools | INFERENCE |
| Narrative headroom exists for a verifiable mining-yield category leader if trust deficits are closed | Messari research portal plus category data context | Positioning upside is plausible, but execution-dependent and sensitive to credibility milestones | HYPOTHESIS |

| Protocol | Functional Role | Reported TVL Snapshot | Relevance to Mars Poolin |
|----------|------------------|-----------------------|----------------------------|
| Mars Poolin | Hashrate tokenized yield | ~$133k | Target protocol baseline |
| BTCST | Hashrate tokenization peer | ~$895k | Directly comparable product shape |
| WBTC | Reserve-backed BTC wrapper | ~$8.275b | Reserve trust and transparency benchmark |
| Function FBTC | Cross-chain BTC wrapper infra | ~$780m | Composability and routing benchmark |
| SolvBTC | BTC reserve + yield routing | ~$505m | BTC-yield packaging benchmark |
| Lombard LBTC | Restaked BTC yield primitive | ~$739m | Yield-bearing BTC product benchmark |
| tBTC | Decentralized BTC bridge token | ~$437m | Decentralized custody and bridge-governance benchmark |
| iBTC Network | Decentralized BTC wrapping | ~$181 | Decentralized custody model reference |

Inference note: TVL scale differences do not imply direct superiority of product design; they indicate market adoption and trust/distribution outcomes under different architectures. Comparable-set inclusion is functional, not an endorsement of each protocol's current risk posture.

## Sources
- https://github.com/MarsFi/POWToken
- https://mars.poolin.fi/
- https://defillama.com/protocol/mars-poolin
- https://defillama.com/protocol/btcst
- https://defillama.com/protocol/wbtc
- https://defillama.com/protocol/solvbtc
- https://defillama.com/protocol/lombard-lbtc
- https://defillama.com/protocol/function-fbtc
- https://defillama.com/protocol/ibtc-network
- https://defillama.com/protocol/tbtc
- https://defillama.com/protocols/decentralized-btc
- https://defillama.com/protocols/restaked-btc
- https://messari.io/research
- https://messari.io/
- https://eips.ethereum.org/EIPS/eip-1967
- https://docs.openzeppelin.com/contracts/4.x/api/governance
- https://chain.link/proof-of-reserve
- https://app.safe.global/

## Internal Artifacts Used
- audit-output/mars-poolin-product-20260413.md
- audit-output/mars-poolin-audit-20260413.md
- audit-output/mars-poolin-arch-20260413.md
- audit-output/mars-poolin-strategy-20260413.md
