Load `skills/ceo-advisor/SKILL.md`.
Load `skills/protocol-diligence/references/research-source-registry.md`.

Expands business and strategy analysis with deeper competitive stack, execution realism, and 2026 market-readiness targets.

**Argument:** $ARGUMENTS (optional — protocol name, strategy question, or strategy report path)

---

## What Runs

1. Resolve target strategy context:
   - Use provided strategy report path if supplied
   - Otherwise use latest `audit-output/[project]-strategy-[YYYYMMDD].md`
2. Refresh market evidence from live sources (DefiLlama, L2BEAT, Token Terminal, Dune where available)
3. Rebuild comparable set by function (not fame):
   - Direct peers
   - Adjacent alternative
   - One-curve-ahead benchmark
4. Expand comparative stack analysis:
   - Where current stack is lagging
   - What to adopt and what to avoid
   - Implementation dependencies and execution risk
5. Build 2026 readiness targets for business-critical dimensions:
   - Narrative clarity and category fit
   - Distribution readiness
   - Revenue durability
   - Docs/GitHub/presentation trust quality
6. Write output to `audit-output/[project]-business-expand-[YYYYMMDD].md`

---

## Output Guidance

- Include baseline, 90-day, and 12-month targets for key operating metrics
- Separate FACT vs INFERENCE vs HYPOTHESIS claims
- Each recommendation must include what to do, what not to do, and dependency risk

---

## Usage Examples

```
/expand-business
/expand-business mars-poolin
/expand-business go-to-market on Base vs Arbitrum
/expand-business audit-output/mars-poolin-strategy-20260413.md
```
