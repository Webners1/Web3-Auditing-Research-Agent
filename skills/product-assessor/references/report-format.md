# Product Review Report Format

## File Naming

```
audit-output/[project-name]-product-[YYYYMMDD].md
```

---

## Report Structure

```markdown
# Product Review - [Project Name]

| Field | Value |
|-------|-------|
| Date | YYYY-MM-DD |
| Reviewer | Web3 Auditing Agent |
| Product stage | Idea / Testnet / Mainnet / Mature |
| Chains | [Detected] |

## Executive Summary
[2-4 sentences on the product, trust model, and biggest non-contract risks]

## Product Snapshot
| Area | Score | Notes |
|------|-------|-------|
| Product clarity | 1-5 | |
| User safety | 1-5 | |
| App flow and UX maturity | 1-5 | |
| Smart wallet / AA readiness | 1-5 / N/A | |
| Offchain trust minimization | 1-5 | |
| Governance maturity | 1-5 | |
| Smart contract quality signals | 1-5 | |
| Docs / GitHub / presentation quality | 1-5 | |
| Business model clarity | 1-5 | |

## What The Product Does
[Short plain-language explanation]

## System Map
[Frontend, contracts, backend, oracles, relayers, multisigs, bridges]

## Trust Boundaries
| Boundary | Why it exists | User impact |
|----------|---------------|-------------|
| Frontend config | | |
| Multisig control | | |
| Oracle dependency | | |

## UX Flow Audit Summary
[One primary flow walkthrough, one failure-path walkthrough, click/decision cost, and top friction points]

## Smart Wallet and AA Readiness
_Fill this section only if applicable to the product path. Otherwise mark `Not Applicable` and explain why in one sentence._

| Capability | Status | Evidence | Gap |
|------------|--------|----------|-----|
| ERC-4337 support | Yes/No/Partial | | |
| Bundler dependency handling | Yes/No/Partial | | |
| Paymaster sponsorship policy | Yes/No/Partial | | |
| Session-key guardrails | Yes/No/Partial | | |
| EIP-1271 compatibility | Yes/No/Partial | | |

## Non-Contract Risk Register
| Category | Severity | Issue | Recommendation |
|----------|----------|-------|----------------|
| PRODUCT-RISK | High | | |
| OPS-RISK | Medium | | |
| UX-FRICTION | High/Medium/Low | | |
| AA-READINESS GAP | High/Medium/Low | | |
| MARKET-READINESS GAP | High/Medium/Low | | |

## 2026 Web3 Market-Readiness Scorecard
| Dimension | Score | Evidence | Priority Fix |
|-----------|-------|----------|--------------|
| UI/UX execution and failure recovery | 1-5 | | |
| Security posture and operational resilience | 1-5 | | |
| Smart contract engineering maturity | 1-5 | | |
| Docs/GitHub/presentation readiness | 1-5 | | |
| Product clarity and category narrative | 1-5 | | |
| Business durability and future relevance | 1-5 | | |
| Comparative stack competitiveness | 1-5 | | |

## Comparative Stack Analysis
| Capability | Current implementation | Best function-matched peer | One-curve-ahead peer | Gap impact | Recommended upgrade |
|------------|------------------------|----------------------------|----------------------|------------|---------------------|
| | | | | | |

For each major gap, explain why the chosen peer is the right benchmark and what would make that upgrade fit this specific protocol.

## Contract Inventory
- [Core contract]
- [Periphery contract]
- [External dependency]

## Recommended Audit Scope
[What should move into the smart contract audit and what should stay out]

## Founder Questions
1. [Open question]
2. [Open question]
3. [Open question]

## Sources
- [Exact URL]
- [Exact URL]
```
