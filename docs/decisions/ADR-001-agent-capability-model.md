# ADR-001: Expand the agent from contract auditor to full Web3 diligence system

## Status
Accepted

## Date
2026-04-09

## Context

The repository started with two strong capabilities:
- smart contract security audit
- architecture advisory

That foundation was useful, but it left major gaps for real-world protocol engagements:
- no dedicated product-level assessment before entering contract audit
- no formal remediation layer to choose the best fix after findings
- no explicit founder / CEO strategy layer for market-aware recommendations
- no single orchestrated flow tying product review, audit, fixes, architecture, and business advice together
- `arch-advisor` referenced supporting files that did not yet exist

The intended direction for the agent is broader than pure security. It should think like a Web3 engineer and a founder: specific, practical, and aware of both technical and market trade-offs.

## Decision

Expand the capability model into six domains:
1. Product assessment
2. Security auditing
3. Remediation engineering
4. Architecture advisory
5. CEO / market strategy
6. Executive reporting

Implement that direction by:
- adding `product-assessor`
- adding `remediation-architect`
- adding `ceo-advisor`
- adding `protocol-diligence` as the end-to-end orchestrator
- filling in the missing `arch-advisor` references
- updating the master constitution and README to reflect the new scope

## Alternatives Considered

### Keep the repo focused only on contract audits
- Pros: simpler scope, less maintenance
- Cons: misses the actual product and business context that determines whether findings matter and what should be built next
- Rejected because the target use case is broader than code review

### Fold everything into one giant skill
- Pros: fewer files, simpler discovery
- Cons: harder to maintain, too much context in one place, weaker specialization
- Rejected because the workflow is naturally multi-stage

### Add business advice inside `arch-advisor`
- Pros: fewer skills
- Cons: mixes structural engineering advice with live market and founder strategy, which have different evidence requirements
- Rejected because market advice should be its own explicit phase

## Consequences

- The repo now models the full engagement lifecycle more realistically
- Future work should focus on richer references, example reports, and optional automation around report generation
- Market strategy output must use live-source verification because those facts change quickly
