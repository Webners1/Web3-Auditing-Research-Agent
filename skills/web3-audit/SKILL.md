---
name: web3-audit
description: Smart contract security audit workflow with static analysis, multi-agent findings, and protocol-intelligence reporting.
---

# Web3 Smart Contract Security Auditor

Comprehensive security audit orchestrator using **Pashov's solidity-auditor methodology** as the primary engine. Runs Slither and Aderyn static analysis, then deploys 8 parallel specialized security agents — each a domain expert — to cover every vulnerability category. Produces professional-grade audit reports with exact file:line references, PoC exploit sequences, 4-gate validated findings, and **industry-standard fix recommendations** that name the protocols and patterns used by Aave, Compound, Uniswap, OpenZeppelin, and Morpho.

## Primary Audit Engine

When `pashov/skills` is installed, invoke `solidity-auditor` from that skill as the **primary audit engine**:
- It runs 8 specialized agents in parallel (vector-scan, access-control, math-precision, economic-security, execution-trace, invariant, periphery, first-principles)
- It enforces the FINDING vs LEAD distinction with 4-gate validation
- Use our 8-agent system below as the **built-in fallback** when pashov/skills is not installed

## Finding Quality Requirements

Every **CRITICAL** or **HIGH** finding MUST include all of the following — no exceptions:

1. **Exact location** — `ContractName.sol:line_number`
2. **Vulnerable code block** — copy the actual offending lines with the vulnerability marked
3. **Concrete exploit sequence** — numbered steps showing exactly how an attacker triggers the issue
4. **Industry benchmark** — name at least one protocol that had this pattern or uses the correct fix (e.g., "Aave v3 uses...", "Compound v3 uses...", "OpenZeppelin SafeERC20 handles this by...")
5. **Recommended fix** — actual corrected Solidity code, not just a description
6. **Fix design rationale** — why this fix is best for this protocol, one viable alternative, and why the alternative is not preferred

Every **MEDIUM** finding MUST include items 1–3 and a fix recommendation.

If the starting point is a product, website, or mixed repo rather than an already-scoped contract set, run `skills/product-assessor/SKILL.md` first so the audit has the right contract surface and threat model.

If external context is needed, load `skills/protocol-diligence/references/research-source-registry.md` and prefer official docs, addresses pages, explorer sources, and prior public audit pages before generic web search.

**Trigger phrases:** `audit`, `security review`, `find vulnerabilities`, `check this contract`, `audit this protocol`, `full audit`, `run audit`

---

## Execution Pipeline

### Phase 1 — Discovery (run all concurrently)

**1a. Enumerate in-scope contracts**
```bash
find . -name "*.sol" \
  -not -path "*/node_modules/*" \
  -not -path "*/lib/*" \
  -not -path "*/test/*" \
  -not -path "*/tests/*" \
  -not -path "*/mock*" \
  -not -path "*Mock*" \
  -not -path "*/.git/*" | sort
```
Ask user to confirm scope if ambiguous.

**1b. Detect framework**
```bash
ls foundry.toml hardhat.config.js hardhat.config.ts 2>/dev/null | head -3
```

**1c. Check tool availability**
```bash
slither --version 2>&1 | head -1
aderyn --version 2>&1 | head -1
```
If either tool is missing, warn with install instructions and continue with AI-only analysis.

**1d. Identify protocol type** — read first 200 lines of main contracts, detect: AMM, Lending, Staking, Bridge, NFT, Governance, Derivatives, Vault (ERC-4626).

**1e. Create output directory**
```bash
mkdir -p audit-output
```

---

### Phase 2 — Static Analysis (run concurrently)

**2a. Slither**
```bash
slither . --json audit-output/slither-raw.json 2>&1
```
Fallback if remapping needed:
```bash
slither . --solc-remaps "@openzeppelin=node_modules/@openzeppelin" --json audit-output/slither-raw.json 2>&1
```

**2b. Aderyn**
```bash
aderyn . --output audit-output/aderyn-raw.md 2>&1
```

Parse outputs:
- From Slither JSON: extract `results.detectors[]` — each has `check`, `impact`, `confidence`, `elements`
- From Aderyn markdown: extract finding blocks with severity and location
- Tag each finding: `[Slither]` or `[Aderyn]`
- Deduplicate findings pointing to same location
- Store as structured list for agent input

---

### Phase 3 — Agent Spawning

Prepare the agent bundle:
1. Read all in-scope `.sol` files — if ≤15 files, include full content inline; if >15 files, provide a manifest with paths
2. Include static analysis findings summary from Phase 2
3. Include `skills/web3-audit/references/audit-agents/shared-rules.md` content

Spawn all 8 agents in a **single parallel batch** — do not wait for one before starting the next:

| # | Agent | Instructions | Domain |
|---|-------|-------------|--------|
| 1 | Reentrancy Agent | `audit-agents/reentrancy-agent.md` | External calls, CEI violations, cross-function & read-only reentrancy |
| 2 | Access Control Agent | `audit-agents/access-control-agent.md` | Role mismanagement, privilege escalation, missing auth checks |
| 3 | Math Precision Agent | `audit-agents/math-precision-agent.md` | Overflow, truncation, precision loss, rounding direction |
| 4 | Economic Security Agent | `audit-agents/economic-agent.md` | Flash loans, oracle manipulation, MEV, sandwich attacks, price impact |
| 5 | Storage Layout Agent | `audit-agents/storage-agent.md` | Proxy storage collisions, slot packing bugs, delegation issues |
| 6 | Invariant Agent | `audit-agents/invariant-agent.md` | Broken conservation laws, state coupling, accounting errors |
| 7 | Periphery Agent | `audit-agents/periphery-agent.md` | External protocol callbacks, trust boundaries, ERC hook security |
| 8 | Upgrade/Proxy Agent | `audit-agents/upgrade-agent.md` | Initializer security, storage gaps, upgrade authorization, delegatecall misuse |

---

### Phase 4 — Consolidation & Security Report

1. **Collect** all 8 agent outputs
2. **Merge** with Slither/Aderyn tool findings
3. **Deduplicate** — group by `contract:function:bug_class`; if two agents flag same issue, keep highest-confidence version and add source tags
4. **Validate** each finding through the 4-gate framework (`references/judging.md`)
   - Gate 1: Is there a concrete guard blocking the attack? If yes, drop or downgrade.
   - Gate 2: Can the vulnerable state actually be reached?
   - Gate 3: Can an unprivileged actor trigger it?
   - Gate 4: Is the impact material (fund loss, DoS, data corruption)?
5. **Sort** by severity: CRITICAL → HIGH → MEDIUM → LOW → INFO

---

### Phase 5 — Protocol Intelligence (required in every report)

**This phase is not optional.** A report with only security findings is incomplete. Founders and protocol teams need the full picture to act on the report.

After completing the security findings, produce these four sections for the report:

#### 5a. Protocol Health Assessment

Rate the protocol across 10 dimensions using 🔴/🟡/🟢:
- Governance model (single EOA vs multisig vs DAO)
- Audit history
- Tokenomics health (is there a sustainable incentive model?)
- Oracle quality (spot vs TWAP vs Chainlink)
- Composability (bespoke vs ERC-4626 vs standard interfaces)
- Upgrade architecture (immutable vs old proxy vs UUPS+timelock)
- L2 / multi-chain presence
- On-chain transparency / proof-of-reserves
- Community trust and communication
- Bug bounty program

Follow with honest commentary on the 3 most critical health gaps and how they compound each other.

#### 5b. Industry Gap Analysis

Compare this protocol's current state against what industry leaders are doing.
- Name specific protocols (Aave, Compound, Curve, Uniswap, Morpho, EigenLayer, etc.)
- Identify what they adopted, when, and what problem it solved
- Quantify the gap impact for this protocol (adoption blocker, TVL cap, trust deficit)

Format: a comparison table + named examples. Do NOT write generic "the industry uses X" — always say "Aave v3 adopted X in [year] because Y, which resulted in Z."

#### 5c. Feature & Integration Opportunities

List specific things the protocol should build or integrate, ranked by impact vs effort.
For each: what it is, what user/business problem it solves, which protocol proves the pattern, effort level (S/M/L).

Standard checklist to evaluate (include all that are relevant):
- veToken / governance model
- ERC-4626 vault wrapper for composability
- Chainlink oracle integration
- L2 deployment strategy
- Smart wallet / account abstraction readiness when applicable (ERC-4337 path, paymaster policy, EIP-1271 support)
- Autocompound mechanism
- Revenue sharing / protocol fee capture
- Cross-chain messaging (CCIP, LayerZero)
- Proof-of-reserves / on-chain transparency
- Bug bounty (Immunefi)
- EIP-7281 or canonical bridge patterns (if cross-chain)

#### 5d. Business & Strategic Observations

Write for the founder/CEO, not the engineer.
- What is the actual value proposition right now (not the marketing version)?
- What has the market moved toward since this protocol launched?
- What UX or wallet-friction bottleneck is suppressing conversion or retention?
- What unfair advantages does this protocol have that competitors cannot easily copy?
- What is the single biggest business risk right now (not a code bug — a market, trust, or retention risk)?
- One directional bet worth serious consideration

Be direct. Specific, uncomfortable truths are more useful than diplomatic vagueness.

#### 5e. 2026 Market-Readiness Snapshot

Add a concise readiness view with evidence-based judgments:
- UI/UX and user-flow reliability
- Security posture and incident resilience
- Smart contract engineering maturity
- Docs/GitHub/presentation quality for external trust
- Product clarity and category fit
- Business durability for the next 12 months
- Comparative stack competitiveness vs function-matched peers

For each weak area, include one concrete upgrade recommendation and expected impact.

---

### Phase 6 — Write Report and Export

1. **Format** all sections per `references/report-format.md` (includes sections 6–13)
2. **Write** report to `audit-output/[project-name]-audit-[YYYYMMDD].md`
3. **Include** 30/60/90 Day Execution Plan as the closing section
4. **Print** findings summary table to terminal
5. **Handoff** to `skills/remediation-architect/SKILL.md` if detailed fix planning is needed
6. **Handoff** to `skills/client-reporting/SKILL.md` for HTML/PDF export

---

## Agent Output Format

Each of the 8 agents must return findings in this exact format:

```
FINDING | contract: VaultCore | function: withdraw | bug_class: reentrancy-eth | severity: CRITICAL
location: VaultCore.sol:142
path: attacker.attack() → VaultCore.withdraw() → attacker.receive() → VaultCore.withdraw()
proof: balance not updated before .call{value}(); attacker re-enters with same balance value
description: Reentrancy in withdraw() allows attacker to drain all ETH before balance is decremented
industry_benchmark: Compound v1 exploited via this exact pattern ($60M). Aave v3 uses nonReentrant + CEI.
fix: |
  // Move state update BEFORE external call (CEI pattern)
  balances[msg.sender] = 0;           // effect first
  (bool ok,) = msg.sender.call{value: amount}("");  // interaction second
  require(ok, "transfer failed");
---
LEAD | contract: VaultCore | function: execute | bug_class: arbitrary-delegatecall | severity: HIGH
location: VaultCore.sol:89
code_smells: delegatecall to user-supplied `target` address in execute(); no whitelist
description: Potential arbitrary delegatecall — if target is attacker-controlled, storage can be corrupted
```

**FINDING** = confirmed vulnerability with concrete exploit path (passes all 4 gates)
**LEAD** = suspicious pattern that may be a vulnerability but needs further verification (fails ≥1 gate)

---

## Critical Rules

- **Scope discipline** — never flag test files, mocks, or libraries as vulnerabilities
- **No gas-only findings as security** — gas issues belong in INFO
- **Tool findings need validation** — Slither/Aderyn hits must pass 4-gate before becoming FINDING
- **Proof requirement** — no PoC = LEAD, not FINDING
- **Source attribution** — tag every finding: `[Slither]`, `[Aderyn]`, `[Agent-N]`, or combinations
- **Protocol-aware** — understand the design intent before calling something a bug

---

## Severity Calibration

| Severity | Criteria |
|----------|---------|
| **CRITICAL** | Direct loss of all or most funds; accessible to any caller without special conditions |
| **HIGH** | Significant fund loss requiring realistic but non-trivial conditions (flash loan, price window) |
| **MEDIUM** | Partial loss, griefing, or DoS requiring specific but achievable conditions |
| **LOW** | Best practice violations, inconsistencies with no direct impact |
| **INFO** | Gas optimizations, code quality, missing documentation |

---

## Safe Patterns (do NOT flag these)

- `unchecked` blocks with explicit overflow justification in comments
- `SafeERC20` wrapping
- `nonReentrant` modifier (but still check cross-contract reentrancy)
- Two-step ownership transfers
- MINIMUM_LIQUIDITY burns in AMMs
- Explicit narrowing casts in tight loops
- Protocol-favoring rounding (always rounds against user — intentional)
