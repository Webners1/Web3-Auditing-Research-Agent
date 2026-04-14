---
name: product-assessor
description: Product-level Web3 assessment covering trust boundaries, UX flow, wallet safety, and contract surface mapping.
---

# Web3 Product Assessor and Surface Mapper

Assesses a Web3 product before the smart contract audit starts. Focuses on non-smart-contract issues: user journey, trust assumptions, frontend risk, backend dependencies, governance controls, offchain infrastructure, token utility, and operational maturity. Produces a product risk report and hands the correct contracts into scope for deep audit.

**Trigger phrases:** `assess this product`, `review this dapp`, `product diligence`, `web3 product review`, `review non smart contract risks`, `map this protocol`, `what is missing in this product`, `find the contracts behind this app`, `audit app flow`, `check ux`, `wallet ux review`, `smart wallet readiness`

---

## Execution Pipeline

### Phase 0 - Source Routing

Load `../protocol-diligence/references/research-source-registry.md`.

Research order:
1. Official project sources
2. Curated Web3 data sources from the registry
3. Explorer sources
4. Generic search only if the required information is still missing

### Phase 1 - Product Surface Mapping

Collect evidence from as many of these sources as are available:
- README, docs, litepaper, whitepaper, pitch deck
- Frontend code (`app/`, `src/`, `frontend/`, `web/`)
- Backend, API, indexer, relayer, keeper, or bot code
- Deployment configs, ABI files, address books, env samples
- Governance docs, multisig lists, incident docs, token docs

Map:
1. Primary user actions: connect, deposit, stake, swap, bridge, vote, withdraw, claim
2. Primary user workflow threads: onboarding, first successful transaction, repeat usage, failure recovery
3. Core components: frontend, contracts, backend APIs, indexers, keeper bots, multisigs, signers, oracles, bridges
4. Chain footprint: mainnet, L2s, appchains, testnets
5. Trust boundaries: what users must trust beyond the contracts
6. Revenue path: fees, spread, token utility, subscription, hidden centralization
7. Readiness evidence pack: docs quality, GitHub hygiene, incident transparency, and product narrative clarity

Run `skills/ux-audit/SKILL.md` as Phase 1.5 immediately after surface mapping. This is mandatory — complete the full UX audit before proceeding to Phase 2. The UX audit outputs (UX Posture score, summary table, all HIGH/CRITICAL findings) feed directly into Phase 2's UX row and Phase 2.4's trust signal register. Do not defer or skip UX review.

Load `references/product-review-checklist.md` before scoring risk.

### Phase 2 - Non-Contract Risk Review

Assess these dimensions:

| Dimension | What to inspect |
|-----------|-----------------|
| UX and wallet safety | Approval flows, signature clarity, slippage controls, network mismatch handling |
| App flow and UI/UX maturity | Can users finish core tasks quickly with low confusion, clear wayfinding, and resilient recovery states |
| Frontend trust | Admin-controlled config, upgrade banners, contract address sourcing, remote script risk |
| Backend dependencies | Private APIs, sequencers, relayers, keepers, cron jobs, indexers, cloud trust |
| Smart wallet and account abstraction readiness (conditional) | Evaluate only when the product relies on smart wallets, gas sponsorship, delegated sessions, or contract-signature flows |
| Key and admin risk | EOAs vs multisigs, timelocks, guardians, emergency authority |
| Governance maturity | Parameter controls, pause process, upgrade process, incident path |
| Token and incentive design | Value capture, reflexivity, emissions, mercenary liquidity risk |
| Smart contract quality signals | Test depth, invariant/fuzz evidence, NatSpec quality, and code hygiene visible in public repos |
| Documentation, GitHub, and presentation readiness | Setup docs, architecture clarity, changelog/incident communication, and investor/partner readiness artifacts |
| Monitoring and operations | Alerts, runbooks, dashboards, freeze levers, disclosure process |
| Legal and user trust disclosures | What is decentralized vs what is managed offchain |

For each issue, classify:
- `PRODUCT-RISK`
- `OPS-RISK`
- `TRUST-ASSUMPTION`
- `GO-TO-MARKET GAP`
- `UX-FRICTION`
- `AA-READINESS GAP`
- `MARKET-READINESS GAP`

### Phase 2.4 - Observable Trust Signal Audit

Collect the factual evidence that external parties — capital allocators, integrators, protocol reviewers, and serious users — actually check before engaging. Record facts first. Do not write generic assessments. "Docs last updated 8 months before v2 deployment" is a finding. "Update your docs" is not.

**GitHub Activity**
Check the main repository branch:
- Last commit date and how many days ago that is
- Commit count: last 30 days / last 90 days / last 180 days
- Open issues: total count, date of oldest unresolved issue
- PR activity: merges in last 90 days
- Contributor count: unique authors in last 6 months
- README and test coverage: last updated, visible test depth

**Documentation**
- Last update date or version stamp on docs site or README
- Coverage: are all deployed contracts documented? Are verified contract addresses listed for every network?
- Integration guide: does one exist for builders who want to compose with this protocol?
- Changelog or release notes: public history of changes?
- Incident disclosure: any past incidents documented publicly with post-mortems?

**Audit Standing**
- Published audit reports: list each — firm name, date, contract version covered
- Currency check: is the currently deployed code within the scope of the most recent audit, or has the code changed since?
- Bug bounty: active program on Immunefi or equivalent, maximum payout tier

**Recent Shipping History**
- Major protocol upgrades or new contract deployments in the last 6 months: what shipped, when, claimed impact
- Publicly announced integrations or partnerships in the last 6 months
- Testnet activity

**Team and Entity Signals**
- Doxxed contributors or known pseudonymous identities with established track records
- Legal entity or DAO operating the protocol
- Official communication channels and their last update

**Community Signals**
- Governance participation rate if on-chain governance exists (voter turnout, proposal count)
- Discord or Telegram: active, slow, or abandoned
- Social media: update frequency and recent communications

**Output format (required):**
Record as observations, not assessments:
- "Last GitHub commit: [date] — [N] days before this review"
- "Docs last updated: [date] — [N] months before/after most recent contract deployment"
- "Audit: [Firm] reviewed [version] on [date] — deployed code [is/is not] within that audit scope"
- "Open issues: [N] total — oldest unresolved: [age]"
- "Shipping history: [what shipped in last 6 months, or 'no major releases in this period']"

Then for each weak or missing signal, add one specific named comparison:
- Name a protocol in the same category with demonstrably better standing on this dimension
- State specifically what they do (not "they have better docs" — "Morpho Blue ships a docs PR within 24 hours of every contract deployment and attributes first integration partner onboarding to this practice")
- State the specific consequence for this protocol ("without current docs covering the v2 deployment, aggregator onboarding requires manual contract discovery, which most integrators skip")

---

### Phase 2.5 - Smart Wallet / Account Abstraction Checkpoint (Conditional)

Run this checkpoint only if smart-wallet or account-abstraction behavior is part of the real product path. If not applicable, mark `Not Applicable` with one sentence explaining why.

If the product claims smart wallet UX, gasless onboarding, or account abstraction support, verify concrete implementation details:
1. Account model: EOA only, Safe-style multisig, or ERC-4337 smart account
2. Gas model: user-paid ETH, relayed sponsorship, paymaster limits, and rate controls
3. Validation model: replay resistance, nonce handling, and signature domain clarity
4. Bundler/paymaster resilience: fallback path if bundler or paymaster rejects UserOperations
5. Session key constraints: target allowlists, spend limits, expiry, and revocation path
6. Interop: EIP-1271 support where contract-signature flows are required

Do not call a product AA-ready if support is only marketing copy without deployed entrypoint/paymaster/bundler behavior.

### Phase 2.6 - 2026 Web3 Market-Readiness Pass

Score the product against a 2026-readiness baseline with explicit evidence:
1. UI/UX execution and failure recovery quality
2. Security posture and incident resilience
3. Smart contract engineering maturity (tests, auditability, code quality)
4. Docs/GitHub/presentation quality for users, partners, and reviewers
5. Product clarity and category positioning
6. Business model durability and 12-month relevance
7. Comparative stack competitiveness against function-matched peers

Any dimension below threshold should produce at least one concrete recommendation tied to cost, owner, and expected upside.

### Phase 3 - Smart Contract Handoff

Locate the contract surface that should move into audit:
1. Find Solidity files, deployed addresses, ABIs, and contract registries
2. Separate core contracts from periphery, interfaces, libraries, mocks, and vendors
3. Identify protocol type and critical invariants
4. Record questions that the security audit must answer

If the product uses third-party contracts heavily, mark what is:
- Owned in-house
- Forked
- Vendor-managed
- Immutable external dependency

### Phase 4 - Output

Write the product report using `references/report-format.md`:

```
audit-output/[project-name]-product-[YYYYMMDD].md
```

The report must include:
- Product summary
- System map
- Trust boundary map
- Non-contract risk register
- Contract inventory and audit scope recommendation
- Open questions for founders or engineers
- Sources appendix with exact URLs

---

## Product Assessor Rules

- Do not call something decentralized if critical actions depend on a private backend, signer, or multisig
- Separate `this is centralized by design` from `this is insecure`
- If the frontend or backend can override safety-critical parameters, report that even if the contracts are sound
- Treat undisclosed trust assumptions as a product risk
- Treat unclear UI flows and wallet-signing confusion as product risk, not cosmetic polish
- AA claims require technical evidence; unsupported claims are `AA-READINESS GAP`
- AA is not a universal requirement; use `Not Applicable` when it is not part of the product path
- A 2026-readiness recommendation must include a benchmarked peer and an execution-level fix
- Product review is not a replacement for contract audit; it exists to make the audit sharper
