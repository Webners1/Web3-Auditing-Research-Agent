# Architecture Advisory Report Format

## File Naming

```
audit-output/[project-name]-arch-[YYYYMMDD].md
```

---

## Report Structure

```markdown
# Architecture Advisory - [Protocol Name]

| Field | Value |
|-------|-------|
| Date | YYYY-MM-DD |
| Reviewer | Web3 Auditing Agent |
| Framework | Foundry / Hardhat / [detected] |
| Contracts | N files, ~XXXX LOC |
| Protocol Type | AMM / Lending / Staking / [detected] |

## Executive Summary
[3-5 sentences on current architecture quality, key structural risks, and top recommendations]

## Protocol Overview
[What this protocol does, current architecture in 3-5 sentences]

## Architecture Diagram
[ASCII or text representation of the major components and trust boundaries]

## Gap Analysis Summary
| Priority | Category | Gap | Impact |
|----------|----------|-----|--------|
| URGENT | Upgradeability | No proxy pattern | Cannot fix critical bugs post-deployment |
| HIGH | Oracle | Spot price from AMM | Flash loan price manipulation |

## Detailed Recommendations
[Per-gap sections]

## Technical Roadmap
### Phase 1 - Security and Access Control
[Tasks]

### Phase 2 - Upgradeability
[Tasks]

### Phase 3 - Integrations and Composability
[Tasks]

### Phase 4 - Chain and Expansion Strategy
[Tasks]

## Trade-Offs and Complexity Costs
[What these recommendations cost in engineering time, gas, and operational burden]

## Sources
- [Exact URL]
- [Exact URL]
```
