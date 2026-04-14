# Audit Report Format

Every audit report is a **complete protocol intelligence document** — not just a bug list.
A protocol team reading it should understand their security posture, where they stand vs the industry,
what they should build next, and a concrete execution path. Both founders and engineers must find it useful.

## File Naming
```
audit-output/[project-name]-audit-[YYYYMMDD].md
```

---

## Required Report Structure

```
1.  Header table
2.  Executive Summary
3.  Methodology (4-gate, confidence scoring)
4.  Findings Summary table
5.  Detailed Security Findings (all severities)
6.  Protocol Health Assessment
7.  Industry Gap Analysis
8.  EIP / ERC Upgrade Intelligence
9.  Feature & Integration Opportunities
10. Business & Strategic Observations
11. 2026 Market-Readiness Assessment
12. Remediation Sequence (effort-tiered: Easy / Medium / Hard)
13. Appendix: Leads / Unconfirmed + Open Questions
```

Sections 1–5 are technical. Sections 6–13 are protocol intelligence.
Both halves are required in every report.

---

## Section Templates

### 1. Header Table

```markdown
# Security Audit — [Protocol Name]

| Field | Value |
|-------|-------|
| Date | YYYY-MM-DD |
| Reviewer | Web3 Auditing Agent (Pashov Methodology) |
| Website | [url] |
| GitHub | [url] |
| Framework | Foundry / Hardhat / Truffle / [detected] |
| Contracts reviewed | [list key files] |
| Source | GitHub clone / local / bytecode |
| Tools | Slither vX, Aderyn vX, multi-agent |
| Prior audits | None / [link] |
| Protocol type | AMM / Lending / Staking / [detected] |
| Chain | Ethereum / Arbitrum / [detected] |
```

---

### 2. Executive Summary

3–5 sentences. Cover:
- What the protocol does and who it serves
- Overall security posture (honest — if poor, say so)
- Single most important protocol-level risk beyond the contracts
- One sentence on competitive position or relevance

Do NOT soften findings. If the protocol has never been audited, centralized admin, and 2021-era architecture,
say that directly. Founders can handle the truth. Vague summaries waste their time.

---

### 3. Methodology

Explain the 4-gate validation and confidence scoring. Keep it short — 1 table each.

---

### 4. Findings Summary Table

| ID | Title | Contract | Severity | Confidence |
|----|-------|----------|----------|------------|
| M-01 | ... | ... | HIGH | 100 |

---

### 5. Detailed Security Findings

For every CRITICAL / HIGH finding:
- **File:** `Contract.sol:line`
- **Confidence:** N — [brief gate summary]
- **4-gate validation:** Gate 1 / 2 / 3 / 4 each answered in one line
- **Vulnerable code:** copy the exact lines
- **Concrete exploit path:** numbered steps — actual state transitions, not prose
- **Industry benchmark:** name a real protocol with this fix ("Aave v3 uses X because Y")
- **Fix:** actual corrected Solidity code
- **Fix rationale:** why this is the best fit here, one alternative, and why that alternative is not preferred

For MEDIUM: location, gates, vulnerable code, fix code. PoC optional but preferred.
For LOW: location, one-line description, fix.
For INFO: location, observation, recommendation if any.

---

### 6. Protocol Health Assessment

Not a security finding — an honest assessment of the protocol as a product and system.

Cover these dimensions (use a table + short commentary):

| Dimension | Status | Notes |
|-----------|--------|-------|
| Governance model | 🔴 / 🟡 / 🟢 | Single EOA / multisig / DAO |
| Audit history | 🔴 / 🟡 / 🟢 | None / partial / full |
| Tokenomics | 🔴 / 🟡 / 🟢 | Emission ended / inflationary / sustainable |
| Oracle quality | 🔴 / 🟡 / 🟢 | AMM spot / TWAP / Chainlink |
| Composability | 🔴 / 🟡 / 🟢 | Bespoke / partial / ERC-4626 / standard |
| Upgrade architecture | 🔴 / 🟡 / 🟢 | Immutable / old proxy / UUPS + timelock |
| L2 / multi-chain | 🔴 / 🟡 / 🟢 | Mainnet only / 1 chain / multi-chain |
| Transparency | 🔴 / 🟡 / 🟢 | Opaque / partial / verifiable on-chain |
| Community / trust | 🔴 / 🟡 / 🟢 | Unknown / partial / established |
| Bug bounty | 🔴 / 🟡 / 🟢 | None / ImmuneFi tier |

After the table, 2–4 paragraphs on the most important health gaps and their compounding effect.

---

### 7. Industry Gap Analysis

What the broader DeFi and Web3 industry is doing that this protocol is not.

**Research discipline:** Do not default to comparing against Aave, Compound, and Uniswap for everything.
Find the **best protocol for each specific gap** — regardless of TVL or fame. A 6-month-old protocol
that solved oracle design better than Aave is a better benchmark for oracle design than Aave.

Before writing this section:
1. Check `skills/protocol-diligence/references/research-source-registry.md` for research sources
2. Search Solodit and Rekt.news for real exploits matching any security-related gaps
3. Check EIPs/ERCs — if a standard exists for the gap, cite the standard
4. Use DefiLlama category data to verify which protocols in this category are actually growing

Format: a comparison table + analysis.

```markdown
| Feature | This Protocol | Best Current Standard | Who Does It Best | Gap Impact |
|---------|--------------|----------------------|-----------------|------------|
| Oracle | AMM spot price, no minimum window | Fully on-chain TWAP with 30-min minimum + Chainlink fallback | Morpho Blue (fully on-chain), Chronicle (Ethereum-native) | Manipulable by large swap + immediate update call |
| Governance | Single EOA | Multisig + TimelockController | OpenZeppelin Governor + Safe (industry standard since 2021) | Single key = full drain, institutional adoption blocker |
```

Follow the table with 3–5 deep-dive examples. For each:
- **What** the gap is
- **Who solved it best** (may not be the most famous protocol)
- **When and why** they solved it — what incident or insight drove the decision
- **What it cost** other protocols that did not solve it (real exploits or adoption failures preferred)

If you cannot find a real incident or a specific named protocol doing something better, label it as
a best-practice recommendation rather than an industry gap.

---

### 8. EIP / ERC Upgrade Intelligence

This section is mandatory. It translates protocol weaknesses into standards-level upgrade decisions.

For each candidate standard include:
- **Standard and title**
- **Current status** (Final / Last Call / Review / Draft / Stagnant / Withdrawn)
- **Protocol fit** (the exact issue it solves in this protocol)
- **Case studies** (named protocols that adopted it, and what changed)
- **Adoption complexity** (LOW / MEDIUM / HIGH)
- **Recommendation** (Adopt now / Track now, adopt later / Do not adopt)

Format:

```markdown
| Standard | Status | Problem It Solves Here | Proven Adoption | Complexity | Recommendation |
|----------|--------|------------------------|-----------------|------------|----------------|
| ERC-4626 | Final | Staking positions are non-composable | Morpho, EtherFi, Yearn vault ecosystem | LOW | Adopt now |
```

Rules:
- Cover both established standards and high-signal emerging standards when relevant
- If multiple standards must be combined, explicitly show the connection path (example: ERC-4626 -> ERC-7540 -> ERC-7575)
- Do not include standards that are not applicable to the protocol's current architecture or business model
- Include one plain-language line after each recommendation explaining business impact for non-technical readers
- Add a protocol-specific implementation map with concrete scope:

```markdown
| Standard | Contracts / Modules Touched | Estimated LoC Delta | Test Additions | Re-Audit Surface |
|----------|------------------------------|---------------------|----------------|------------------|
```

- For status-sensitive standards (Draft/Review/Last Call), include a one-line risk note explaining what could change before adoption.

---

### 9. Feature & Integration Opportunities

Specific things this protocol should build or integrate, ranked by impact vs effort.

Each recommendation must map:
1. protocol problem,
2. best reference protocol(s),
3. technical implementation path,
4. business outcome.

Use this structure:

```markdown
| Current Problem | Best Reference Protocol(s) | Recommended Build / Integration | Technical Path | Business Outcome (Plain Language) | Effort |
|-----------------|----------------------------|----------------------------------|----------------|-----------------------------------|--------|
```

For each row, add a short paragraph:
- Why this reference protocol is the best fit (not just the most famous)
- Which additional features it unlocks once implemented
- How this recommendation connects with other recommendations in this section

AA/smart-wallet rows are conditional. If not applicable, explicitly mark `Not Applicable` with a one-line reason.

---

### 10. Business & Strategic Observations

Write this for founders, operators, and non-technical stakeholders.

Required blocks:
- **Founder Brief (plain language, 5 bullets max)**
- **Current value proposition vs perceived value proposition**
- **Market shift since launch and why it matters now**
- **Defensible moat and how to protect it**
- **Top non-code business risk**
- **Recommended business model direction with technical dependency notes**
- **YC-style operating scorecard (metrics table)**
- **12-month projection model (Downside / Base / Upside)**

Every strategic point should include one explicit technical dependency line:
"This business move depends on shipping [specific technical change]."

Metric requirements (mandatory):
- Provide numeric baseline, 90-day target, and 12-month target for at least 5 metrics.
- Use startup-operating metrics (not vanity metrics), such as:
	- net TVL growth rate (WoW or MoM)
	- liquidity retention (4-week or 8-week)
	- protocol revenue run-rate
	- incentive efficiency (incentives spent / net TVL added)
	- integration funnel conversion (pipeline -> live)
- Separate facts vs assumptions explicitly.

Projection requirements (mandatory):
- Include a scenario table with Downside / Base / Upside.
- Show at least one formula used (example: `Revenue = TVL * Gross Yield * Protocol Take Rate`).
- State assumptions clearly and keep them realistic for current protocol stage.

---

### 11. 2026 Market-Readiness Assessment

This section synthesizes technical and operating readiness for the next market cycle. Every row requires observable evidence — not opinions.

**UX row requirement:** If `skills/ux-audit/SKILL.md` was run (it should have been as part of product-assessor Phase 1.5), use the UX Posture score and the top 2 HIGH/CRITICAL UX findings as the evidence. UX quality is a trust signal and a conversion driver — it belongs in this table with the same rigor as security.

```markdown
| Dimension | Status | Evidence (observable facts) | Gap Cost | Priority Upgrade |
|-----------|--------|------------------------------|----------|------------------|
| UI/UX quality and user-flow reliability | Strong / Mixed / Weak | [UX Posture from ux-audit + key finding] | | |
| Security and incident resilience | Strong / Mixed / Weak | [audit history, audit currency, bug bounty status] | | |
| Smart contract quality maturity | Strong / Mixed / Weak | [test coverage visible in repo, framework, audit scope] | | |
| Docs/GitHub/presentation quality | Strong / Mixed / Weak | [last commit date, docs freshness vs deployment] | | |
| Product clarity and differentiation | Strong / Mixed / Weak | [first-impression finding from ux-audit, DefiLlama category rank] | | |
| Business durability (12-month view) | Strong / Mixed / Weak | [TVL trend, token emission status, revenue model status] | | |
| Stack competitiveness | Strong / Mixed / Weak | [named peer comparison from category with specific metric] | | |
```

For each Weak or Mixed dimension: one implementation-ready recommendation with a named reference protocol and sequencing note.

**UX → Trust connection:** For the UI/UX row, always connect UX quality to trust and adoption consequences, not only to "user satisfaction." A Weak UX rating with no trust signal explanation is incomplete.

---

### 12. Remediation Sequence (Effort-Tiered)

Organize fixes by implementation hardness, not calendar time.

Tiers:
- **Easy:** isolated code changes, low coordination, no migration
- **Medium:** cross-contract changes, upgrade steps, moderate migration/testing
- **Hard:** architecture changes, new trust assumptions, external integrations, migrations

For each action include:
- Exact file and line or component
- What to change
- Why it matters
- Validation requirement (tests, simulations, formal checks, or review)
- Dependency on other actions (if any)

Mandatory hard-tier requirement:
- Include an explicit recommendation for a dedicated external audit before mainnet deployment of hard-tier changes.
- State clearly that this report is not a substitute for implementation-specific re-audit.

---

### 13. Appendix: Leads / Open Questions

Include both unconfirmed technical leads and unresolved product/business questions.

```markdown
| Type | Item | Location / Area | Why It Matters | What Would Confirm It |
|------|------|-----------------|----------------|------------------------|
| Lead | ... | File.sol:LN | ... | ... |
| Open Question | ... | Product / Ops | ... | ... |
```

---

## Formatting Rules

1. Code blocks always include language identifier (`solidity`, `bash`, etc.)
2. Every CRITICAL and HIGH finding must include a PoC exploit path
3. Location format: `FileName.sol:line_number`
4. Sort findings within severity: most impactful first
5. Protocol Health table comes AFTER all security findings — not before
6. Industry Gap Analysis must name specific protocols, not categories
7. EIP / ERC Intelligence must include status, relevance, case studies, and adoption complexity
8. Every recommendation must explicitly map problem -> reference protocol -> technical path -> business outcome
9. Remediation must use effort tiers (Easy / Medium / Hard), never calendar tiers (days/weeks/months)
10. Write every strategic section in clear language understandable by non-technical stakeholders
11. Do not write a findings-only report. A report with no sections 6–13 is incomplete.
12. Business sections must include numeric scorecards and projection scenarios, not prose-only strategy.
13. Technical standards sections must include module-level implementation scope, not standards lists alone.
14. CRITICAL and HIGH findings require explicit fix rationale and at least one considered alternative.
15. AA readiness must be marked `Not Applicable` when the product path does not depend on smart-wallet behavior.
