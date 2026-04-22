# Mode: scan - Trigger Stage 1 Discovery

This mode belongs to stage 1 of the three-agent pipeline.

Its job inside the sales agent is only to trigger the lead finder and show what entered the inbox.

---

## Workflow

1. Run the stage-1 scanner:

```bash
node ../career-ops-source/scan.mjs
```

2. Read `data/pipeline.md`
3. Surface the newly-added raw leads
4. Stop and remind the user:
   - stage 2 must now run from the main repo
   - stage 3 cannot pitch until a research handoff exists

---

## Output

Show:

```markdown
## Scan Complete

New raw leads were added to `data/pipeline.md`.

Next required step:
1. Run `/sales-research-pipeline` from the main repo
2. Wait for `data/research-handoffs/{slug}.md`
3. Return here for `/web3-sales pipeline` or `/web3-sales pitch`
```

Do not continue into evaluation or pitching from `scan`.
