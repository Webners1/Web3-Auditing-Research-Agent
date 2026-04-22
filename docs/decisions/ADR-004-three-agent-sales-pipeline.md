# ADR-004: Enforce the Three-Agent Web3 Sales Pipeline

## Status

Accepted

## Context

The workspace now contains three distinct agents:

1. `career-ops-source`
2. `web3-auditing-agent`
3. `web3-sales-agent`

Before this ADR, the sales agent still contained instructions that let it discover, evaluate, and pitch leads without a mandatory research handoff from the main repo. That created a bypass around the intended order.

## Decision

The required flow is:

```text
career-ops-source
  -> web3-sales-agent/data/pipeline.md
  -> web3-auditing-agent
  -> audit-output/*.md + web3-sales-agent/data/research-handoffs/{slug}.md
  -> web3-sales-agent
  -> reports/*.md + output/* + tracker updates
```

### Stage responsibilities

- Stage 1 finds raw leads only.
- Stage 2 owns protocol diligence and writes the research handoff.
- Stage 3 owns sales packaging and outreach only after the handoff exists.

### Handoff contract

Stage 2 must write one file per protocol to:

```text
web3-sales-agent/data/research-handoffs/{slug}.md
```

Required fields:
- `Protocol`
- `Slug`
- `Chain`
- `Bucket`
- `Lead Source`
- `Report Type`
- `Report Path`
- `Status: Research Complete`
- `Recommended Service`
- `Primary Pain`
- `Pitch Hook`
- `Proof Points To Use`
- `Cautions`

## Consequences

### Positive

- The intended order is explicit and verifiable.
- The sales agent can no longer silently replace the research agent.
- A single handoff file gives stage 3 a stable contract.

### Tradeoffs

- Stage 2 must now do one additional write per researched lead.
- Stage 3 will refuse to pitch when the handoff is missing or incomplete.
