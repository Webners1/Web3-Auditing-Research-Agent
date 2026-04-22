---
name: report-standards
description: Evidence standards, three-pillar framework, banned output patterns, specificity rules, and scenario playbook detail for the Web3 Auditing Agent. Load when writing any formal report or diligence output.
user-invocable: false
---

# Report Standards — Evidence, Specificity, and Quality Rules

Load this skill before writing any audit report, product assessment, diligence package, or strategic recommendation. These are the non-negotiable quality gates.

---

## Report Philosophy

**A findings-only report is a failure.** Every audit deliverable must cover all nine areas:

1. **Security findings** — broken with proof, severity, and industry-standard fixes
2. **Protocol health** — governance, tokenomics, oracle quality, composability, trust architecture vs. what serious protocols have in 2026
3. **Industry gap analysis** — what Aave, Compound, Curve, Uniswap, Morpho, EigenLayer, and category peers are doing that this protocol is not, and what those gaps cost in adoption, trust, or TVL
4. **Feature opportunities** — specific things to build or integrate (veToken, ERC-4626, Chainlink, L2, autocompound, bug bounty) with named protocol examples
5. **Business observations** — market shift since launch, real vs. marketing value proposition, single biggest non-code risk right now
6. **Execution roadmap** — effort-tiered sequence (Easy / Medium / Hard) with specific validated actions — no calendar estimates, no aspirational bullets
7. **App flow and UX maturity** — can real users complete core tasks quickly, confidently, and recover from failures
8. **Smart wallet readiness (conditional)** — AA claims implemented safely and operationally when applicable
9. **2026 market-readiness scorecard** — execution-ready across UI/UX, security, contracts, docs/GitHub, product clarity, business fit, and competitive stack

---

## Three-Pillar Assessment Framework

Every engagement assesses all three pillars. These are lenses applied throughout the report, not sections.

### Pillar 1 — Smart Contract Security

**What it measures:** Provable vulnerabilities in deployed or reviewed source code.

**Evidence standard:** Exact `File.sol:line`, vulnerable code block, numbered exploit sequence, 4-gate validation, industry-standard fix, fix rationale with one considered alternative.

**Output format:** FINDING (passes all 4 gates) or LEAD (incomplete proof) — never vague security commentary.

### Pillar 2 — Product Trust & Professional Standing

**What it measures:** Observable signals that capital allocators, integrators, protocol reviewers, and users use to decide whether a protocol is trustworthy. Covers operational maturity AND UX/design quality — because how a product looks and feels is itself a trust signal.

**Required evidence collection:**

*Operational maturity (use `skills/product-assessor/SKILL.md` Phase 2.4):*
- GitHub activity: last commit date, commit count last 30/90/180 days, open issue count, oldest unresolved issue age, contributor count
- Documentation freshness: last update date vs most recent contract deployment date, whether all deployed contracts are documented, whether an integration guide exists
- Audit standing: firms, dates, exact contract versions covered, whether currently deployed code is within audit scope
- Shipping history: major updates or deployments in last 6 months — what shipped, when, what impact was claimed
- Team and entity transparency: known contributors, entity operating the protocol, official channels
- Community signals: governance participation rate, incident communication history

*UX and design quality (use `skills/ux-audit/SKILL.md`):*
- Visual design: communicates professionalism or looks like an untouched template?
- Value clarity: can a first-time visitor understand the protocol within 10 seconds?
- Wallet connection flow: how many steps, what error states, what wallet coverage?
- Core transaction UX: is risk shown before signing, are errors decoded, are states handled?
- Trust signals in UI: contract addresses, audit links, risk disclosures visible in the app?
- Mobile and cross-browser: works on MetaMask Mobile and WalletConnect?
- Competitive UX position: where does this protocol sit vs function-matched peers?

**Output standard:** State the observable fact first. "Docs last updated 8 months before the v2 deployment" is the finding. "Update your docs" is not a finding — it is the recommendation. Same for UX: "The wallet connection flow requires 4 manual steps with no network auto-detection — users on the wrong network see a silent failure with no guidance" is a finding. "Improve your wallet UX" is not.

### Pillar 3 — Market Position & Strategic Path

**What it measures:** Where this protocol sits relative to its category right now and what specific actions close the highest-value gaps.

**Evidence standard for every strategic claim:**
1. A live data point from DefiLlama, L2BEAT, or Token Terminal — not training-data memory, not "the industry"
2. A named protocol doing the specific thing better — not "other protocols" or "industry leaders"
3. A concrete action — not "consider X" but "implement Y at Z using pattern W, reference: [specific protocol]"

**Output standard:** If a recommendation could appear unchanged in an audit of any DeFi protocol, it must be rewritten with protocol-specific evidence and a named comparison.

---

## Specificity Standards

The test for any output: could this same sentence appear unchanged in an audit of a completely different protocol? If yes, it is generic and must be rewritten before delivery.

### Banned Output Patterns

| Generic (never write this) | Required Replacement |
|---------------------------|---------------------|
| "Consider improving your documentation" | State last update date vs most recent deployment, name missing coverage, cite adoption cost ("DefiLlama shows 'unverified' without current docs") |
| "You should go multi-chain" | Name the specific chain, the market thesis grounded in live data, which protocols in the same category are growing there and why |
| "Improve your tokenomics" | Identify the specific failure (emission ended, reflexive incentive, no fee-to-token path), name the mechanism fix, cite a protocol that deployed it and what changed |
| "The industry uses X" | Name the exact protocol, what they specifically built, when they shipped it, what it cost other protocols not to do it |
| "Consider launching a governance token" | Specify the utility mechanism, distribution model, and a named protocol where this drove measurable TVL retention |
| "Commission a bug bounty" | Name the engagement type needed (full source audit + fuzzing, formal verification), name firms that specialize in this category, state what this report covers and does not |
| "Consider X for better Y" | "Implement X at [location] using [specific pattern] — reference: [Protocol] deployed this via [mechanism] — closes [specific gap] that currently prevents [specific consequence]" |
| Any trend claim without data | Attach a DefiLlama/L2BEAT/Token Terminal citation — if none exists, label the claim explicitly as hypothesis |

### Required Structure for Every Recommendation

Every substantive recommendation must follow this structure:

1. **Current observable state** — what is measurable right now (date, number, URL, or direct quote)
2. **Named comparison** — which specific protocol does this better, and what exactly they built or shipped
3. **Gap consequence** — what this specific gap prevents or costs (integration blocked, TVL cap, institutional barrier, user retention failure)
4. **Specific action** — not "improve X" but "implement Y at Z because W — reference: [Protocol that did it]"

---

## Scenario Playbooks — Detail

### Idea Mode
Trigger: user exploring or sharing thoughts before formal work begins.
- Use `founder-copilot`
- Respond conversationally — this is not a report
- Focus on viability, hidden risks, sequencing, and stronger variants
- Save good ideas to memory if the user confirms

### Discovery Mode
Trigger: the protocol is not yet fully understood.
- Use `product-assessor`
- Map the system, trust boundaries, contracts, and dependencies
- Explicitly evaluate one primary workflow and one failure path
- Do not jump into contract findings before the product is understood

### Audit Mode
Trigger: user wants a security review.
- Use `web3-audit`
- Maintain strict proof discipline — FINDING requires all 4 gates; otherwise it is a LEAD
- Update `findings.md` and `open-questions.md` in protocol memory

### Remediation Mode
Trigger: findings exist and the user wants solutions.
- Use `remediation-architect`
- Optimize for the best fix, not the easiest fix
- Record chosen direction in `decisions.md`

### Architecture Mode
Trigger: the protocol needs better structure or scale.
- Use `arch-advisor`
- Benchmark against strong protocol patterns (named protocols, not generics)
- Document trade-offs and sequencing

### Founder / Market Mode
Trigger: user wants strategy, positioning, or roadmap advice.
- Use `ceo-advisor`
- Verify live market conditions before making any trend claim
- Connect business advice to execution capacity and protocol realities

### UX / Wallet Experience Mode
Trigger: user asks for app-flow quality, conversion bottlenecks, or wallet UX.
- Run a UX walkthrough on core flows and failure paths
- Classify friction as business risk when it impacts activation or retention
- Include fixes implementable by the current team

### Account Abstraction Mode
Trigger: user asks about smart wallets, gasless UX, or account abstraction.
- Verify whether ERC-4337 claims are backed by deployed behavior
- Assess paymaster limits, bundler failure handling, replay assumptions, and session key controls
- Separate marketing claims from operational reality

### Incident Mode
Trigger: live exploit, pause, or emergency is in scope.
- Prioritize in order: containment → blast-radius mapping → user safety → communication
- Separate confirmed facts from unknowns explicitly
- Recommend pause, key rotation, migration, or disclosure steps when warranted
- Do not speculate — label every unknown as unknown

### Multi-Protocol Mode
Trigger: several engagements are running at once.
- Never assume context carries over automatically between protocols
- Use protocol memory actively — load `memory/protocols/[slug]/` explicitly
- Keep a clean boundary between protocol-specific facts, findings, and founder notes

### Sales Research Mode (Stage 2)
Trigger: request is part of the three-agent sales workflow.
- Treat `web3-sales-agent/data/pipeline.md` as the shared inbox from `career-ops-source`
- Use `protocol-diligence` by default unless a narrower report is explicitly requested
- Write the Stage 2 report to `audit-output/`
- Write the research handoff to `web3-sales-agent/data/research-handoffs/{slug}.md`
- Include: report path, service recommendation, pitch hook, proof points, cautions
- Never generate the sales message — that belongs to `web3-sales-agent`
