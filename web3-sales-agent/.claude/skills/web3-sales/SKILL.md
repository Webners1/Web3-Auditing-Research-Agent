---
name: web3-sales
description: Stage-3 Web3 sales agent - consume completed research handoffs, generate sales briefs, write pitches, and track outreach
user_invocable: true
args: mode
argument-hint: "[scan | evaluate | compare | pitch | deep | tracker | pipeline | batch | patterns | followup]"
---

# web3-sales - Router

## Mode Routing

Determine the mode from `{{mode}}`:

| Input | Mode |
|-------|------|
| (empty / no args) | `discovery` |
| Protocol URL, name, or address | `auto-pipeline` |
| `scan` | `scan` |
| `evaluate` | `evaluate` |
| `compare` | `compare` |
| `pitch` | `pitch` |
| `deep` | `deep` |
| `tracker` | `tracker` |
| `pipeline` | `pipeline` |
| `batch` | `batch` |
| `patterns` | `patterns` |
| `followup` | `followup` |

If `{{mode}}` does not match a sub-command and does not look like a protocol, show discovery.

---

## Discovery Mode

Show:

```text
web3-sales - Stage 3 Sales Agent

Required order:
  1. career-ops-source finds leads
  2. main repo research agent writes the report + handoff
  3. web3-sales generates the sales brief and pitch

Available commands:
  /web3-sales scan         -> run stage 1 lead discovery
  /web3-sales evaluate     -> build a sales brief from a completed research handoff
  /web3-sales pitch        -> generate outreach from the handoff + report
  /web3-sales compare      -> rank multiple sales-ready leads
  /web3-sales deep         -> pre-call research brief
  /web3-sales tracker      -> pipeline status overview
  /web3-sales pipeline     -> process research-ready queue items
  /web3-sales batch        -> batch-process research-ready leads
  /web3-sales patterns     -> analyze conversion patterns
  /web3-sales followup     -> generate follow-ups

Shared inbox:
  web3-sales-agent/data/pipeline.md

Research handoffs:
  web3-sales-agent/data/research-handoffs/{slug}.md
```

---

## Context Loading

### Modes that require shared sales context

Read:
- `modes/_shared.md`
- `modes/_profile.md`
- `modes/{mode}.md`

Applies to:
- `auto-pipeline`
- `evaluate`
- `compare`
- `pitch`
- `scan`
- `pipeline`
- `batch`

### Standalone modes

Read only:
- `modes/{mode}.md`

Applies to:
- `tracker`
- `deep`
- `patterns`
- `followup`

---

## Scan Mode

`scan` belongs to stage 1.

Run:

```bash
node ../career-ops-source/scan.mjs
```

Then:
1. read `data/pipeline.md`
2. surface the newly-added raw leads
3. remind the user that stage 2 must run before this agent can pitch

Do not evaluate or pitch directly from `scan`.

---

## Auto-Pipeline Mode

When a protocol URL, name, or address is passed directly:

1. Check whether a matching handoff exists in `data/research-handoffs/`
2. If the handoff exists:
   - run `evaluate`
   - if the resulting score is strong enough, offer `pitch`
3. If the handoff does not exist:
   - ensure the lead is present in `data/pipeline.md`
   - stop and tell the user to run stage 2 with the main repo agent

The sales agent must never replace stage 2.

---

## Stage-2 Handoff Requirement

Before running `evaluate`, `pitch`, `pipeline`, or `batch`, check for:

```text
data/research-handoffs/{slug}.md
```

The handoff must include:
- `**Protocol:**`
- `**Slug:**`
- `**Chain:**`
- `**Report Type:**`
- `**Report Path:**`
- `**Status:** Research Complete`
- `**Recommended Service:**`
- `**Primary Pain:**`
- `**Pitch Hook:**`
- `**Proof Points To Use:**`
- `**Cautions:**`

If the handoff is missing or incomplete, do not continue into sales work.

---

## Expected Outputs

Stage 3 produces:
- `reports/{NUM}-{slug}-{YYYY-MM-DD}.md` - sales brief
- `output/{slug}-pitch-{YYYY-MM-DD}.md` - pitch draft if requested
- `batch/tracker-additions/{NUM}-{slug}.tsv` - tracker addition

Stage 3 consumes:
- `data/pipeline.md`
- `data/research-handoffs/{slug}.md`
- `../audit-output/*.md`

---

## Guardrails

- Never generate outreach without the stage-2 handoff.
- Never claim stage-3 scoring came from fresh diligence if it came from the stage-2 report.
- Never send a pitch automatically.
- When uncertain, prefer stopping and pointing back to the missing stage.
