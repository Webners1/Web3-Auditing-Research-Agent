# Web3 Rabbit

**Three-agent Web3 client acquisition and diligence system.**

Built by Muzammil Siddiqui — 5 years working directly with Web3 startups across smart contract development, protocol architecture, and product strategy.

```
STAGE 1 — career-ops-source     Finds hot protocol leads across 8 Web3 sources
STAGE 2 — web3-auditing-agent   Runs diligence: security, product, UX, strategy
STAGE 3 — web3-sales-agent      Writes the pitch, proposal, and tracks outreach
```

Control all three agents from a single command: `/web3-rabbit {command}`

---

## Quick Start

```bash
# 1. Install dependencies (career-ops-source scanner)
cd career-ops-source && npm install && cd ..

# 2. Configure lead sources (add API keys for Bountycaster, RootData)
nano career-ops-source/portals.yml

# 3. Fill the pipeline with fresh leads
/web3-rabbit scan

# 4. Score and rank the leads
/web3-rabbit score

# 5. Run diligence on the top lead
/web3-rabbit research {slug}

# 6. Generate a pitch brief
/web3-rabbit pitch {slug}

# Or: run the full pipeline autonomously
/web3-rabbit run
```

---

## Command Reference

All commands run via `/web3-rabbit {command}` from the `web3-auditing-agent` Claude Code session.

### Stage 1 — Lead Finding

These commands control `career-ops-source`. They scan, enrich, and analyze protocol leads.

| Command | Description |
|---------|-------------|
| `/web3-rabbit scan` | Full batch scan: all 8 sources in three priority waves |
| `/web3-rabbit scan commonwealth` | Commonwealth governance forum — UI/UX and migration pain threads |
| `/web3-rabbit scan bountycaster` | Farcaster bounty/dev channels — explicit dev requests with dollar amounts |
| `/web3-rabbit scan tally` | Tally on-chain governance — treasury whale detection ($200k+ DAO) |
| `/web3-rabbit scan l2beat` | L2Beat upcoming/announced — pre-launch L3s and app-chains |
| `/web3-rabbit scan rootdata` | RootData — seed/grant recipients with low TVL |
| `/web3-rabbit scan defillama` | DefiLlama — $50k–$200k TVL sweet spot across 3,000+ protocols |
| `/web3-rabbit scan gecko` | GeckoTerminal — new pool deployments on Base/Arbitrum |
| `/web3-rabbit enrich {slug}` | Cross-source enrichment for one pipeline lead (DefiLlama + Commonwealth + L2Beat + WebSearch) |
| `/web3-rabbit enrich-all` | Enrich every unresearched lead in the pipeline |
| `/web3-rabbit score` | Score all pipeline leads 1–10 (signal × cross-source × budget × urgency × chain) |
| `/web3-rabbit patterns` | Analyze scan history — which sources yield best leads, keyword performance |

### Stage 2 — Research and Diligence

These commands control `web3-auditing-agent`. They run the full three-pillar diligence suite.

| Command | Description |
|---------|-------------|
| `/web3-rabbit research {slug}` | Full diligence for one protocol: product, security, UX, architecture, strategy |
| `/web3-rabbit research-all` | Diligence for all unresearched leads, ordered by signal score |

Research routes by lead type:
- `Immediate Dev Need` → smart contract audit first
- `UI/Pain Lead` → product assessment + UX audit first
- `Treasury Whale - Stale Product` → product + CEO strategy first
- `Pre-Launch L3/AppChain` → architecture + strategy first
- `TVL Sweet Spot` / `Grant Recipient` → full diligence suite

### Stage 3 — Pitch and Outreach

These commands operate on `web3-sales-agent`. They require a research handoff to exist first.

| Command | Description |
|---------|-------------|
| `/web3-rabbit pitch {slug}` | Sales brief + outreach message for one researched lead |
| `/web3-rabbit pitch-all` | Pitch briefs for all completed research handoffs |

### Full Pipeline

| Command | Description |
|---------|-------------|
| `/web3-rabbit pipeline` | Unified view: lead counts, research status, pitch status across all three stages |
| `/web3-rabbit run` | Autonomous full pipeline: scan → score → research top leads → generate pitches |
| `/web3-rabbit status` | Health check: API keys, tools (Slither/Aderyn/Forge), pipeline file paths |

### Also Supported

Paste a URL or protocol name directly — the agent auto-routes:

| Input | Action |
|-------|--------|
| `commonwealth.im/compound` | Classify the thread as a lead, suggest enrichment |
| `tally.xyz/gov/myprotocol` | Check treasury + governance activity |
| `defillama.com/protocol/rysk` | Check TVL → add to pipeline if in range |
| `warpcast.com/dev/0x1a2b` | Extract and classify as Bountycaster lead |
| `"Rysk Finance"` (plain name) | Look up across sources → classify and add |

---

## Lead Sources

The scanner pulls from 8 sources, ranked by signal quality:

| Signal | Source | Why |
|--------|--------|-----|
| CRITICAL | **Bountycaster** | Founders post "paying $3k for Solidity dev" with explicit urgency |
| HIGH | **Commonwealth** | DeFi pain discussions happen BEFORE Snapshot votes — leads are warm |
| HIGH | **Tally** | Treasury > $200k + 0 proposals = zombie whale with resources |
| LONG_TERM | **L2Beat** | Announced/pre-launch L3s — reach them before they hit $1k TVL |
| MEDIUM | **DefiLlama** | $50k–$200k TVL sweet spot — 3,000+ protocols, filtered |
| MEDIUM | **RootData** | Seed/grant recipients with low TVL — money in, no product yet |
| MEDIUM | **GeckoTerminal** | New Base/Arbitrum pool deployments in TVL range |
| MEDIUM | **DexScreener** | Trending DEX pairs by chain |

Cross-source amplification: the same protocol appearing in 2+ sources is automatically upgraded to CRITICAL or HIGH. A Commonwealth pain thread + Tally treasury is the best lead in the system.

---

## Lead Signal Classification

Every lead gets a signal level and a lead type before delivery to the pipeline.

| Signal | Meaning |
|--------|---------|
| `CRITICAL` | Direct, explicit request — act immediately |
| `HIGH` | Strong community pain or treasury whale detected |
| `MEDIUM` | Funded or TVL-filtered — solid lead, standard urgency |
| `LONG_TERM` | Pre-launch — early mover advantage |

| Lead Type | Pitch Direction |
|-----------|----------------|
| `Immediate Dev Need` | "I saw your post, here's what we do" |
| `UI/Pain Lead` | "We fixed this exact pain for X protocol" |
| `Grant Recipient - Needs Product` | "You have the runway, let's build it right" |
| `Treasury Whale - Stale Product` | "Your DAO has resources. Let's ship a V2." |
| `Pre-Launch L3/AppChain` | "Reach out before they hit $1k TVL" |
| `TVL Sweet Spot` | Standard diligence pitch |

---

## Three-Stage Pipeline

### Stage 1 — career-ops-source (Grocery Guy)

Scans 8 Web3 sources. Applies three-level fallback: direct API → keyword WebSearch → open WebSearch. Classifies every lead with signal level, lead type, and evidence. Deduplicates against scan history. Writes raw leads to the shared inbox.

**Output:** `web3-sales-agent/data/pipeline.md`

**Modes:** `scan`, `enrich`, `score`, `patterns`, `batch`, `tracker`, `status`

**Scanner:** `career-ops-source/scan.mjs` (zero Claude tokens — pure HTTP/JSON)

### Stage 2 — web3-auditing-agent (Research Agent)

Reads unresearched leads from the pipeline. Runs a full three-pillar diligence suite:

- **Pillar 1 — Smart Contract Security:** Exact `File.sol:line`, exploit path, 4-gate validation, industry-standard fix. FINDING = proven. LEAD = suspicion. No speculative warnings.
- **Pillar 2 — Product Trust:** GitHub activity, docs freshness vs deployment dates, audit standing, UX quality (9-dimension), wallet connection flow, mobile support, trust signals in UI.
- **Pillar 3 — Market Position:** Live DefiLlama / L2BEAT data, named protocol benchmarks, function-matched competitors, 2026 readiness scorecard.

**Output:** `audit-output/{slug}-diligence-{YYYYMMDD}.md` + `web3-sales-agent/data/research-handoffs/{slug}.md`

**Skills:** protocol-diligence, product-assessor, ux-audit, web3-audit, remediation-architect, arch-advisor, ceo-advisor, protocol-memory, founder-copilot

### Stage 3 — web3-sales-agent (Closer)

Reads the research handoff + linked report. Writes the sales brief, outreach message, and proposal outline. Updates the lead tracker.

**Input:** `web3-sales-agent/data/research-handoffs/{slug}.md`
**Output:** `web3-sales-agent/data/pitches/{slug}-pitch-{YYYYMMDD}.md`

---

## Configuration

### portals.yml (career-ops-source)

The "grocery list" — controls what sources the scanner hits, TVL filter, API keys, and output paths.

```yaml
# TVL filter — sweet spot: needs help, can pay
tvl_filter:
  min: 50000     # $50k
  max: 200000    # $200k

# Tally treasury whale threshold
tally:
  min_treasury_usd: 200000
  max_proposals: 20

# Source list — enable/disable sources here
tracked_sources:
  - name: Bountycaster Bounties Channel
    type: bountycaster
    api_key: ""          # Get free key at neynar.com
    enabled: false       # Enable once API key is set

  - name: DefiLlama All Protocols
    type: defillama
    enabled: true        # No key required — enable by default
  ...
```

Full configuration reference: [`career-ops-source/portals.yml`](career-ops-source/portals.yml)

### API Keys

| Source | Where to Get | Header |
|--------|-------------|--------|
| Bountycaster | [neynar.com](https://neynar.com) (free tier ~100 req/day) | `Api-Key` |
| RootData | [rootdata.com/api](https://rootdata.com) | `Api-Key` |

Set API keys in `portals.yml` → `api_key: "your-key-here"`, then set `enabled: true`.

Sources without API keys (DefiLlama, GeckoTerminal, L2Beat, Commonwealth) work out of the box.

---

## What Stage 2 Actually Does

Most audit tools give you a bug list. This agent gives you three things across every engagement:

**1. Security findings you can act on**
Every finding passes a 4-gate proof sequence (Refutation → Reachability → Trigger → Impact) before it is called a finding. No speculative warnings. Every confirmed finding includes exact file and line, numbered exploit path, and production-ready Solidity fix code. Industry-standard fixes are benchmarked against named protocols that solved the same class of problem.

**2. An honest picture of protocol trustworthiness**
Capital allocators, integrators, and serious users check GitHub activity, docs freshness relative to deployment dates, audit history, and whether the UI surfaces trust signals. This agent audits all of it with observable facts — not opinions. "Docs last updated 8 months before the v2 deployment" is a finding. "Update your docs" is not.

**3. A market position grounded in live data**
"Consider going multi-chain" is not advice. This agent uses live DefiLlama, L2BEAT, and Token Terminal data, searches exploit databases and EIP/ERC standards, and benchmarks protocols against function-matched competitors — including newer protocols that may have solved a specific problem better than the well-known blue chips.

---

## Example Output

The [`audit-output/`](audit-output/) folder contains a complete audit of Mars Poolin — a live Bitcoin hashrate tokenization protocol on Ethereum mainnet.

Findings: SafeMath underflow in `LpStaking.sol`, paramSetter-controlled TWAP manipulation in `PolyTWAP.sol`, single EOA admin with no multisig or timelock.

---

## File Structure

```
web3-auditing-agent/               ← Stage 2 root (this repo)
├── .claude/commands/
│   └── web3-rabbit.md             ← Unified /web3-rabbit command controller
├── .claude/skills/
│   ├── protocol-diligence/        ← Full end-to-end diligence skill
│   ├── product-assessor/          ← Product review and contract discovery
│   ├── web3-audit/                ← Smart contract security audit
│   ├── ux-audit/                  ← Web3 UX and design quality audit
│   ├── arch-advisor/              ← Architecture review and strategy
│   ├── ceo-advisor/               ← Market position and founder strategy
│   ├── remediation-architect/     ← Fix planning and remediation
│   ├── protocol-memory/           ← Persistent protocol context
│   ├── founder-copilot/           ← Conversational idea copilot
│   ├── report-standards/          ← Evidence standards and output rules
│   └── context-budget/            ← Context window optimization
├── audit-output/                  ← All diligence reports (Stage 2 output)
├── memory/protocols/              ← Per-protocol persistent memory
├── CLAUDE.md                      ← Stage 2 agent constitution
│
├── career-ops-source/             ← Stage 1 — Lead Scanner
│   ├── scan.mjs                   ← Scanner engine (zero Claude tokens)
│   ├── portals.yml                ← Source config and API keys
│   ├── modes/
│   │   ├── _shared.md             ← Signal classification and delivery format
│   │   ├── lead-sources.md        ← Deep intelligence for all 8 sources
│   │   ├── scan.md                ← Single-source scan mode
│   │   ├── batch.md               ← Three-wave parallel batch scan mode
│   │   ├── enrich.md              ← Cross-source enrichment mode
│   │   ├── score.md               ← Lead scoring matrix mode
│   │   └── patterns.md            ← Source performance analysis mode
│   ├── .claude/skills/career-ops/ ← career-ops skill (all mode routing)
│   └── CLAUDE.md                  ← Stage 1 agent constitution
│
└── web3-sales-agent/              ← Stage 3 — Sales and Outreach
    └── data/
        ├── pipeline.md            ← Shared lead inbox (written by Stage 1)
        ├── scan-history.tsv       ← Cross-session dedup log
        ├── leads.md               ← Stage 3 tracker (read by Stage 1 for dedup)
        └── research-handoffs/     ← Stage 2 → Stage 3 handoff files
```

---

## Running Individual Agents

Each agent can also be controlled directly from its own session:

**Stage 1 — career-ops scanner:**
```bash
cd career-ops-source
node scan.mjs                         # all enabled sources
node scan.mjs --dry-run               # preview without writing
node scan.mjs --source commonwealth   # single source
node scan.mjs --source bountycaster
node scan.mjs --source defillama
```

Or via skill from within the career-ops-source Claude session:
```
/career-ops scan
/career-ops scan commonwealth
/career-ops enrich rysk-v1
/career-ops score
/career-ops patterns
/career-ops status
```

**Stage 2 — research agent** (from web3-auditing-agent session):
```
/start {protocol}           → Resume or start a protocol engagement
/research {protocol}        → Full external research and diligence
/product-assessor {protocol}
/web3-audit {protocol}
/arch-advisor {protocol}
/ceo-advisor {protocol}
/protocol-diligence {protocol}
/sales-research-pipeline    → Research all queued leads from pipeline
```

---

## Building

The scanner requires Node.js (v18+) and one npm package:

```bash
cd career-ops-source
npm install          # installs js-yaml (and playwright for future browser fallback)
```

No build step needed. The scanner runs as a plain ESM Node script.

The Claude agent skills are markdown files — no compilation, no deployment.

---

## Principles

1. **No speculative findings** — every security finding needs a concrete exploit path
2. **Product before code** — understand what the system does before judging how it does it
3. **Industry-standard fixes** — remediation benchmarks against named protocols, not generic advice
4. **Live data only** — trend and market claims must cite DefiLlama, L2BEAT, or Token Terminal
5. **Business specificity** — advice must be concrete enough to act on tomorrow
6. **Three-level fallback** — scanner never gives up on a source without trying three approaches
7. **Complete reports** — a security-only report is a failure; all nine areas are mandatory
8. **Stage discipline** — each agent stays in its lane: find → research → pitch
