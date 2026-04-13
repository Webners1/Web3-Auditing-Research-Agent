---
name: protocol-diligence
description: End-to-end Web3 diligence orchestrator spanning product, audit, remediation, architecture, strategy, UX, and AA readiness.
---

# Web3 Protocol Diligence Orchestrator

Runs the full engagement flow for a Web3 product: product review, contract discovery, smart contract audit, remediation planning, architecture review, and CEO-level strategy. Use this when the user wants an end-to-end assessment rather than a single audit pass.

**Trigger phrases:** `full protocol diligence`, `review this web3 product end to end`, `full stack web3 review`, `complete protocol review`, `founder mode`, `investor diligence`, `full audit and strategy`, `full product and ux audit`, `business and smart wallet readiness review`

---

## End-to-End Flow

Run these phases in order. Skip only when a phase is clearly not applicable.

### Phase 1 - Product Surface Review

Load `references/research-source-registry.md` first so the workflow stays inside the approved Web3 research path before expanding outward.

Run `skills/product-assessor/SKILL.md` first.

Goal:
- Understand what the product does before judging the contracts
- Map frontend, backend, relayers, indexers, oracles, bridges, multisigs, admin keys, and user journeys
- Evaluate one primary user workflow and one failure-path workflow for UX friction and recovery behavior
- Check wallet model and account-abstraction readiness only when smart-wallet behavior is part of the product path
- Build a 2026-readiness baseline across UX, security, contract quality, docs/GitHub quality, and business clarity
- Discover smart contract addresses, repositories, and trust boundaries

If installed, use `ux-audit` for the user-flow pass and `account-abstraction` for ERC-4337/smart-wallet checks.

Primary output:
- `audit-output/[project]-product-[YYYYMMDD].md`

### Phase 2 - Contract Discovery and Scope

From the product review:
1. Identify the contracts that actually power the product
2. Separate core contracts, periphery contracts, interfaces, mocks, and vendor code
3. Record deployment addresses and chain targets if available
4. Capture invariants and critical user flows for the audit handoff

If companion skills are installed, `x-ray` from pashov is the preferred pre-audit mapper.

### Phase 3 - Smart Contract Security Audit

Run `skills/web3-audit/SKILL.md`.

Goal:
- Execute the full static-analysis plus multi-agent audit pipeline
- Produce validated findings with exploit paths, severities, and fixes

Primary output:
- `audit-output/[project]-audit-[YYYYMMDD].md`

### Phase 4 - Remediation Engineering

Run `skills/remediation-architect/SKILL.md`.

Goal:
- Turn findings into implementation-ready fixes
- Benchmark fix patterns against industry-standard designs
- Define tests, rollout sequence, and re-audit requirements

Primary output:
- `audit-output/[project]-remediation-[YYYYMMDD].md`

### Phase 5 - Architecture Advisory

Run `skills/arch-advisor/SKILL.md`.

Goal:
- Improve scalability, upgradeability, composability, and operational resilience
- Recommend the right architecture for the protocol stage and product goals

Primary output:
- `audit-output/[project]-arch-[YYYYMMDD].md`

### Phase 6 - CEO / Market Strategy

Run `skills/ceo-advisor/SKILL.md`.

Goal:
- Benchmark the product against current market direction
- Recommend which opportunities to pursue, defer, or avoid
- Translate technical capability into business positioning
- Build a function-matched comparable set, including one one-curve-ahead benchmark
- Evaluate competitive stack quality and document what must be upgraded to be 2026 market-ready

If installed, use `positioning-canvas` and `marketing-strategy-pmm` to structure strategy and narrative sections.

Primary output:
- `audit-output/[project]-strategy-[YYYYMMDD].md`

### Phase 7 - Executive Package

Combine the outputs above into a single executive summary using `references/report-format.md`.

Write:
- `audit-output/[project]-diligence-[YYYYMMDD].md`

The combined report should answer:
1. What does the product do?
2. Where are the biggest technical and business risks?
3. What should be fixed immediately?
4. What should be built next?
5. Which strategy best matches current market conditions?
6. Can a user complete core workflows with low friction and high trust?
7. Is the product 2026 market-ready across UX, security, contracts, docs/GitHub, and business execution?
8. If AA is applicable, is the product operationally ready for smart-wallet/account-abstraction expectations?

Then hand off to `skills/client-reporting/SKILL.md` to export the final Markdown deliverable to HTML and PDF.

---

## Operating Rules

- Do not start with contract findings if the product itself is not yet understood
- Do not start with generic web search if the answer can be obtained from official project sources, the source registry, or approved explorer/data sources
- Do not give market or trend advice from memory alone; verify with live sources in the CEO phase
- Keep product risk, contract risk, architecture debt, and market advice clearly separated
- Keep UX friction explicit in both product and strategy sections
- Treat smart-wallet/AA readiness as conditional, not universal, and mark `Not Applicable` when out of scope
- Every final recommendation must include both upside and cost
- Comparable sets must be function-matched and include rationale; avoid generic blue-chip lists
- Include 2026 market-readiness metrics and comparative stack evidence in final recommendations
- If the project is pre-launch, bias toward architecture and execution readiness
- If the project is live, bias toward risk reduction, migration safety, and incident response
