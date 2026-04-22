# web3-sales-agent

Stage-3 Web3 sales agent for a mandatory three-agent client-acquisition workflow.

## Required Order

```text
1. career-ops-source
   -> finds raw protocol leads
   -> writes web3-sales-agent/data/pipeline.md

2. web3-auditing-agent
   -> researches the queued protocol
   -> writes audit-output/*.md
   -> writes web3-sales-agent/data/research-handoffs/{slug}.md

3. web3-sales-agent
   -> reads the handoff + report
   -> writes the sales brief, pitch, proposal, and tracker updates
```

If stage 2 is missing, stage 3 must not pitch.

---

## What This Agent Does

| Feature | Description |
|---------|-------------|
| Sales brief generation | Converts stage-2 diligence into a stage-3 decision |
| Pitch generation | Drafts DMs, emails, and proposals from the research handoff |
| Queue processing | Processes only research-ready leads |
| Pipeline tracking | Tracks `Evaluated -> Pitched -> Responded -> Closed` |
| Follow-up support | Generates follow-up reminders and drafts |

---

## Key Files

| File | Role |
|------|------|
| `data/pipeline.md` | Shared raw lead inbox from stage 1 |
| `data/research-handoffs/` | Required stage-2 handoffs |
| `reports/` | Stage-3 sales briefs |
| `output/` | Pitch drafts and proposals |
| `data/leads.md` | Sales tracker |
| `service-profile.md` | Your services and proof |
| `modes/_profile.md` | Tone, pricing, objections |
| `templates/research-handoff-template.md` | Stage-2 handoff schema |

External dependencies:
- `../audit-output/*.md`
- `../career-ops-source/portals.yml`

---

## Quick Start

```bash
# 1. Fill in your seller profile
cp config/profile.example.yml config/profile.yml
cp modes/_profile.template.md modes/_profile.md

# 2. Add your credentials and proof
# edit service-profile.md

# 3. Verify the three-agent flow
node scripts/verify-pipeline.mjs
```

Then run the agents in order:

1. stage 1: `node ../career-ops-source/scan.mjs`
2. stage 2: use the main repo agent to research queued leads and write handoffs
3. stage 3: use `/web3-sales pipeline`, `/web3-sales evaluate [protocol]`, or `/web3-sales pitch [protocol]`

---

## Commands

```text
/web3-sales scan         -> trigger stage 1 lead discovery
/web3-sales evaluate     -> build a sales brief from a completed handoff
/web3-sales pitch        -> generate outreach from the handoff + report
/web3-sales compare      -> rank sales-ready leads
/web3-sales deep         -> pre-call brief
/web3-sales tracker      -> show pipeline status
/web3-sales pipeline     -> process research-ready queue items
/web3-sales batch        -> batch-process research-ready leads
/web3-sales patterns     -> analyze conversions
/web3-sales followup     -> generate follow-ups
```

Direct protocol input is allowed, but if no research handoff exists the agent should stop and send the workflow back to stage 2.

---

## Research Handoff Contract

Stage 2 must write one Markdown file per lead to:

```text
data/research-handoffs/{slug}.md
```

Required fields:
- `Protocol`
- `Slug`
- `Chain`
- `Bucket`
- `Lead Source`
- `Report Type`
- `Report Path`
- `Status: Research Complete`
- `Recommended Service`
- `Primary Pain`
- `Pitch Hook`
- `Proof Points To Use`
- `Cautions`

The template lives at:

```text
templates/research-handoff-template.md
```

---

## Verification

Run:

```bash
node scripts/verify-pipeline.mjs
```

It checks:
- required inbox and tracker files
- stage-1 config presence
- handoff directory and required fields
- linked stage-2 report paths
- pending tracker additions

---

## Credits

Original architecture inspiration: [career-ops](https://github.com/santifer/career-ops) by [santifer](https://santifer.io).

This workspace repurposes the pipeline into a three-agent Web3 lead -> research -> sales system.
