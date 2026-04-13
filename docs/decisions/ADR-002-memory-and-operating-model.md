# ADR-002: Add protocol memory, command-style interaction, and scenario playbooks

## Status
Accepted

## Date
2026-04-09

## Context

The repo had domain skills for product review, security audit, remediation, architecture, and strategy, but three important operating gaps remained:
- no explicit command-style interaction model for idea sharing in chat
- no structured memory system for handling multiple protocols at once
- no detailed statement of personality, evolution loop, or behavior under different scenarios

Without these, the agent risks behaving like a one-shot analyst instead of an ongoing protocol advisor.

## Decision

Add:
- `founder-copilot` for conversational idea intake and pressure-testing
- `protocol-memory` for per-protocol working memory
- a `memory/` directory structure for active context storage
- command-style prompt guidance in the constitution and README
- scenario playbooks and personality rules in the constitution

## Consequences

- the agent can now maintain separate context across multiple engagements
- operators get a clearer way to interact with the system through chat
- future development should include automating memory file creation and richer session summaries
