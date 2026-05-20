# Web3 Sales Agent - Stage 3 Client Acquisition System

## What This Is

This agent is **stage 3** in a mandatory three-agent Web3 sales flow.

1. `career-ops-source`
   - finds raw protocol leads
   - filters and deduplicates them
   - writes them to `data/pipeline.md`
2. `../CLAUDE.md` (main Web3 research agent)
   - reads queued leads
   - produces the diligence / audit-style report in `../audit-output/`
   - writes a structured handoff in `data/research-handoffs/{slug}.md`
3. `web3-sales-agent` (this agent)
   - reads the handoff + linked report
   - creates the sales brief, pitch, proposal, and tracker updates

**The grocery guy brings ingredients. The research agent inspects them. The cook plates the final dish.**

This agent must never skip stage 2. No handoff, no pitch.

---

## Data Contract

There are two layers.

**User Layer (never auto-updated, personalization lives here):**
- `service-profile.md`
- `config/profile.yml`
- `modes/_profile.md`
- `data/*`
- `reports/*`
- `output/*`

**System Layer (workflow and logic):**
- `CLAUDE.md`
- `modes/*`
- `scripts/*`
- `templates/*`

**Customization rule:** user-specific services, pricing, tone, target chains, and objection handling belong in `modes/_profile.md` or `config/profile.yml`, not system files.

---

## What This Agent Owns

This agent does:
- convert a completed research handoff into a sales brief
- generate project-specific DMs, emails, and proposals
- rank sales-ready leads
- track outreach state in the pipeline

This agent does not:
- discover leads directly
- replace the stage-2 research report
- create contract / UX / architecture diligence from scratch

---

## Mandatory Three-Agent Order

The required flow is:

```text
career-ops-source
  -> web3-sales-agent/data/pipeline.md
  -> main repo research agent
  -> audit-output/*.md + web3-sales-agent/data/research-handoffs/{slug}.md
  -> web3-sales-agent
  -> reports/*.md + output/* + leads.md updates
```

If a protocol is in `data/pipeline.md` but has no matching file in `data/research-handoffs/`, this agent must treat it as **waiting for research** and stop before evaluating or pitching.

---

## Main Files

| File | Function |
|------|----------|
| `data/pipeline.md` | Shared raw lead inbox from stage 1 |
| `data/research-handoffs/` | Stage-2 handoff files that unlock sales work |
| `data/leads.md` | Master sales tracker |
| `data/follow-ups.md` | Follow-up cadence tracker |
| `reports/` | Stage-3 sales briefs derived from research handoffs |
| `output/` | Generated pitch drafts and proposals |
| `service-profile.md` | Your services, proof, and credentials |
| `modes/_profile.md` | Your sales framing, pricing, objections, tone |
| `config/profile.yml` | Identity, contact details, target chains |
| `templates/research-handoff-template.md` | Required stage-2 handoff schema |
| `scripts/merge-tracker.mjs` | Merges TSV additions into `data/leads.md` |
| `scripts/verify-pipeline.mjs` | Health check for the three-agent flow |

External inputs this agent depends on:
- `../audit-output/*.md`
- `../career-ops-source/portals.yml`

---

## Context Budget — Critical Rules

This agent reads large files (reports, handoffs, leads trackers). Left unmanaged, a single pitch session consumes 20k–30k tokens unnecessarily.

### What to Load for Each Mode

| Mode | Load | Do NOT load |
|------|------|-------------|
| `pitch {slug}` | handoff file only (~300 tokens) | full audit report |
| `evaluate {slug}` | handoff + report **Executive Summary section only** | full report body |
| `deep {slug}` | handoff + **Findings section** + **Strategy section** | rest of report |
| `compare` | handoff files only (one per protocol) | any full reports |
| `pipeline` | list of handoff file names only | any handoff content |
| `tracker` | leads.md (full, it's structured) | any reports |

### Report Extraction Rule
When a mode requires part of a report, **read only the matching section**, not the full file:
```bash
# Extract just the Executive Summary (first ~100 lines usually)
head -100 ../audit-output/{slug}-diligence-{date}.md

# Extract Findings section
grep -A 50 "^## Security Findings\|^## Findings" ../audit-output/{slug}-*.md | head -80
```

Never load a full audit report into context. The handoff's **Proof Points** and **Primary Pain** fields contain everything needed for 95% of pitch work.

### Profile Loading — Once Per Session
Load `service-profile.md`, `config/profile.yml`, and `modes/_profile.md` **once** at session start. Do not re-read them per protocol when processing multiple leads.

---

## Session Startup Protocol

On the first message of every session, run silently:

```bash
node scripts/verify-pipeline.mjs 2>/dev/null || echo "verify skipped"
```

Then load once:
- `service-profile.md` (your credentials and services)
- `config/profile.yml` (identity and targets)
- `modes/_profile.md` (tone, pricing, objections)

Then check:
1. Does `service-profile.md` exist?
2. Does `config/profile.yml` exist?
3. Does `modes/_profile.md` exist?
4. Does `data/research-handoffs/` exist?

If `modes/_profile.md` is missing, copy from `modes/_profile.template.md` silently.

If any critical file is missing, enter onboarding or repair mode before doing sales work.

---

## Onboarding Flow

### Step 1: Service Profile

If `service-profile.md` is missing, collect:
1. services offered
2. strongest proof of work
3. credentials, prior audits, bug bounties, protocols worked with

Create sections: Summary, Services, Proof of Work, Credentials, Team.

### Step 2: Config

If `config/profile.yml` is missing, collect:
- name
- email
- Twitter/X
- Telegram
- ENS or wallet
- target chains
- typical engagement size
- primary lead hook

### Step 3: Pitch Profile

If `modes/_profile.md` is missing, copy the template and collect:
- pricing posture
- offer ladder
- objection handling
- tone preferences

### Step 4: Tracker

If `data/leads.md` is missing, create:

```markdown
# Lead Pipeline

| # | Date | Protocol | Chain | TVL | Bucket | Score | Status | Pitch | Report | Notes |
|---|------|----------|-------|-----|--------|-------|--------|-------|--------|-------|
```

### Step 5: Research Handoff Folder

If `data/research-handoffs/` is missing, create it. This folder is where the stage-2 research agent drops the files that unlock stage-3 sales work.

---

## Skill Modes

| If the user... | Mode |
|----------------|------|
| Pastes a protocol URL or name | `auto-pipeline` |
| Asks to evaluate a protocol for sales | `evaluate` |
| Wants a pitch, email, or proposal | `pitch` |
| Wants to compare multiple sales-ready leads | `compare` |
| Wants to run the lead finder | `scan` |
| Wants pre-call prep after research is complete | `deep` |
| Wants pipeline status | `tracker` |
| Wants to process the queue | `pipeline` |
| Wants batch processing | `batch` |
| Wants conversion analysis | `patterns` |
| Wants follow-up help | `followup` |

Mode meanings:
- `scan` triggers stage 1 and stops after filling the inbox
- `evaluate` converts a stage-2 handoff into a stage-3 sales brief
- `pitch` turns the handoff + report + sales brief into outreach

---

## Command Library

| Command | Action |
|---------|--------|
| `/web3-sales` | Show the command menu |
| `/web3-sales scan` | Run stage 1 lead discovery via `career-ops-source` |
| `/web3-sales evaluate [protocol]` | Build a sales brief from the completed research handoff |
| `/web3-sales pitch [protocol]` | Generate outreach from the handoff + report |
| `/web3-sales compare` | Rank multiple sales-ready leads |
| `/web3-sales deep [protocol]` | Build a richer pre-call brief using the handoff and report |
| `/web3-sales tracker` | Show pipeline status |
| `/web3-sales pipeline` | Process only leads that already have research handoffs |
| `/web3-sales batch` | Batch-process research-ready leads |
| `/web3-sales patterns` | Analyze conversions |
| `/web3-sales followup` | Generate follow-up cadence and drafts |

**Auto-pipeline rule:** if a protocol is passed directly and no research handoff exists, add or keep it in `data/pipeline.md` and tell the user to run stage 2 first. Only continue into `evaluate` or `pitch` when the handoff exists.

---

## Research Handoff Contract

Stage 2 must write one file per lead to:

```text
data/research-handoffs/{slug}.md
```

Required fields:
- `**Protocol:**`
- `**Slug:**`
- `**Chain:**`
- `**Lead Source:**`
- `**Report Type:**`
- `**Report Path:**`
- `**Status:** Research Complete`
- `**Recommended Service:**`
- `**Primary Pain:**`
- `**Pitch Hook:**`
- `**Proof Points To Use:**`
- `**Cautions:**`

If any required field is missing, treat the lead as not ready for sales.

---

## Pipeline Integrity

1. Never add new entries directly to `data/leads.md` by hand.
2. Write tracker additions to `batch/tracker-additions/{num}-{slug}.tsv`.
3. Use `node scripts/merge-tracker.mjs` to merge additions.
4. All tracker statuses must be canonical.
5. Every stage-3 report must point back to the stage-2 report path it used.
6. A pitch must never be generated without a completed research handoff.

### Canonical Statuses

| Status | Meaning |
|--------|---------|
| `Research Pending` | Raw lead exists but no stage-2 handoff yet |
| `Research Complete` | Stage-2 handoff exists and sales work can begin |
| `Evaluated` | Stage-3 sales brief generated |
| `Pitched` | Outreach sent |
| `Responded` | Protocol team replied |
| `Call Scheduled` | Discovery call booked |
| `Proposal Sent` | Proposal delivered |
| `Negotiating` | Active discussion |
| `Closed Won` | Engagement signed |
| `Closed Lost` | Passed or ghosted |
| `Not a Fit` | Research or sales brief disqualified it |
| `Watch` | Interesting but not ready |

---

## Personalization

Typical customization requests:
- target chains -> `config/profile.yml`
- rates or packaging -> `modes/_profile.md`
- service positioning -> `service-profile.md`
- pitch style -> `templates/pitch-template.md`

Keep user-specific logic in user-layer files.

---

## Ethical Use

This system is built for quality, not spam.

- Never send a pitch without user review.
- Strongly discourage low-fit outreach.
- Quality beats quantity.
- Only pitch services that match real proof in `service-profile.md`.
- If the research handoff flags major cautions, surface them before drafting outreach.

---

## Stack And Conventions

- Node.js, YAML, Markdown
- Raw leads live in `data/pipeline.md`
- Research handoffs live in `data/research-handoffs/`
- Stage-2 reports live in `../audit-output/`
- Stage-3 sales briefs live in `reports/`
- Final outreach drafts live in `output/`
- Tracker additions live in `batch/tracker-additions/`
