# Web3 Auditing Agent

A founder-grade Web3 protocol diligence system for [Claude Code](https://claude.ai/code). Point it at any protocol URL or local contract folder and get back a complete intelligence report — not just a bug list.

**Security findings. Protocol health. Industry gap analysis. Feature opportunities. Business strategy. 30/60/90 day plan.**

---

## What It Produces

Every report covers these core areas:

| Area | What you get |
|------|-------------|
| **Security findings** | Exact file:line locations, 4-gate validated exploits with PoC sequences, and industry-standard fix code |
| **App experience and UX flow** | Workflow-level friction analysis (onboarding, first transaction, failure recovery) with practical fixes that improve conversion and trust |
| **Smart wallet / AA readiness (conditional)** | ERC-4337 and smart-wallet reality check when applicable: paymaster policy, bundler dependencies, session-key guardrails, and EIP-1271 compatibility gaps |
| **Protocol health** | 10-dimension scorecard — governance, oracle quality, composability, audit history, upgrade architecture, and more |
| **Industry gap analysis** | Comprehensive research across the full Web3 landscape — exploit databases, EIPs, emerging protocols, and live category data — to find the best standard for each gap, not just what the largest protocols happen to do |
| **Feature opportunities** | Specific things to build or integrate, ranked by impact vs effort, with named protocol proof |
| **Business observations** | Real value proposition, market shift since launch, unfair advantages, and the single biggest non-code risk |
| **2026 market-readiness scorecard** | Evidence-based readiness view across UI/UX, security, contract quality, docs/GitHub/presentation, product clarity, business durability, and stack competitiveness |
| **30/60/90 day plan** | Sequenced, concrete execution steps |

> See [`audit-output/mars-poolin-audit-20260413.md`](audit-output/mars-poolin-audit-20260413.md) for a full example on a live Ethereum protocol.

---

## Installation

**Step 1 — Install the agent in Claude Code:**

```
install https://github.com/Webners1/Web3-Auditing-Agent
```

**Step 2 — Install companion skills and dependencies:**

```bash
npm install
```

That's it. `npm install` automatically downloads and installs all companion skills (pashov/skills, trailofbits/skills) via the Claude Code CLI. If the Claude Code CLI is not in your PATH yet, the installer will tell you exactly what to run manually.

---

## Prerequisites

**Required:**
- [Claude Code](https://claude.ai/code) — the CLI or desktop app

**Recommended (unlocks static analysis layer):**

```bash
# Slither — Trail of Bits static analyzer
pip install slither-analyzer

# Aderyn — Cyfrin Rust-based analyzer
cargo install aderyn

# Foundry — compilation, testing, fuzzing
curl -L https://foundry.paradigm.xyz | bash && foundryup
```

The agent works fully without these tools — it falls back to multi-agent AI analysis only. Static analysis adds an additional detection layer on top.

---

## Quick Start

**Audit a live protocol by URL:**
```
/start https://app.yourprotocol.xyz/
```

**Full end-to-end diligence:**
```
/diligence https://app.yourprotocol.xyz/
```

**Audit contracts in a local folder:**
```
/audit contracts/
```

**Just the security review:**
```
/audit https://github.com/protocol/contracts
```

---

## Slash Commands

| Command | What it does |
|---------|-------------|
| `/start [url or name]` | Initialize a protocol — discover contracts, load memory, set context |
| `/research [url or name]` | Research a protocol, map its full surface, find all contracts |
| `/audit [url or name]` | Full security audit — findings, protocol health, gaps, opportunities |
| `/fix` | Generate remediation plan for current findings |
| `/arch [url or name]` | Architecture advisory — upgradeability, integrations, chain strategy |
| `/strategy [url or name]` | CEO / market strategy memo with live market research |
| `/diligence [url or name]` | Full 7-phase end-to-end review |
| `/expand-security-audit [protocol/finding/report]` | Deep expansion of major findings with fix-option tradeoffs and implementation packets |
| `/expand-business [protocol/question/report]` | Deep business and competitive-stack expansion with 2026 readiness targets |
| `/expand-uiux [protocol/url/report]` | Deep UI/UX journey expansion with prioritized conversion/trust fix backlog |
| `/report` | Export current report to HTML + PDF |
| `/brief [protocol]` | Quick status recall — what we know, what's open, what's next |
| `/idea [protocol]: ...` | Pressure-test an idea through 5 lenses |
| `/remember [protocol]: ...` | Save a decision or constraint to protocol memory |

**Chat-style variants:**
```
/recall mars-poolin
/switch-protocol uniswap-v4
/next-actions mars-poolin
/challenge mars-poolin: should we deploy on Arbitrum before fixing the oracle?
/compare mars-poolin: veTokenomics vs flat staking rewards
```

---

## Audit Methodology

Security findings use **Pashov's solidity-auditor methodology** when installed, with a built-in 8-agent fallback:

| Agent | Attack Surface |
|-------|---------------|
| Reentrancy | External calls, CEI violations, cross-function reentrancy |
| Access Control | Role mismanagement, privilege escalation, missing auth |
| Math Precision | Overflow, truncation, precision loss, rounding direction |
| Economic Security | Flash loans, oracle manipulation, MEV, sandwich attacks |
| Storage Layout | Proxy collisions, slot packing bugs, delegatecall misuse |
| Invariant | Conservation laws, accounting drift, state coupling |
| Periphery | External callbacks, ERC hook security, trust boundaries |
| Upgrade / Proxy | Initializer security, storage gaps, upgrade authorization |

Every finding passes **4-gate validation** before being classified as a FINDING:

```
Gate 1 — Refutation  : Is there a concrete code guard that blocks this?
Gate 2 — Reachability: Can a valid tx sequence reach this state?
Gate 3 — Trigger     : Can an unprivileged actor cause the harm?
Gate 4 — Impact      : Is the harm material (fund loss, DoS, governance capture)?
```

---

## Research Approach

The industry gap analysis and feature recommendations are based on **comprehensive, broad research** — not a fixed list of reference protocols.

The agent searches across:

- **Exploit databases** — Solodit, Rekt.news, DeFiHacks, Immunefi disclosed reports, Code4rena, Sherlock
- **EIPs and ERCs** — if a standard exists for the pattern, it cites the standard
- **Live market data** — DefiLlama, L2BEAT, Token Terminal, Dune Analytics
- **Security research** — Trail of Bits, Spearbit, Pashov, Halborn, OtterSec, BlockSec blogs
- **Emerging protocols** — new entrants in the relevant category, not just established blue chips
- **Academic and technical research** — Ethereum Research, Paradigm, a16z Crypto, Flashbots

The benchmark for any gap is **the best solution that exists anywhere** — which may come from a protocol that launched six months ago, not from Aave or Uniswap.

Comparable sets are selected by **function match first**, then by market relevance:
- direct peer solving the same user job
- adjacent alternative solving the same outcome differently
- one-curve-ahead protocol showing where the category is heading

Category narrative or sentiment claims are always paired with live data evidence.

---

## Optional Capability Extensions

When installed, these skills deepen cross-functional diligence beyond contract logic:

| Skill | Purpose |
|-------|---------|
| `ux-audit` | Real-user walkthroughs, friction mapping, resilience checks |
| `positioning-canvas` | Structured differentiation and category framing |
| `marketing-strategy-pmm` | GTM, messaging, and launch strategy scaffolding |
| `account-abstraction` | ERC-4337/smart-wallet implementation and sharp-edge checks |

---

## Skills

| Skill | File | Purpose |
|-------|------|---------|
| Full Diligence | `skills/protocol-diligence/SKILL.md` | 7-phase end-to-end orchestrator |
| Product Assessor | `skills/product-assessor/SKILL.md` | Product review, trust mapping, contract discovery |
| Security Audit | `skills/web3-audit/SKILL.md` | Deep smart contract security audit |
| Remediation Architect | `skills/remediation-architect/SKILL.md` | Best-practice fix planning |
| Architecture Advisor | `skills/arch-advisor/SKILL.md` | Upgradeability, integrations, chain strategy |
| CEO Advisor | `skills/ceo-advisor/SKILL.md` | Market positioning and roadmap strategy |
| Protocol Memory | `skills/protocol-memory/SKILL.md` | Persistent per-protocol context |
| Founder Copilot | `skills/founder-copilot/SKILL.md` | Conversational idea pressure-testing |

---

## Output Files

Reports are written to `audit-output/`:

```
audit-output/
  [project]-product-[YYYYMMDD].md      ← product review and trust model
  [project]-audit-[YYYYMMDD].md        ← full audit + protocol intelligence
  [project]-remediation-[YYYYMMDD].md  ← implementation-ready fix plan
  [project]-arch-[YYYYMMDD].md         ← architecture roadmap
  [project]-strategy-[YYYYMMDD].md     ← CEO strategy memo
  [project]-diligence-[YYYYMMDD].md    ← complete executive package
```

Run `/report` to export any report to HTML and PDF.

---

## Protocol Memory

The agent maintains persistent memory per protocol across sessions:

```
memory/
  index.md                          ← active protocol registry
  protocols/[slug]/
    profile.md                      ← what the protocol is
    findings.md                     ← audit findings
    decisions.md                    ← architectural decisions
    open-questions.md               ← unresolved questions
    next-actions.md                 ← what to do next
    working-memory.md               ← session context
```

---

## Repo Structure

```
.claude/commands/       ← slash commands (/audit, /fix, /arch, /strategy, etc.)
skills/
  web3-audit/           ← security audit engine + 8 specialized agents + references
  product-assessor/     ← product and dapp surface review
  remediation-architect/← fix planning and rollout
  arch-advisor/         ← architecture, upgrade patterns, chain strategy
  ceo-advisor/          ← market research and business strategy
  protocol-diligence/   ← full end-to-end orchestrator
  protocol-memory/      ← persistent per-protocol memory
  founder-copilot/      ← conversational idea review
memory/protocols/       ← one folder per active protocol
audit-output/           ← all generated reports
scripts/
  render_report.py      ← Markdown → HTML → PDF renderer
  install-skills.js     ← companion skill auto-installer (runs on npm install)
CLAUDE.md               ← agent constitution and operating rules
package.json            ← npm entry point (postinstall runs skill setup)
```

---

## Example Output

The [`audit-output/`](audit-output/) folder contains a complete audit of [Mars Poolin](https://mars.poolin.fi/) — a live Bitcoin hashrate tokenization protocol on Ethereum mainnet.

Findings: 2 HIGH, 4 MEDIUM, 3 LOW, 4 INFO — all with exact source code references and PoC sequences.

Protocol intelligence: health scorecard, industry gap analysis across the hashrate/yield category, 8 feature opportunities (veToken model, ERC-4626 vault, Chainlink oracle, Arbitrum deployment, Chainlink PoR), business positioning, and a concrete 30/60/90 day plan.

---

## License

MIT
