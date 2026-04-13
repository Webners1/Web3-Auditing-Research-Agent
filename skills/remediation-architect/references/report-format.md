# Remediation Report Format

## File Naming

```
audit-output/[project-name]-remediation-[YYYYMMDD].md
```

---

## Report Structure

```markdown
# Remediation Plan - [Project Name]

| Field | Value |
|-------|-------|
| Date | YYYY-MM-DD |
| Source audit | [Audit report name] |
| Reviewer | Web3 Auditing Agent |

## Executive Summary
[How hard the fix set is, what can be hotfixed, what needs deeper redesign]

## Prioritized Fix Queue
| Priority | Finding | Preferred fix | Effort | Rollout risk |
|----------|---------|---------------|--------|--------------|
| HOTFIX | | | | |
| SHORT SPRINT | | | | |

## Finding-by-Finding Plan
### [Finding Title]
**Root Cause:** [One sentence]
**Preferred Fix:** [Specific change]
**Alternative Fix:** [If relevant]
**Why This Is Best:** [Short rationale]
**Why It Fits This Protocol:** [Stack fit, upgrade constraints, and execution capacity]
**Tests Required:** [Unit / integration / invariant]
**Rollout Notes:** [Upgrade, migration, comms, monitoring]

For every CRITICAL/HIGH finding, add this subsection:

### Deep Fix Packet — [Finding Title]
**Implementation Scope:** [Contracts/modules/storage touched]
**Design Trade-offs:** [Security gain vs complexity/gas/ops cost]
**Alternative Path Decision:** [What was considered and why rejected]
**Sequencing Dependencies:** [What must ship first]
**Rollback Plan:** [How to revert safely if rollout fails]
**Post-Deploy Verification:** [On-chain and ops checks]

## Shared Refactors
[Common changes that solve multiple findings]

## Comparative Fix Benchmarking
| Finding | Chosen fix pattern | Benchmark protocol/pattern | Why this benchmark fits | Notes |
|---------|--------------------|-----------------------------|-------------------------|-------|
| | | | | |

## Re-Audit Scope
[What must be re-reviewed after implementation]

## Suggested Execution Order
1. [First]
2. [Second]
3. [Third]
```
