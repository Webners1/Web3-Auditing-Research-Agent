# Research Handoff Template

Stage 2 writes one file per protocol to:

```text
data/research-handoffs/{slug}.md
```

Use this structure:

```markdown
**Protocol:** [Protocol Name]
**Slug:** [protocol-slug]
**Chain:** [Primary chain]
**Bucket:** [Ghost Lead / Leaky Bucket / Security Risk / Chain Migrator]
**Lead Source:** data/pipeline.md
**Report Type:** [diligence / audit / product / arch / strategy]
**Report Path:** ../audit-output/[report-file].md
**Status:** Research Complete
**Recommended Service:** [Best-fit service]
**Primary Pain:** [The problem that justifies outreach]
**Pitch Hook:** [One sentence opening hook for stage 3]
**Proof Points To Use:** [1-2 proof points from the seller profile]
**Cautions:** [Budget risk, anonymous team, weak urgency, reputational risk, etc.]
```

Rules:
- `Report Path` must point to a real Markdown file in `../audit-output/`
- `Status` must be exactly `Research Complete`
- `Cautions` must not be omitted; write `None` if there are no material cautions
- Stage 3 may refuse to pitch if required fields are missing
