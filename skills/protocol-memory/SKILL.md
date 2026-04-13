# Web3 Protocol Memory Manager

Maintains structured memory for each protocol so the agent can work across multiple projects without mixing context. Use when the user wants the agent to remember information, recall prior context, switch active protocol, continue a past engagement, or keep persistent notes while auditing multiple projects.

**Trigger phrases:** `remember this for`, `save this for`, `switch to protocol`, `load memory for`, `what do we know about`, `protocol brief`, `recall`, `update memory`, `working memory`, `continue where we left off`

---

## Memory Purpose

This skill prevents cross-project confusion. Each protocol gets its own memory folder so:
- findings do not leak between projects
- founder ideas remain attached to the right protocol
- architecture and business recommendations stay contextual
- the agent can resume work later without rebuilding everything from scratch

---

## Memory Layout

Store memory in:

```text
memory/protocols/[protocol-slug]/
```

Use these files:
- `profile.md` - what the protocol is, category, chains, core components, links
- `working-memory.md` - current hypotheses, latest facts, session notes
- `findings.md` - confirmed findings and unresolved leads
- `decisions.md` - decisions made, rejected options, rationale
- `open-questions.md` - what is still unknown or blocked
- `next-actions.md` - immediate next steps for the agent or founder

Update the top-level index:
- `memory/index.md`

Load `references/memory-schema.md` before creating or updating memory.

---

## Execution Pipeline

### Phase 1 - Identify Active Protocol

1. If the user names the protocol, use that.
2. If the repo clearly maps to one protocol, infer it and say so.
3. If multiple protocols are active and the target is ambiguous, ask a short clarifying question.

Normalize to a stable slug:
- `Aave v4` -> `aave-v4`
- `My Protocol` -> `my-protocol`

### Phase 2 - Read Existing Memory

Before answering substantive questions about a protocol:
1. Read `memory/index.md`
2. Read the active protocol folder if it exists
3. Summarize the active memory in 5-10 bullets internally before proceeding

### Phase 3 - Update Memory

When the user shares meaningful information, update the right file:

| Type of information | File |
|---------------------|------|
| Protocol description, components, links | `profile.md` |
| New session facts, hypotheses, observations | `working-memory.md` |
| Security findings, leads, exploit notes | `findings.md` |
| Chosen direction, rejected option, rationale | `decisions.md` |
| Unknowns, blockers, missing data | `open-questions.md` |
| Concrete next tasks | `next-actions.md` |

Also update `memory/index.md` with:
- protocol name
- last touched date
- current phase
- current status

### Phase 4 - Recall and Switching

When the user says things like:
- `switch to protocol X`
- `what do we know about X`
- `brief me on X`

Load that protocol memory first, then answer with:
1. what the protocol is
2. where we are in the workflow
3. key risks / findings / opportunities
4. next actions

---

## Memory Rules

- Never mix notes between protocols
- Label uncertain claims as hypotheses until verified
- If a belief changes, update the previous belief rather than silently overwriting history
- Keep memory concise and decision-oriented
- Treat memory as internal operating context, not as a substitute for fresh evidence
- For market-sensitive claims, memory can store prior conclusions, but live verification still overrides stale notes
