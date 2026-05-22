# /web3-rabbit — Unified Three-Agent Pipeline Controller

**Argument:** $ARGUMENTS

Controls all three Web3 client acquisition agents from a single command. Routes each sub-command to the correct agent and maintains pipeline state across Stage 1 → Stage 2 → Stage 3.

```
STAGE 1  career-ops-source    → Finds leads (grocery guy)
STAGE 2  web3-auditing-agent  → Researches leads (this repo)
STAGE 3  web3-sales-agent     → Pitches leads (closer)
```

---

## Step 1 — Parse Sub-command

Split `$ARGUMENTS` on the first space: `{sub-command} {target?}`

| Sub-command | Stage | Action |
|-------------|-------|--------|
| `scan` | 1 | Full batch scan across all enabled sources |
| `scan {source}` | 1 | Single-source scan (see sources list below) |
| `enrich {slug}` | 1 | Cross-source enrichment for one pipeline lead |
| `enrich-all` | 1 | Enrich every unresearched lead in pipeline |
| `score` | 1 | Score and rank all unresearched pipeline leads |
| `patterns` | 1 | Analyze which sources produce best leads |
| `research {slug}` | 2 | Run full diligence on one lead |
| `research-all` | 2 | Research every unresearched lead in pipeline |
| `pitch {slug}` | 3 | Generate pitch brief for one researched lead |
| `pitch-all` | 3 | Generate pitch briefs for all researched leads |
| `draft {slug}` | 3 | Create Gmail draft for a pitch-ready lead |
| `draft-all` | 3 | Create Gmail drafts for all pitches that don't have drafts yet |
| `inbox` | 3 | Check Gmail for replies from protocol teams |
| `label-setup` | 3 | Create Web3-Rabbit Gmail labels (one-time) |
| `pipeline` | all | View current state across all three stages |
| `run` | all | Autonomous full pipeline: scan → score → research → pitch → draft |
| `status` | all | Health check across all three agents |
| (empty) | — | Show this command menu |

---

## Step 2 — Route to the Right Agent

### Stage 1 Commands (`scan`, `enrich`, `score`, `patterns`)

These operate on `career-ops-source`. Load `career-ops-source/CLAUDE.md` for context and execute the corresponding mode:

**`scan` / `scan {source}`**
Load `career-ops-source/modes/batch.md` (all sources) or `career-ops-source/modes/scan.md` (single source).
Execute: `node career-ops-source/scan.mjs` (or `--source {source}`)

Valid source names: `commonwealth`, `bountycaster`, `tally`, `l2beat`, `rootdata`, `defillama`, `gecko`, `dexscreener`

**`enrich {slug}` / `enrich-all`**
Load `career-ops-source/modes/enrich.md`.
Look up target slug in `web3-sales-agent/data/pipeline.md`.
Run cross-source enrichment sequence (DefiLlama → Commonwealth → L2Beat → WebSearch fallback).

**`score`**
Load `career-ops-source/modes/score.md`.
Call `search_leads` (rabbit-pipeline MCP) with `status: "unresearched"` to get all pending leads.
Apply scoring matrix to results and output ranked list.
(pipeline.md is auto-generated — read from DB, not the file directly.)

**`patterns`**
Load `career-ops-source/modes/patterns.md`.
Read `web3-sales-agent/data/scan-history.tsv` and `web3-sales-agent/data/leads.md`.
Output source performance analysis and keyword intelligence.

---

### Stage 2 Commands (`research`, `research-all`)

These operate on this repo (web3-auditing-agent). Load the appropriate skill and run diligence.

**`research {slug}`**
1. Run in terminal: `python scripts/phase_runner.py {slug}`
   - The script is a Manager/Worker orchestrator — it spawns 3 isolated `claude --print` subprocesses,
     one per phase. Each subprocess terminates completely before the next starts.
   - Phase 1 → Product Assessment → writes `memory/protocols/{slug}/phase1_handoff.json`
   - Phase 2 → Smart Contract Audit → writes `memory/protocols/{slug}/phase2_handoff.json`
   - Phase 3 → Report Assembly → writes `audit-output/{slug}-diligence-{date}.md` + handoff
2. After script exits 0, confirm `web3-sales-agent/data/research-handoffs/{slug}.md` exists
3. Call `export_pipeline_md` (rabbit-pipeline MCP) to sync `pipeline.md`
4. Print: "Research complete — {slug} is ready for /web3-rabbit pitch {slug}"

Error recovery:
- "No lead found in DB" → run `/web3-rabbit scan` first
- "claude CLI not found" → ensure Claude Code is installed and `claude --version` works in terminal
- Phase timeout → retry with `python scripts/phase_runner.py {slug} --resume-from {N} --timeout 900`
- Partial failure at phase N → retry with `python scripts/phase_runner.py {slug} --resume-from {N}`
  (phase handoffs are cached to `memory/protocols/{slug}/phaseN_handoff.json` for safe resume)

**`research-all`**
Call `search_leads` (rabbit-pipeline MCP) with `status: "unresearched"`.
Run `research {slug}` for each result, ordered by:
1. Signal level (CRITICAL first — use signal_score field from DB)
2. Score (if score mode was run — read from score output)
3. Alphabetical fallback

Spawn a subagent per lead when researching 3+ leads:
```
Agent(
  subagent_type="general-purpose",
  prompt="[full research context for this slug]",
  description="web3-rabbit research {slug}"
)
```

---

### Stage 3 Commands (`pitch`, `pitch-all`)

These operate on `web3-sales-agent`. Read the research handoff and generate pitch material.

**`pitch {slug}`**
1. Confirm handoff exists: `web3-sales-agent/data/research-handoffs/{slug}.md`
2. If not found: "No research handoff for {slug}. Run /web3-rabbit research {slug} first."
3. If found: read handoff fields ONLY — `Primary Pain`, `Pitch Hook`, `Proof Points To Use`, `Cautions`, `Recommended Service` (do NOT load the full audit report)
4. Run **Insight Extraction** (see `web3-sales-agent/CLAUDE.md` → Insight Extraction section):
   - Select ONE finding from Proof Points
   - Translate to business risk sentence (`{insight}`)
5. Apply **Email Generation Rules** to produce a 3–4 sentence email using only the `{insight}`
6. Write to `web3-sales-agent/data/pitches/{slug}-pitch-{YYYYMMDD}.md`:
   - Internal section: full sales brief (recommended service, pricing, proposal outline)
   - Outreach section: the 3–4 sentence email ONLY — no raw findings, no report summary
7. The full audit report MUST NOT appear in the pitch file's outreach section or email draft

**`pitch-all`**
Run `pitch {slug}` for every handoff file in `web3-sales-agent/data/research-handoffs/` that does not already have a corresponding pitch.

---

### Gmail Commands (`draft`, `draft-all`, `inbox`, `label-setup`)

These commands use the Gmail MCP (`gmail` server in `.mcp.json`). Requires one-time OAuth setup — see `web3-sales-agent/docs/gmail-setup.md`. The agent **never sends email** — it creates drafts for user review.

**`label-setup`**
One-time setup. Call:
```
create_label: "Web3-Rabbit"
create_label: "Web3-Rabbit/Pending"
create_label: "Web3-Rabbit/Sent"
create_label: "Web3-Rabbit/Replied"
create_label: "Web3-Rabbit/Call-Scheduled"
```
Confirm labels were created and print: "Gmail labels ready. Run /web3-rabbit draft {slug} to create your first draft."

**`draft {slug}`**
1. Read pitch file: `web3-sales-agent/data/pitches/{slug}-pitch-*.md` (load body only — skip the full sales brief)
2. Extract: To email, Subject, and the outreach body text (Option A from the pitch)
3. If no email address found in pitch file:
   - Try: WebSearch `"{protocol name}" security contact email site:twitter.com OR "{protocol} team email"`
   - If still not found: print "No contact email found for {slug}. Add it manually to the pitch file as `**Contact Email:**` then re-run."
   - Do NOT create a draft without a verified To address
4. Call `draft_email`:
   - `to`: contact email
   - `subject`: neutral subject — e.g. "quick note on [protocol name]" (never "vulnerability", "audit", "security issue")
   - `body`: the 3–4 sentence outreach email from the pitch file's **Outreach Email** section ONLY — plain text, no markdown, no findings list, no report summary, no attachments
   - Label: `Web3-Rabbit/Pending`
5. Update pitch file: add line `**Gmail Draft ID:** {id}` and `**Draft Created:** {YYYY-MM-DD}`
6. Print: "Draft saved. Open Gmail → Drafts to review. After you send it, run `/web3-rabbit pipeline` to update the status to Pitched."

**`draft-all`**
Run `draft {slug}` for every file in `web3-sales-agent/data/pitches/` that does not contain a `**Gmail Draft ID:**` line.

**`inbox`**
Check Gmail for replies from pitched leads.

1. Read `web3-sales-agent/data/leads.md` — extract all rows where Status = `Pitched`
2. For each pitched lead, run:
   ```
   search_emails query: "label:Web3-Rabbit/Sent" after:{pitch_date_minus_1_day}
   ```
   Then for each protocol domain: `search_emails query: from:{domain} in:inbox`
3. For each reply found:
   - Call `read_email` to get the reply text (first 500 chars)
   - Classify response: `Positive` / `Negative` / `Question` / `Bounced` / `Auto-reply`
   - Apply label `Web3-Rabbit/Replied` to the thread
   - Print: `✓ {slug} replied — {classification}: "{first 100 chars of reply}"`
4. Print summary:
   ```
   Inbox Check — {date}
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   {N} pitched leads checked
   Replies: {M}
     ✓ {slug} — {classification}
     ...
   No reply: {K} leads
   → Run /web3-rabbit pipeline for full status
   ```

---

### Cross-Stage Commands (`pipeline`, `run`, `status`)

**`pipeline`**
Read all three data files and print a unified status view:

```
Web3 Rabbit Pipeline — {date}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STAGE 1 — Leads
  Unresearched:  {- [ ] count in pipeline.md}
  Researched:    {- [x] count in pipeline.md}
  Last scan:     {most recent date in scan-history.tsv}

  Top unresearched (by signal):
    + {name} | {chain} | {signal} | {lead_type}
    ...

STAGE 2 — Research
  Handoffs written:  {file count in research-handoffs/}
  Reports in audit-output/: {count}

  Researched protocols:
    ✓ {slug} — {date}
    ...

STAGE 3 — Pitches
  Pitch briefs ready: {count in pitches/ or leads.md}

  Pitched:   {- [x] or pitched count in leads.md}
  Pending:   {handoffs without pitches}

→ Suggested next action: {based on state above}
```

**`run`**
Autonomous full pipeline execution. Confirm with user before starting:
"Running full pipeline: scan → score → research top leads → generate pitches → create Gmail drafts. Confirm? (y/n)"

On confirmation:
1. Run `scan` (batch mode)
2. Run `score` to rank new leads
3. Run `research` for all leads scored 7+ (CRITICAL/HIGH with budget evidence)
4. Run `pitch` for all completed research handoffs
5. Run `draft-all` to create Gmail drafts for all new pitches
6. Print final `pipeline` summary with draft count

**`status`**
Check health across all three agents:

```
Web3 Rabbit Status
  career-ops-source/
    portals.yml:       OK ({N} sources, {M} enabled)
    scan.mjs:          OK / ERROR: {message}
    API keys:          Bountycaster: {SET/MISSING} | RootData: {SET/MISSING}
    scan-history.tsv:  {N} entries, last scan: {date}

  Pipeline DB (rabbit-pipeline MCP):
    rabbit_pipeline.db: {N} total | {M} unresearched | {K} researched | {J} pitched
    MCP server:        Call get_pipeline_stats to check DB health
    pipeline.md:       auto-generated export (read-only)

  web3-auditing-agent/
    Slither:           {version or NOT INSTALLED}
    Aderyn:            {version or NOT INSTALLED}
    Forge:             {version or NOT INSTALLED}
    audit-output/:     {N} reports
    research-handoffs: {N} handoffs

  web3-sales-agent/
    leads.md:          {exists / missing}
    pitches/:          {N} pitch briefs
    Gmail MCP:         {CONNECTED / NOT CONFIGURED}
    Drafts pending:    {N} (pitches without Gmail Draft ID)
    Inbox replies:     check with /web3-rabbit inbox
```

To check DB state directly: call `get_pipeline_stats` from the `rabbit-pipeline` MCP server.

---

## Step 3 — Unknown Sub-command

If sub-command is not in the list above, print:

```
Unknown command: {input}

Usage: /web3-rabbit {sub-command} [{target}]

Stage 1 — Lead Finding (career-ops-source):
  scan                Batch scan all 8 sources (three-wave parallel)
  scan {source}       Single-source scan
  enrich {slug}       Cross-source enrichment for one lead
  enrich-all          Enrich all unresearched pipeline leads
  score               Score and rank all pipeline leads (1–10)
  patterns            Analyze source performance and keywords

Stage 2 — Research (web3-auditing-agent):
  research {slug}     Full diligence for one protocol
  research-all        Diligence for all unresearched leads (ordered by score)

Stage 3 — Pitching + Email (web3-sales-agent):
  pitch {slug}        Sales brief + outreach for one researched lead
  pitch-all           Pitches for all completed research
  draft {slug}        Create Gmail draft for a pitch-ready lead
  draft-all           Create Gmail drafts for all un-drafted pitches
  inbox               Check Gmail for replies from pitched leads
  label-setup         Create Web3-Rabbit Gmail labels (one-time)

Full Pipeline:
  pipeline            View state across all three stages
  run                 Autonomous scan → score → research → pitch → draft
  status              Health check across all three agents + Gmail
```
