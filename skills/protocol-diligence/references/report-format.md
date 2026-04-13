# Full Diligence Report Format

## File Naming

```
audit-output/[project-name]-diligence-[YYYYMMDD].md
```

---

## Report Structure

```markdown
# Web3 Protocol Diligence - [Project Name]

| Field | Value |
|-------|-------|
| Date | YYYY-MM-DD |
| Reviewer | Web3 Auditing Agent |
| Scope | Product, contracts, architecture, strategy |
| Chains | [Detected chains] |
| Repositories | [Reviewed repos or links] |

## Executive Verdict
[3-5 sentences on product quality, security posture, execution maturity, and strategic position]

## Snapshot
| Area | Status | Notes |
|------|--------|-------|
| Product clarity | Strong / Mixed / Weak | |
| App flow and UX maturity | Strong / Mixed / Weak | |
| Smart wallet / AA readiness | Strong / Mixed / Weak / N/A | |
| Offchain trust model | Strong / Mixed / Weak | |
| Contract security | Strong / Mixed / Weak | |
| Upgrade readiness | Strong / Mixed / Weak | |
| Smart contract quality maturity | Strong / Mixed / Weak | |
| Docs / GitHub / presentation readiness | Strong / Mixed / Weak | |
| Market positioning | Strong / Mixed / Weak | |

## What The Product Is
[Short explanation of the product, users, chains, and core flows]

## Top Risks
1. [Highest risk]
2. [Second risk]
3. [Third risk]

## Top Opportunities
1. [Highest upside move]
2. [Second upside move]
3. [Third upside move]

## Product Review Summary
[Key points from product report]

## UX and Wallet Flow Summary
[Primary workflow pass, failure-path behavior, and highest-friction checkpoints]

## Smart Wallet / Account Abstraction Readiness Summary
[Include only if applicable. If not applicable, write `Not Applicable` with rationale. For applicable products summarize EOA vs smart-account posture, sponsorship model, bundler/paymaster dependency, and operational gaps.]

## 2026 Web3 Market-Readiness Scorecard
| Dimension | Status | Evidence | Priority Upgrade |
|-----------|--------|----------|------------------|
| UI/UX and flow resilience | Strong / Mixed / Weak | | |
| Security posture and incident readiness | Strong / Mixed / Weak | | |
| Smart contract engineering quality | Strong / Mixed / Weak | | |
| Docs/GitHub/presentation quality | Strong / Mixed / Weak | | |
| Product clarity and narrative fitness | Strong / Mixed / Weak | | |
| Business durability and future fit | Strong / Mixed / Weak | | |
| Stack competitiveness | Strong / Mixed / Weak | | |

## Audit Summary
[Key points from smart contract audit]

## Remediation Summary
[Key points from remediation report]

## Architecture Summary
[Key points from architecture report]

## CEO Strategy Summary
[Key points from strategy report]

## Positioning and Comparable Strategy Summary
[Function-matched comparable set, one-curve-ahead benchmark, and what this changes in roadmap sequencing]

## Comparative Stack Deep Dive
| Stack Area | Current state | Function-matched best reference | One-curve-ahead reference | Gap impact | Recommended fix path |
|------------|---------------|----------------------------------|---------------------------|------------|----------------------|
| | | | | | |

For the top three gaps, include implementation detail level sufficient for engineering kickoff (affected modules, complexity, sequencing, and validation).

## 30 / 60 / 90 Day Plan
### 0-30 Days
[Critical fixes and decisions]

### 31-60 Days
[Architecture and launch hardening]

### 61-90 Days
[Growth, integrations, and market moves]

## Recommended Engagement Sequence
1. [Immediate]
2. [Next]
3. [Then]

## Sources
- [Exact URL]
- [Exact URL]
```
