Load `skills/web3-audit/SKILL.md`.
Load `skills/remediation-architect/SKILL.md`.

Expands the security audit with deeper major-issue analysis and implementation-grade fix architecture.

**Argument:** $ARGUMENTS (optional — protocol name, finding ID, or audit report path)

---

## What Runs

1. Resolve target audit report:
   - Use provided file path if supplied
   - Otherwise use latest `audit-output/[project]-audit-[YYYYMMDD].md`
2. Select focus set:
   - Requested finding IDs (if supplied)
   - Otherwise all CRITICAL/HIGH findings
3. For each finding, produce a deep-fix packet:
   - Revalidated exploit sequence and impacted invariant
   - Preferred fix and at least one viable alternative
   - Why preferred fix fits this protocol stack and upgrade constraints
   - Implementation scope (contracts/modules/storage surfaces)
   - Test matrix (unit/integration/invariant/fuzz)
   - Rollout + rollback plan
4. Benchmark each fix choice against named protocol patterns and explain fit
5. Write output to `audit-output/[project]-security-expand-[YYYYMMDD].md`

---

## Output Guidance

- Focus on actionable engineering detail, not severity restatement
- Include sequence dependencies when fixes touch multiple contracts
- Flag where external re-audit is mandatory before production rollout

---

## Usage Examples

```
/expand-security-audit
/expand-security-audit mars-poolin
/expand-security-audit M-02
/expand-security-audit audit-output/mars-poolin-audit-20260413.md
```
