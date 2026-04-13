# Web3 Remediation Architect

Acts like a senior blockchain engineer after an audit. Takes findings, explains the real root causes, chooses the best fix according to industry-standard patterns, and turns the result into an implementation and rollout plan. This skill exists to answer `how should we fix this correctly`, not just `what is broken`.

**Trigger phrases:** `how do we fix this finding`, `best solution for this audit issue`, `remediation plan`, `patch strategy`, `fix these vulnerabilities`, `engineering response`, `industry standard fix`

---

## Execution Pipeline

### Phase 1 - Ingest Findings and Constraints

Read:
- Audit findings
- Product report if available
- Architecture report if available
- Upgradeability constraints
- Chain and protocol constraints

For each finding, capture:
1. Exploit path
2. Root cause
3. Impacted invariant
4. Whether the fix touches storage, math, roles, external integrations, or user flows

### Phase 2 - Fix Selection

Load `references/fix-patterns.md`.

For each finding, produce:
- Preferred fix
- Acceptable alternative fix
- Why the preferred fix is safer
- What new risks the fix introduces
- Why this fix fits this protocol's current stack, team capacity, and upgrade constraints

Always benchmark against known patterns from:
- OpenZeppelin
- Aave
- Uniswap
- Compound
- Morpho

If a finding changes upgradeability or storage layout, also consult:
- `skills/arch-advisor/references/upgrade-patterns.md`

### Phase 3 - Implementation Design

Translate the preferred fix into engineering work:
1. Files and modules to change
2. Test cases to add
3. Migration or upgrade steps
4. Monitoring or circuit-breaker changes
5. Re-audit scope after the patch
6. Rollback and contingency path if rollout fails

Estimate each fix:
- `HOTFIX`
- `SHORT SPRINT`
- `MULTI-SPRINT`

### Phase 4 - Verification Plan

For every finding, specify:
- Unit tests
- Integration tests
- Invariant or fuzz tests
- Manual review points
- Deployment checks

For every CRITICAL/HIGH finding, include a detailed fix packet:
- Implementation diff outline (storage impact, access-control impact, external-call impact)
- One alternative architecture path and trade-offs
- Sequencing dependencies across teams/contracts
- Success criteria and post-deploy verification signals

### Phase 5 - Output

Write the remediation plan using `references/report-format.md`:

```
audit-output/[project-name]-remediation-[YYYYMMDD].md
```

---

## Remediation Rules

- Do not recommend generic fixes without checking protocol-specific side effects
- A fix is incomplete if it lacks a regression test plan
- If the safest fix is operational rather than code-level, say so explicitly
- If a hotfix creates long-term architecture debt, record the follow-up work
- Prefer fixes that reduce privileged trust, not just exploitability
- Do not recommend one-size-fits-all patterns; select fixes by protocol fit, not protocol fame
