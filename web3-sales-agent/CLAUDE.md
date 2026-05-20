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
- `pitch` runs Insight Extraction → then generates the outreach email
- `draft` creates the Gmail draft from the extracted insight email only

---

## Command Library

| Command | Action |
|---------|--------|
| `/web3-sales` | Show the command menu |
| `/web3-sales scan` | Run stage 1 lead discovery via `career-ops-source` |
| `/web3-sales evaluate [protocol]` | Build a sales brief from the completed research handoff |
| `/web3-sales pitch [protocol]` | Generate outreach from the handoff + report |
| `/web3-sales draft [protocol]` | Create Gmail draft for a pitch-ready lead |
| `/web3-sales inbox` | Check Gmail for replies from protocol teams |
| `/web3-sales label-setup` | Create Web3 Rabbit Gmail labels (one-time setup) |
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

## Insight Extraction — Mandatory Step Before Any Email

The full diligence report and handoff are **internal state only**. They are never attached, quoted, or summarised in outbound email. Before generating any outreach, run this extraction step.

### Step 1 — Select One Finding

Read the handoff's `**Proof Points To Use:**` and `**Primary Pain:**` fields only (not the full report). Apply this filter to select exactly ONE finding:

| Criterion | Rule |
|-----------|------|
| Impact | Must be directly tied to money, users, or protocol continuity |
| Non-obvious | Not "update dependencies" or "add comments" — something they wouldn't catch without knowing where to look |
| Specific | Tied to a named contract, mechanism, or integration — not a category of risk |
| Provable | You can point to it without guessing |

If the handoff has a CRITICAL or HIGH finding, always select it. If all findings are MEDIUM or LOW, select the one with the most concrete business consequence.

### Step 2 — Translate to Business Risk

Map the technical finding to the protocol's specific business model. Use this mapping table:

| Protocol Type | Technical Class | Business Risk Translation |
|---------------|----------------|--------------------------|
| DeFi / Lending | Reentrancy, access control | "liquidity pool drained in a single transaction" |
| DeFi / Lending | Oracle manipulation | "collateral mispriced — bad debt accumulates silently" |
| Derivatives / Perps | Missing circuit breaker | "leveraged positions wiped during a normal volatility event" |
| Derivatives / Perps | Keeper / oracle staleness | "pool balances corrupted during network downtime — impossible to unwind cleanly" |
| DEX / AMM | Price manipulation | "LP positions sandwiched at scale — liquidity exits" |
| Bridge | Replay / double-spend | "cross-chain assets locked or minted twice" |
| NFT / Gaming | Minting exploit | "token supply broken — floor price collapses" |
| DAO / Treasury | Governance attack | "proposal passes with a flash-loaned quorum" |
| Any | No timelock on admin | "fee parameters changed against users between deposit and withdrawal" |

Write the translation as a **single sentence of business risk**. It must:
- Name the consequence in business terms (funds, users, reputation)
- Include a protocol-specific anchor (e.g. "your oracle integration", "your upkeep mechanism", "your deposit flow")
- NOT name the vulnerability class, file, or line number

Store this internally as `{insight}`. This is the only piece of audit data that enters the email.

### Step 3 — Compose the Email

Apply the Email Generation Rules below. The `{insight}` is the only audit data allowed in.

---

## Email Generation Rules

Every outbound email must follow this exact structure. No exceptions.

### Structure (3–4 sentences total)

**Sentence 1 — Hook (proves you found something specific):**
"I reviewed [protocol name]'s [named area — e.g. oracle integration / upkeep mechanism / deposit flow] and flagged something that [brief non-technical description of what it affects]."

**Sentence 2 — Business risk (makes them feel the consequence):**
The `{insight}` sentence. One sentence. Business language only. No CVEs, no Solidity, no line numbers.

**Sentence 3 — Withhold + soft CTA:**
"I've documented the specifics — want me to send over the brief?" 
OR: "Happy to share the one-page summary if useful."
OR: "I can walk you through it in 15 minutes if you want to see it."

**Sentence 4 (optional — use only if the protocol is declining/winding down):**
"Either way, thought it was worth flagging."

### Hard Rules

| Rule | Detail |
|------|--------|
| Max length | 3–4 sentences. Never more. |
| No report in email | Never attach, link, paste, or summarise the full report |
| No technical terms | No "reentrancy", "calldata", "Solidity", "EVM", "ABI", ".sol" in the email body |
| No "report below" | Banned phrases: "attached", "report below", "here is the audit", "findings include", "I found X vulnerabilities" |
| No list of issues | One insight only. Lists signal "I did a scan and dumped it". One specific thing signals "I understood your system" |
| Proof of specificity | The hook must name a concrete area of the protocol, not a generic risk category |
| Soft CTA only | Never demand a call, a contract, or a budget conversation in the first message |
| Sign-off | Name + one link only (GitHub or profile — not both) |

### Banned Openers

Never start with:
- "I hope this email finds you well"
- "I wanted to reach out"
- "My name is X and I"
- "I am a smart contract auditor"
- "I noticed your protocol has some issues"

### Good vs Bad Examples

| Bad | Good |
|-----|------|
| "I found 3 vulnerabilities in your contracts including a reentrancy in LiquidityPool.sol line 142." | "I reviewed your deposit mechanism and flagged something that could allow balances to be manipulated without a direct transaction." |
| "Attached is my full audit report of your protocol." | "I documented the specifics — want me to send over the summary?" |
| "Your contracts have not been audited since 2021 which is a serious risk." | "There's a gap in your oracle integration that's been open since your last audit cycle — pool balances could be corrupted during a network event." |
| "I am Muzammil, a senior blockchain developer with 3 years experience..." | Start with the finding. Never with your bio. |

---

## Gmail Automation

This agent uses the Gmail MCP (`@gongrzhe/server-gmail-autoauth-mcp`) to create email drafts and monitor replies. See `docs/gmail-setup.md` for the one-time OAuth setup.

### Draft-and-Confirm Model

The agent **never sends email automatically.** The workflow is:

```
pitch generated → agent creates Gmail draft → user reviews in Gmail → user clicks Send
                                                                              ↓
                                              agent monitors inbox for replies → updates tracker
```

### Label Structure

On first use, run `/web3-sales label-setup`. This creates:
- `Web3-Rabbit/Pending` — draft created, not yet sent
- `Web3-Rabbit/Sent` — outreach sent (apply manually after sending)
- `Web3-Rabbit/Replied` — protocol team has responded (agent applies this)
- `Web3-Rabbit/Call-Scheduled` — discovery call booked

### Finding the Contact Email

When creating a draft, search for the team's contact in this order:
1. Read the pitch file — check for email found during research
2. `search_emails` query: `from:{protocol-domain} OR to:{protocol-domain}`
3. WebSearch: `"{protocol name}" team email contact security OR audit site:twitter.com OR site:linkedin.com`
4. Check the protocol's docs for a security disclosure email
5. If no email found: note "contact not found — use Twitter DM" in the pitch file and skip draft creation

### Draft Creation (mode: `draft`)

When the user runs `/web3-sales draft {slug}`:

1. Read `data/pitches/{slug}-pitch-{date}.md` (handoff only — ~300 tokens)
2. Extract: To address, subject line, pitch body (Option A or B from the pitch file)
3. Call `draft_email`:
   ```
   to: {contact email}
   subject: {subject from pitch}
   body: {outreach draft text — plain text, no markdown}
   ```
4. After draft is created, update the pitch file: add `**Draft ID:** {id}` and `**Draft Created:** {date}`
5. Update `data/leads.md` status to `Draft Created`
6. Print: "Draft created in Gmail. Open Drafts → review → click Send. Run `/web3-sales inbox` to check for replies."

### Reply Monitoring (mode: `inbox`)

When the user runs `/web3-sales inbox`:

1. Load `data/leads.md` — find all rows with status `Pitched`
2. For each pitched lead, call `search_emails`:
   ```
   query: from:{protocol-domain} in:inbox after:{pitch-date}
   ```
3. If a reply is found:
   - Call `read_email` on the thread to extract the reply text
   - Summarize the response (positive / negative / question / ignored)
   - Update `data/leads.md` status to `Responded`
   - Apply label `Web3-Rabbit/Replied` to the thread
   - Print a summary: "Reply from {protocol}: {one-line summary}"
4. If no replies: "No new replies from {N} pitched leads."

### Gmail Tool Reference

| Tool | When Used | Key Args |
|------|-----------|----------|
| `draft_email` | After pitch generation | `to`, `subject`, `body`, `cc` (optional) |
| `search_emails` | Reply monitoring | Gmail search query string |
| `read_email` | Reading a reply | Email ID from search result |
| `list_email_labels` | One-time: verify labels exist | — |
| `create_label` | One-time: create label hierarchy | `name`, `color` |

### Context Budget for Gmail Modes

| Mode | Load | Do NOT load |
|------|------|-------------|
| `draft {slug}` | pitch file only | full audit report, leads.md |
| `inbox` | leads.md status column only | any pitch files |

Email bodies are short — inline. No intermediate files needed for Gmail modes.

---

## Pipeline Integrity

1. Never add new entries directly to `data/leads.md` by hand.
2. Write tracker additions to `batch/tracker-additions/{num}-{slug}.tsv`.
3. Use `node scripts/merge-tracker.mjs` to merge additions.
4. All tracker statuses must be canonical.
5. Every stage-3 report must point back to the stage-2 report path it used.
6. A pitch must never be generated without a completed research handoff.
7. A draft must never be created without a pitch file existing in `data/pitches/`.

### Canonical Statuses

| Status | Meaning |
|--------|---------|
| `Research Pending` | Raw lead exists but no stage-2 handoff yet |
| `Research Complete` | Stage-2 handoff exists and sales work can begin |
| `Evaluated` | Stage-3 sales brief generated |
| `Draft Created` | Gmail draft created — awaiting user review and Send |
| `Pitched` | Outreach sent (user manually applied after clicking Send) |
| `Responded` | Protocol team replied — agent detected via inbox check |
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
