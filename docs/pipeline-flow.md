# Web3 Rabbit — Complete Pipeline Flow

**Last updated:** 2026-05-22  
**Author:** Muzammil Siddiqui

---

## Overview

Web3 Rabbit is a three-stage automated client acquisition system for blockchain development and smart contract security services.

```
STAGE 1 — career-ops-source      Scan 8 sources → classify leads → write to DB
STAGE 2 — web3-auditing-agent    Research lead → audit contracts → write report + handoff
STAGE 3 — web3-sales-agent       Generate pitch → create Gmail draft
```

Human touchpoints: review Gmail drafts before sending, respond to replies.  
Everything else is automated.

---

## Stage 1 — Lead Discovery

### Command

```
/web3-rabbit scan               # all 8 sources
/web3-rabbit scan defillama     # single source
```

Or directly: `node career-ops-source/scan.mjs`

### What it does

1. Reads `career-ops-source/portals.yml` for source URLs, API keys, and TVL filter
2. Fetches each enabled source in parallel (max 5 concurrent)
3. Parses raw data with a per-source parser
4. Applies filters (see below)
5. Deduplicates against DB + scan-history.tsv
6. Writes new leads to `rabbit_pipeline.db` (primary store)
7. Regenerates `pipeline.md` as a read-only human-readable export

### Sources and Signal Levels

| Source | Signal | Lead Type | Why It Works |
|--------|--------|-----------|--------------|
| Bountycaster | CRITICAL | Immediate Dev Need | Founders post "paying $3k for Solidity dev" |
| Commonwealth | HIGH | UI/Pain Lead | Pain discussions before governance votes |
| Tally | HIGH | Treasury Whale - Stale Product | Fat treasury + no governance activity |
| L2Beat | LONG_TERM | Pre-Launch L3/AppChain | Catch them before $1k TVL |
| DefiLlama | MEDIUM | TVL Sweet Spot | $50k–$200k range, best volume |
| RootData | MEDIUM | Grant Recipient | Has budget, hasn't built yet |
| GeckoTerminal | MEDIUM | TVL Sweet Spot | New pool deployments on Base/Arbitrum |
| DexScreener | MEDIUM | TVL Sweet Spot | Trending pairs with momentum |

### TVL Filter ($50k–$200k)

- **Below $50k:** hobby project, cannot pay
- **$50k–$200k:** needs help, has capacity to pay — **our sweet spot**
- **Above $200k:** likely has internal team already

Configured in `portals.yml` under `tvl_filter`.

### Version Filter (V1/V2/V3 Detection)

The most important filter for versioned protocols. Logic:

```
rysk-v1  ($194k)  + rysk-v12 ($43M)  → SKIP V1     (company too big, active product is V12)
fuji-v1  ($196k)  + fuji-v2  ($155k) → INCLUDE V1  (V1 is the dominant version, V2 is smaller)
fuji-v2  ($155k)  + fuji-v1  ($196k) → SKIP V2     (V1 is the bigger sibling, V2 will lose this round)
spectra-v1 ($178k) only              → INCLUDE V1  (no sibling exists, isolated product)
```

**Rule:** If any versioned sibling has TVL above our max ($200k), skip this version entirely. The real product is too big for us.

**Implementation in `scan.mjs`:**

```javascript
// V2 is above our range → protocol outgrew us
if (biggerVersionSlug && tvlBySlug.get(biggerVersionSlug) > max) continue;

// V2 is in our range → it will be picked up instead when loop reaches it
if (biggerVersionSlug && tvlBySlug.get(biggerVersionSlug) >= min) continue;
```

### Deduplication

Three-layer dedup before any lead is written:
1. URL exact match against DB
2. Slug match (normalized name) against DB + scan-history.tsv
3. Name match against scan-history.tsv

### DB Write

All new leads go to `web3-sales-agent/data/rabbit_pipeline.db`:

```sql
CREATE TABLE leads (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  url          TEXT NOT NULL UNIQUE,
  slug         TEXT NOT NULL,
  name         TEXT NOT NULL,
  chain        TEXT,
  tvl          TEXT,           -- formatted string: "$183k"
  lead_type    TEXT,
  signal_score TEXT,           -- CRITICAL | HIGH | MEDIUM | LONG_TERM
  source       TEXT,
  evidence     TEXT,
  status       TEXT DEFAULT 'unresearched',  -- unresearched | researched | pitched | replied | closed | skip
  created_at   TEXT,
  updated_at   TEXT
);
```

### Scan History TSV

`web3-sales-agent/data/scan-history.tsv` — append-only dedup log. Never auto-cleaned.

---

## Stage 2 — Research

### Command

```
/web3-rabbit research {slug}
/web3-rabbit research-all
```

### Lead Selection

The agent calls `get_next_unresearched_lead` on the `rabbit-pipeline` MCP server, which returns the highest-priority lead ordered:
1. CRITICAL → HIGH → MEDIUM → LONG_TERM (by signal_score)
2. Oldest first within same signal

For manual selection: `search_leads` with chain/signal filters.

### Phase-Gated Research (6 Phases)

Each phase loads ONE skill, writes output to disk, then unloads before next phase starts. This prevents context overflow on large protocols.

| Phase | Skill | Output File | Budget |
|-------|-------|-------------|--------|
| 0 | protocol-memory | `memory/protocols/{slug}/profile.md` | ~3k tokens |
| 1 | product-assessor | `memory/protocols/{slug}/product-notes.md` | ~12k |
| 2 | web3-audit | `memory/protocols/{slug}/findings.md` | ~15k |
| 3 | arch-advisor | `memory/protocols/{slug}/arch-notes.md` | ~10k |
| 4 | ceo-advisor | `memory/protocols/{slug}/strategy-notes.md` | ~10k |
| 5 | report-standards | `audit-output/{slug}-diligence-{date}.md` | ~25k |
| 6 | inline | `web3-sales-agent/data/research-handoffs/{slug}.md` | ~3k |

Each phase passes only a 50-token Phase Handoff to the next phase, never the full output.

### Contract Analysis (Phase 2)

Contract acquisition order:
1. GitHub clone → enumerate `.sol` files
2. Etherscan API (`getsourcecode`)
3. Etherscan UI / Blockscout (L2)
4. WebSearch fallback

Security analysis runs 8 parallel reasoning agents against the contracts:
- Access control, reentrancy, oracle staleness, arithmetic overflow
- Flash loan vectors, upgrade proxy risks, cross-function state consistency
- L2-specific issues (Arbitrum sequencer downtime, gas price assumptions)

Every finding must pass the 4-gate proof sequence:
1. **Refutation** — Is there a mechanism that prevents this? (modifiers, checks)
2. **Reachability** — Can an external caller actually reach this code path?
3. **Trigger** — What specific conditions make it exploitable?
4. **Impact** — What is the business consequence in plain language?

No finding is written without passing all four gates. Speculation is explicitly banned.

### Report Standards (Three-Pillar Framework)

A findings-only report is a failure. Every report covers three pillars:

**Pillar 1 — Security:** All findings with severity, proof path, and business impact  
**Pillar 2 — Protocol Health:** TVL trend, team activity, governance, competitive position  
**Pillar 3 — Market Position:** Category competitors, differentiation gap, 2026 readiness

### Research Handoff

After the report, a compact (~300 token) handoff is written to `web3-sales-agent/data/research-handoffs/{slug}.md`:

```
**Protocol:** {name}
**Slug:** {slug}
**Chain:** {chain}
**Recommended Service:** {service type + price range}
**Primary Pain:** {one sentence, what's wrong with the system}
**Pitch Hook:** {one sentence, why now, why you}
**Proof Points To Use:** {1-2 specific findings translated to business language}
**Cautions:** {conversion risk, team status, wind-down signals}
```

### DB Status Update

After research is complete:
```
update_lead_status(slug, "researched")
export_pipeline_md()   ← regenerates pipeline.md
```

---

## Stage 3 — Pitch + Email

### Command

```
/web3-rabbit pitch {slug}
/web3-rabbit draft {slug}
```

### Insight Extraction (Mandatory Step)

Before any email is written, the agent runs a 3-step extraction:

1. **Select ONE finding** from the handoff's Proof Points. The most concrete one with clearest business consequence.
2. **Translate to business risk.** Never use technical terms. Convert to: what goes wrong → who loses money → how much.
3. **Compose the {insight} sentence.** This is the ONLY finding that ever enters the outreach email.

Examples of correct translation:

| Protocol Type | Raw Finding | Business Risk ({insight}) |
|---------------|-------------|---------------------------|
| Derivatives/Perps | Missing L2 sequencer check | "pool balances get corrupted during network downtime — difficult to unwind cleanly" |
| DeFi/Lending | Reentrancy in withdraw | "liquidity pool drained in a single transaction under specific market conditions" |
| Bridge | Replay attack in relayer | "cross-chain assets locked or minted twice — impossible to resolve on-chain" |
| Options | Oracle slippage unprotected | "options can be purchased below fair value during any price spike — guaranteed loss to the pool" |

### Email Generation Rules

Every first outreach email is exactly **3–4 sentences**, never more:

```
Sentence 1 — Hook:        name the specific area reviewed (oracle integration, deposit flow, etc.)
Sentence 2 — Business risk: {insight} sentence — business language only, no CVE language
Sentence 3 — Withhold CTA: "I documented the specifics — want me to send over the summary?"
Sentence 4 (optional):    Softener if protocol is winding down
```

**What NEVER appears in an outreach email:**
- Raw findings, vulnerability names, CVE IDs, file paths, line numbers
- The words: audit, vulnerability, reentrancy, exploit, calldata, Solidity
- Any lists (lists signal automated scan, not expertise)
- Attachments or links to the full report
- Credentials or bio in sentence 1

**Subject line:** Neutral only — "quick note on [Protocol]", "flagged something in [Protocol]"  
Never: "Security vulnerability found", "Audit report for [Protocol]"

### Pitch File Structure

`web3-sales-agent/data/pitches/{slug}-pitch-{date}.md` contains three separated sections:

```
## Internal Sales Brief   ← NEVER sent
Recommended service, price range, proposal scope, contact search notes

## Insight Extraction     ← NEVER sent
Which finding was selected, why, business risk translation

## Outreach Email         ← ONLY this section goes to Gmail
The 3–4 sentence email, subject line, sign-off
```

### Gmail Draft Creation

The agent calls `draft_email` (gmail MCP) with:
- `to`: contact email (found from GitHub README, docs, or WebSearch)
- `subject`: neutral subject from Outreach Email section
- `body`: the 3–4 sentence email text only — no markdown, no findings summary
- Label: `Web3-Rabbit/Pending`

The agent **never sends email** — only creates drafts. Human reviews and clicks Send.

---

## Pipeline State Machine

### Lead Status Transitions

```
unresearched → researched → pitched → replied → closed
                                    → closed
           → skip   (filtered out: version too big, chain not primary, etc.)
```

### MCP Tools (rabbit-pipeline server)

| Tool | When to Use |
|------|-------------|
| `insert_lead` | scan.mjs calls this automatically after dedup |
| `get_next_unresearched_lead` | start of any research session |
| `search_leads` | filter by chain, signal, status |
| `update_lead_status` | after research, pitch, or reply |
| `export_pipeline_md` | after any status change to sync human view |
| `get_pipeline_stats` | health check |

### pipeline.md

**Read-only.** Auto-generated from DB by `exportPipelineMd()`. Never edit manually — scan.mjs will overwrite it.

---

## Current Pipeline State (2026-05-22)

| Status | Count |
|--------|-------|
| Total leads | 768 |
| Unresearched | 729 |
| Researched | 1 (mycelium-perpetual-pools) |
| Pitched | 0 |
| Skip | 38 (versioned with larger sibling) |

**Top unresearched by signal (primary chains):**

All current leads are MEDIUM signal (DefiLlama TVL Sweet Spot). CRITICAL/HIGH leads require Bountycaster and Tally API keys.

**Pending API keys:**
- Bountycaster (Neynar): needed for CRITICAL immediate dev need leads
- Tally: needed for HIGH treasury whale leads
- RootData: ✅ configured (`8IBw3evhInoUn0O4f3xLuBE2gMqXWxmy`)

---

## Known Gaps and Pending Work

### Milestone 1 — Complete
- SQLite DB with WAL mode (rabbit_pipeline.db)
- MCP server (rabbit-pipeline) with 6 tools
- scan.mjs writes to DB, pipeline.md is auto-generated export
- Version filter fixed: skip V1 if any sibling TVL > $200k

### Milestone 2 — Pending
sqlite-vec vector DB (`rabbit_memory.db`) — store audit findings as embeddings so similar vulnerabilities are automatically surfaced during research.

### Milestone 3 — Pending
Python orchestrator — hard phase gating in code (not prompts). Physically terminates LLM context between phases, passes only `phase_handoff.json`. Eliminates risk of phase bleed.

### Milestone 4 — Pending
Neynar (Bountycaster CRITICAL), Tally GraphQL (Treasury Whale HIGH). RootData already done.

### Milestone 5 — Pending
`/web3-rabbit deliver {slug}` — Stage 4 reply bridge. When a protocol replies to the outreach, generates a 1-2 page Risk Briefing that shows the exploit path in business language (no line numbers, no patch code), concluding with a CTA for a 15-minute verification call.

### Gmail OAuth — Pending
User must complete the 7-step setup in `web3-sales-agent/docs/gmail-setup.md` before draft creation works.

---

## File Map

```
d:/web3-auditing-agent/
├── .mcp.json                              MCP server registrations
├── .claude/commands/web3-rabbit.md        Unified command controller
├── career-ops-source/
│   ├── scan.mjs                           Stage 1 scanner (DB write path)
│   ├── portals.yml                        Source config + API keys
│   ├── pipeline-mcp-server.mjs            MCP server for DB tools
│   └── db/pipeline-db.mjs                 SQLite DB layer (node:sqlite)
├── skills/
│   ├── product-assessor/SKILL.md          Phase 1 research
│   ├── web3-audit/SKILL.md                Phase 2 security
│   ├── arch-advisor/SKILL.md              Phase 3 architecture
│   ├── ceo-advisor/SKILL.md               Phase 4 strategy
│   ├── protocol-memory/SKILL.md           Cross-session memory
│   └── context-engine/SKILL.md            Phase-gating rules + budget
├── audit-output/                          Full diligence reports
├── memory/protocols/{slug}/               Per-protocol memory
├── web3-sales-agent/
│   ├── CLAUDE.md                          Stage 3 constitution
│   ├── config/profile.yml                 Muzammil's credentials + pricing
│   ├── modes/_profile.md                  Email rules + objection handling
│   ├── data/
│   │   ├── rabbit_pipeline.db             Primary lead store (SQLite, WAL)
│   │   ├── pipeline.md                    Auto-generated export (read-only)
│   │   ├── scan-history.tsv               Dedup registry (append-only)
│   │   ├── research-handoffs/{slug}.md    Stage 2 → Stage 3 handoffs
│   │   └── pitches/{slug}-pitch-{date}.md Pitch briefs (internal + outreach)
│   └── docs/gmail-setup.md                OAuth setup guide (7 steps)
└── docs/pipeline-flow.md                  This file
```
