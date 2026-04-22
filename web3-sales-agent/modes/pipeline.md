# Mode: pipeline - Research-Gated Sales Queue

Process the shared inbox in the required order:

1. Stage 1 writes raw leads to `data/pipeline.md`
2. Stage 2 writes handoffs to `data/research-handoffs/`
3. Stage 3 processes only the research-ready leads

---

## Workflow

1. Read `data/pipeline.md`
2. Find all items marked `- [ ]` in the `Pending` section
3. For each pending item:
   - identify the protocol slug or best-match name
   - check whether `data/research-handoffs/{slug}.md` exists
4. Split the queue into:
   - `Research Ready`
   - `Waiting For Research`
5. Only run `evaluate` for the `Research Ready` set
6. Leave `Waiting For Research` items untouched in `Pending`
7. After each completed evaluation:
   - write the stage-3 sales brief
   - write the tracker TSV addition
   - if appropriate, offer to continue into `pitch`

---

## Handoff Rule

A lead is `Research Ready` only if:
- a matching handoff file exists
- the handoff says `**Status:** Research Complete`
- the linked report path exists

If any of those fail, the lead is not ready for stage 3.

---

## Queue Summary Output

After scanning the queue, show:

```markdown
## Pipeline Status

### Research Ready
| Protocol | Chain | Handoff | Action |
|----------|-------|---------|--------|

### Waiting For Research
| Protocol | Chain | Reason |
|----------|-------|--------|
```

If everything is waiting on stage 2, say so explicitly and stop.

---

## Processed Line Format

When a lead has completed stage 3 evaluation, move it to `Processed` as:

```text
- [x] #NNN | {protocol} | {chain} | {bucket} | {score}/5 | Research report: {report-path} | Pitch ❌
```

Do not mark an item processed until stage 3 evaluation is actually complete.

---

## Batch Threshold

If there are 3 or more `Research Ready` items, batch them.

Each worker should receive:
- `modes/_shared.md`
- `modes/_profile.md`
- `modes/evaluate.md`
- the specific handoff file path

Never send raw pending items without handoffs to a batch worker.

---

## Notes

- `Pending` is the shared inbox, not proof of sales readiness.
- The presence of a protocol in `data/pipeline.md` does not mean it can be pitched yet.
- Stage 3 should help the user see which leads are blocked on stage 2.
