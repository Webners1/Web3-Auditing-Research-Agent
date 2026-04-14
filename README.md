# Web3 Auditing Agent

Built by **Muzammil Siddiqui** — 5 years working directly with Web3 startups across smart contract development, protocol architecture, and product strategy. This agent distills that experience into a structured diligence system: the kind of review that catches what a checklist-based audit misses and gives founders a real picture of where their protocol stands, not just a list of bugs.

The goal is not to replace an audit firm. It is to give Web3 founders access to the same caliber of thinking — security, architecture, product, and market — that most teams only get after raising a Series A.

---

## What This Agent Actually Does

Most audit tools give you a bug list. This agent gives you three things:

**1. Security findings you can act on**
Every finding is validated through a 4-gate proof sequence before it is called a finding. No speculative warnings. Every confirmed finding comes with the exact file and line, a numbered exploit path showing how an attacker reaches the vulnerable state, and production-ready Solidity fix code — not advice to "consider adding a check." Industry-standard fixes are benchmarked against named protocols that solved the same class of problem.

**2. An honest picture of your protocol's trustworthiness**
Founders often underestimate how much the non-contract layer matters. Capital allocators, integrators, and serious users check GitHub activity, docs freshness relative to deployment dates, audit history, and whether the UI surfaces trust signals (contract addresses, audit links, risk disclosures). This agent audits all of it with observable facts, not opinions. If your docs were last updated 8 months before your v2 deployment, the report says that and names the specific integrators you are losing because of it. If your wallet connection flow requires 4 manual steps with no network auto-detection, the report says that too — and names a protocol in your category doing it right.

**3. A market position grounded in live data**
"Consider going multi-chain" is not advice. This agent uses live data from DefiLlama, L2BEAT, and Token Terminal, searches exploit databases and EIP/ERC standards, and benchmarks your protocol against function-matched competitors — including newer protocols that may have solved a specific problem better than the well-known blue chips. The result is a 2026 market-readiness scorecard across 7 dimensions with specific, implementable actions, not generic strategy bullets.

---

## The Three-Pillar Framework

Every report is organized around three pillars. All three are mandatory — a security-only report is a failure.

### Pillar 1 — Smart Contract Security
Provable vulnerabilities with exact locations, exploit paths, and industry-standard fixes.

Evidence standard: `File.sol:line`, vulnerable code block, numbered exploit sequence, 4-gate validation (Refutation → Reachability → Trigger → Impact), fix code, fix rationale, one considered alternative.

If a finding fails any gate it becomes a Lead, not a Finding. Leads are listed in the appendix — they are real suspicions, but unconfirmed.

### Pillar 2 — Product Trust and Professional Standing
Observable signals that determine whether external parties engage with the protocol.

Covers:
- GitHub: last commit date, commit velocity (30/90/180 days), open issues age, contributor count
- Docs: last update date vs most recent contract deployment — if these are out of sync, integrators cannot onboard without manual effort
- Audit standing: which firm, which contract version, whether currently deployed code is within that audit scope
- Shipping history: what shipped in the last 6 months and whether it was communicated publicly
- UX quality: 9-dimension audit (visual design, first impression, wallet connection, core transaction flow, error handling, trust signals in the UI, mobile support, information architecture, performance)
- Team and entity transparency signals

### Pillar 3 — Market Position and Strategic Path
Live-data-backed view of where the protocol sits in its category and what specific moves close the highest-value gaps.

Every recommendation follows a required structure: observable current state → named protocol doing it better → specific gap consequence → concrete implementable action. If a recommendation could apply unchanged to any DeFi protocol, it gets rewritten.

---

## Example: Mars Poolin Audit

The [`audit-output/`](audit-output/) folder contains a complete audit of [Mars Poolin](https://mars.poolin.fi/) — a live Bitcoin hashrate tokenization protocol on Ethereum mainnet. This is a real protocol with real findings.

**What the security audit found:**
- `LpStaking.sol`: SafeMath underflow in `calculateLpStakingIncomeRate` — when `totalLpStakingAmount` drops below `lastLpStakingAmount`, the subtraction reverts, permanently blocking all staking reward calculations. DoS on core protocol function.
- `PolyTWAP.sol`: paramSetter-controlled TWAP update frequency — a privileged address can set `updateFrequency` to 1 block, collapsing the time-weighted average to a spot price and enabling oracle manipulation.
- Single EOA controls all admin functions with no multisig, no timelock, and no pause mechanism — a compromised key means full protocol drain with no recovery path.

**What the product trust audit found:**
- GitHub: 4 total commits, created January 2021, no meaningful activity since
- Docs: no documentation site found. No changelog. No integration guide.
- Audit standing: no publicly verifiable audit
- Last on-chain transaction: January 6, 2026 — 97 days before this review
- UX: React SPA returns "You need to enable JavaScript" to crawlers. Wallet connection flow has no network auto-detection. Error states return raw hex reverts.

**What the market analysis found:**
- TVL declined 99.7% from $42.2M peak (November 2021) to $133K — not a bear market artifact, a structural erosion
- BTC restaking entrants (Swell swBTC, Bedrock brBTC, EigenLayer BTC yield) now offer comparable or better yield with dramatically more liquidity, audit history, and trust signals
- The protocol has a real moat — direct relationship with Poolin hashrate — but has not capitalized on it while the category moved

The full report covers all 13 sections including EIP/ERC upgrade intelligence (ERC-4626, ERC-7540, Chainlink PoR), 6 feature opportunities with reference protocol benchmarks, a Downside/Base/Upside projection model, and an effort-tiered remediation sequence (Easy/Medium/Hard).

---

## Requirements

**Required:**
- [Claude Code](https://claude.ai/code) — the CLI or desktop app. Free and Pro plans both work. Opus produces deeper analysis on complex protocols; Sonnet is faster for quick passes.

**Recommended (adds a parallel static analysis layer):**
```bash
pip install slither-analyzer        # Trail of Bits static analyzer
cargo install aderyn                # Cyfrin Rust-based analyzer
curl -L https://foundry.paradigm.xyz | bash && foundryup   # Foundry
```

The agent runs fully without these — it falls back to 8-agent AI analysis. Static tools add an additional detection layer on top.

---

## Installation

**Step 1 — Install inside Claude Code:**
```
install https://github.com/Webners1/Web3-Auditing-Agent
```
Type this in the Claude Code chat (not your terminal).

**Step 2 — Install companion skills:**
```bash
npm install
```
This automatically registers the Pashov and Trail of Bits skill packs. If the Claude Code CLI is not in your PATH, the installer tells you what to run manually.

---

## How to Use It

**Audit a live protocol:**
```
/audit https://app.yourprotocol.xyz/
```
The agent fetches the frontend, finds the contracts (via the app, explorer, or GitHub), runs the full three-pillar analysis, and writes a report to `audit-output/`.

**Full diligence (product + audit + strategy in one pass):**
```
/diligence https://app.yourprotocol.xyz/
```

**Audit a local contract folder:**
```
/audit contracts/
```

**Just the UX and product trust review:**
```
/ux-audit https://app.yourprotocol.xyz/
```

**Pressure-test an idea before building:**
```
/idea my-protocol: we want to launch a veToken model before fixing the oracle — is that right?
```

**Come back to a protocol in a new session:**
```
/recall my-protocol
```
Protocol memory persists across sessions. The agent remembers findings, open questions, decisions made, and next actions.

---

## All Commands

| Command | What it does |
|---------|-------------|
| `/start [url or name]` | Initialize a protocol — discover contracts, load memory, set context |
| `/research [url or name]` | Map the full protocol surface — contracts, docs, backend, governance |
| `/audit [url, path, or name]` | Full three-pillar audit report |
| `/diligence [url or name]` | 7-phase end-to-end review — product, security, architecture, strategy |
| `/ux-audit [url or name]` | 9-dimension UX audit — design, wallet flow, trust signals, mobile, competitive position |
| `/fix` | Effort-tiered remediation plan for current findings |
| `/arch [url or name]` | Architecture advisory — upgradeability, integrations, chain strategy |
| `/strategy [url or name]` | Market strategy memo with live data |
| `/expand-security-audit [protocol or finding]` | Deep dive on a finding — tradeoff analysis, alternative fixes, implementation packet |
| `/expand-business [protocol or question]` | Deep business expansion — competitive stack, 2026 readiness targets |
| `/expand-uiux [protocol or url]` | Full UX backlog — prioritized conversion and trust fix list |
| `/report` | Export current report to HTML + PDF |
| `/brief [protocol]` | What we know, what's open, what's next |
| `/idea [protocol]: ...` | Pressure-test an idea — viability, hidden risks, sequencing, stronger variants |
| `/remember [protocol]: ...` | Save a decision or constraint to protocol memory |
| `/recall [protocol]` | Load context for a protocol |
| `/challenge [protocol]: ...` | Force the agent to argue against an idea and explain why it may fail |
| `/compare [protocol]: A vs B` | Compare two directions with tradeoffs |
| `/next-actions [protocol]` | Current recommended next steps |

---

## What the Reports Look Like

All reports are written to `audit-output/` as Markdown. Run `/report` to render HTML and PDF.

```
audit-output/
  [project]-audit-[YYYYMMDD].md        ← full three-pillar report
  [project]-product-[YYYYMMDD].md      ← product and trust assessment
  [project]-remediation-[YYYYMMDD].md  ← implementation-ready fix plan
  [project]-arch-[YYYYMMDD].md         ← architecture roadmap
  [project]-strategy-[YYYYMMDD].md     ← CEO strategy memo
  [project]-diligence-[YYYYMMDD].md    ← complete executive package
```

The PDF renderer requires Chrome or Edge to be installed.

---

## Repo Structure

```
.claude/commands/          ← slash command definitions
skills/
  web3-audit/              ← 8-agent security audit engine with 4-gate validation
  product-assessor/        ← product surface mapping, trust signal audit
  ux-audit/                ← 9-dimension UX audit (built-in)
  remediation-architect/   ← effort-tiered fix planning
  arch-advisor/            ← upgradeability, composability, chain strategy
  ceo-advisor/             ← live-data market research and strategy
  protocol-diligence/      ← 7-phase end-to-end orchestrator
  protocol-memory/         ← persistent per-protocol memory
  founder-copilot/         ← conversational idea pressure-testing
memory/protocols/          ← one folder per active protocol
audit-output/              ← all generated reports
scripts/
  render_report.py         ← Markdown → HTML → PDF renderer
  install-skills.js        ← companion skill auto-installer
CLAUDE.md                  ← agent rules, three-pillar framework, specificity standards
package.json               ← npm entry point
```

---

## Optional Companion Skills

```
install https://github.com/pashov/skills
install https://github.com/trailofbits/skills
```

When Pashov's `x-ray` is installed, it runs before the audit to map protocol invariants and surface. When `solidity-auditor` is installed, it validates remediation code during implementation. Trail of Bits skills add advanced fuzzing and formal analysis integration.

---

## License

MIT

---

*Built by Muzammil Siddiqui. 5 years in Web3 — development, architecture, product strategy. This agent exists because most founders get a bug list when they need a real picture of where their protocol stands.*
