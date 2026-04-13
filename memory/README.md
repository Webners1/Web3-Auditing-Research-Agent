# Protocol Memory

This directory stores structured working memory for each protocol the agent is handling.

## Goals

- keep multiple protocol engagements separate
- make it easy to resume work
- preserve decisions, findings, and founder context
- avoid repeating discovery on every session

## Structure

```text
memory/
  index.md
  protocols/
    [protocol-slug]/
      profile.md
      working-memory.md
      findings.md
      decisions.md
      open-questions.md
      next-actions.md
  templates/
```

## Rules

- one protocol per folder
- concise, decision-oriented notes
- uncertain statements are marked as hypotheses
- live market claims still require fresh verification
