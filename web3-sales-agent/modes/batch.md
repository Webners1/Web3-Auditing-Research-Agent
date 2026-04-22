# Mode: batch - Batch Process Research-Ready Leads

Use batch mode only for leads that already completed stage 2.

---

## When To Use

After stage 2 has produced handoffs for 5 or more queued leads, use batch mode to create multiple stage-3 sales briefs efficiently.

---

## Workflow

1. Read `data/pipeline.md`
2. Match pending items against `data/research-handoffs/`
3. Build the `Research Ready` set
4. Launch workers only for that set
5. Each worker runs `modes/evaluate.md` using the specific handoff file
6. Collect reports and TSV additions
7. Run `node scripts/merge-tracker.mjs`

Do not batch raw leads that are still waiting on research.

---

## Worker Prompt Template

Each worker receives:

```text
[content of modes/_shared.md]

[content of modes/_profile.md]

[content of modes/evaluate.md]

Evaluate this research-ready lead for stage-3 sales:
Handoff: data/research-handoffs/{slug}.md
Report number: {NUM}
Date: {TODAY}
```

Expected outputs:
1. `reports/{NUM}-{slug}-{TODAY}.md`
2. `batch/tracker-additions/{NUM}-{slug}.tsv`

---

## Batch Summary

After all workers complete, show:

```markdown
## Batch Sales Briefs Complete - {DATE}

| # | Protocol | Chain | Bucket | Score | Verdict | Next Step |
|---|----------|-------|--------|-------|---------|-----------|
```

Then remind the user to merge tracker additions.
