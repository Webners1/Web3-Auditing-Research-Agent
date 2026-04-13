# ADR-003: Add source-routed research and client-report export

## Status
Accepted

## Date
2026-04-09

## Context

The agent already had domain skills and report formats, but it still lacked two critical pieces:
- a strict source-routing discipline that keeps research focused on Web3-specific sources before broad search
- a client-report export path that turns Markdown deliverables into shareable PDF files

Because this is a special-purpose agent, it should begin from a curated registry of official and Web3-native sources rather than wander across generic web search results.

## Decision

Add:
- a central research source registry with exact URLs and research order
- a `client-reporting` skill that turns report drafts into client-ready deliverables
- a standard `scripts/render_report.py` HTML and PDF export path
- report expectations that require exact source links in the final deliverable

## Consequences

- the agent now has a narrower and more reliable research path
- report generation becomes an explicit workflow instead of an implied formatting step
- PDF export depends on a local Chrome or Edge installation, which is acceptable for this workspace
