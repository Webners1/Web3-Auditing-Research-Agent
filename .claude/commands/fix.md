Load `skills/remediation-architect/SKILL.md`.

Takes existing audit findings and produces a concrete, implementation-ready fix plan. Answers not just "what is broken" but "how to fix it correctly, in what order, and with what tests."

**Argument:** $ARGUMENTS (optional — protocol name or path to audit report)

---

## What Runs

1. Reads findings from:
   - Most recent `audit-output/[project]-audit-*.md`
   - Or a file path if provided in $ARGUMENTS
2. For each finding, selects the best fix pattern from industry standards
3. Designs implementation steps, test requirements, and rollout sequence
4. Flags fixes that require upgrade, migration, or re-audit
5. Writes remediation plan to `audit-output/[project]-remediation-[YYYYMMDD].md`

---

## After Fix Planning

- To review upgrade implications: `/arch`
- For a client-ready PDF: `/report security`

---

## Usage Examples

```
/fix
/fix Aave v3
/fix audit-output/myprotocol-audit-20260413.md
```
