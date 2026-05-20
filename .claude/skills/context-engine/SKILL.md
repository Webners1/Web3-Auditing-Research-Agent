---
name: context-engine
description: Phase-gated context management for multi-phase protocol diligence. Prevents context bloat by loading only the skill needed for the current phase, writing findings to disk at each phase boundary, and using compact phase-handoff files instead of keeping all findings in context.
user-invocable: false
---

# Context Engine — Phase-Gated Diligence Pattern

Load this before beginning any multi-phase protocol engagement (diligence, audit+arch+strategy). It defines the loading rules, phase boundaries, and filesystem discipline that keep context under control.

---

## The Problem This Solves

A full diligence run without phase gating loads: product-assessor (~2k tokens) + web3-audit (~4k) + arch-advisor (~2k) + ceo-advisor (~2k) + report-standards (~2k) + all fetched web content + all contract source + all findings = 40k–60k tokens in a single session. This degrades output quality and hits context limits on large protocols.

Phase gating keeps each phase under ~15k tokens by:
1. Loading only the current phase's skill
2. Writing findings to disk at the phase boundary
3. Starting the next phase with a compact reference to the written file, not the full content

---

## Phase Map

| Phase | Skill to Load | Output File | Context Budget |
|-------|--------------|-------------|----------------|
| 0 — Memory | `protocol-memory` | `memory/protocols/{slug}/profile.md` | ~3k |
| 1 — Discovery | `product-assessor` | `memory/protocols/{slug}/product-notes.md` | ~12k |
| 2 — Security | `web3-audit` | `memory/protocols/{slug}/findings.md` | ~15k |
| 3 — Architecture | `arch-advisor` | `memory/protocols/{slug}/arch-notes.md` | ~10k |
| 4 — Strategy | `ceo-advisor` | `memory/protocols/{slug}/strategy-notes.md` | ~10k |
| 5 — Report | `report-standards` | `audit-output/{slug}-diligence-{date}.md` | ~12k |
| 6 — Handoff | inline | `web3-sales-agent/data/research-handoffs/{slug}.md` | ~3k |

---

## Phase Entry Rules

### Before loading any phase skill:
1. Confirm the previous phase's output file was written to disk
2. Load a 3-sentence summary of what was learned (read from file, do not re-derive)
3. State current phase explicitly: `PHASE {N} — {Name}: loading {skill}`

### File written = phase complete:
A phase is only complete when its output file exists on disk with meaningful content (not a placeholder). The next phase starts cold with only: that file's key findings + the new phase's skill.

---

## Phase Handoffs (what carries forward)

Each phase writes a compact handoff at the bottom of its output file:

```markdown
## Phase Handoff
- Protocol: {name}
- Chain: {chain}
- Key finding from this phase: {one sentence}
- Open question for next phase: {one question}
- Skip next phase? {yes/no — reason}
```

The next phase reads only this section, not the full file.

---

## Discovery Phase (Phase 1) — Context Budget Rules

Fetch in this order. Stop fetching once budget is near:
1. Protocol homepage (fetch, extract: what it does, chain, TVL, oracle) — max 500 tokens output
2. GitHub (check commits, find contract files — list only, don't read yet) — max 200 tokens
3. Docs (extract: architecture, trust model, contract list) — max 500 tokens
4. DefiLlama profile (TVL, category, audit field) — max 200 tokens

**Do not** keep full web page HTML in context. Extract only the facts listed. Discard the rest.

Write to `product-notes.md`: what the protocol does, trust model, oracle, GitHub status, audit history, UX observations. Do not write raw fetched content.

---

## Security Phase (Phase 2) — Context Budget Rules

Load contracts in batches. Do not keep all contract source in context simultaneously:
1. Read one contract at a time, extract findings, write to `findings.md`, then discard the contract from active context
2. Pattern: read → analyze → write finding → next contract
3. After analyzing all contracts, the findings file IS the security record

**Findings file format** (compact, queryable):

```
[FINDING-001] CRITICAL | LiquidityPool.sol:142 | Underflow in calculateRewards
  Proof: {one sentence exploit path}
  Fix: {one sentence}

[LEAD-001] HIGH | OptionExchange.sol:89 | Unvalidated oracle price
  Status: needs deeper check
```

Stage 2 report assembles from this file. The file IS the security section.

---

## Architecture Phase (Phase 3) — Context Budget Rules

Load only:
- `product-notes.md` → Phase Handoff section (50 tokens)
- `findings.md` → Phase Handoff section (50 tokens)
- `arch-advisor/SKILL.md`

Do NOT reload the full product notes or findings. The handoff summaries are enough for architectural recommendations.

---

## Strategy Phase (Phase 4) — Context Budget Rules

Load only:
- `arch-notes.md` → Phase Handoff section (50 tokens)
- `findings.md` → count of CRITICAL/HIGH/MEDIUM findings only (20 tokens)
- `ceo-advisor/SKILL.md`
- One WebSearch for live market data (required before any trend claim)

Do NOT reload product or security details. CEO analysis needs market context, not contract line numbers.

---

## Report Phase (Phase 5) — Assembly

Load:
- `product-notes.md` (full)
- `findings.md` (full)
- `arch-notes.md` (full)
- `strategy-notes.md` (full)
- `report-standards/SKILL.md`

This is the only phase that loads all phase outputs simultaneously. It is the assembly phase — not a research phase, so no new fetching occurs here.

Write the full report to `audit-output/{slug}-diligence-{date}.md`.

---

## Handoff Phase (Phase 6) — Compact

Do NOT load the full report. Write the handoff from memory + the Phase Handoff sections:

```markdown
**Protocol:** {name}
**Slug:** {slug}
**Chain:** {chain}
**Bucket:** {CRITICAL/HIGH/MEDIUM}
**Lead Source:** {source}
**Report Type:** full-diligence
**Report Path:** audit-output/{slug}-diligence-{date}.md
**Status:** Research Complete
**Recommended Service:** {audit | product-review | arch-advisory | full-diligence}
**Primary Pain:** {one sentence — the #1 finding or gap}
**Pitch Hook:** {one sentence — what to lead with}
**Proof Points To Use:** {2–3 bullets}
**Cautions:** {1–2 bullets — things that reduce fit or urgency}
```

This is ~300 tokens. Stage 3 (web3-sales-agent) loads ONLY this file, not the full report.

---

## Context Budget Summary

| Phase | Max active context |
|-------|-------------------|
| Any single phase | 15,000 tokens |
| Report assembly | 25,000 tokens |
| Full session total (all phases) | 60,000 tokens |

If a phase would exceed its budget: write what you have, note what was skipped, and continue. A partial finding file is better than a context overflow.

---

## When to Skip Phases

| Condition | Skip |
|-----------|------|
| No contracts found or private repo | Skip Phase 2 (Security) |
| Protocol is pre-launch (no product) | Skip Phase 1 fully, reduce Phase 3 |
| Lead type is `Immediate Dev Need` | Skip Phase 4 (Strategy) |
| Lead type is `Treasury Whale` | Skip Phase 2, go deep on Phase 4 |
| Protocol is already known from memory | Skip Phase 1, load profile.md only |
