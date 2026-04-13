Load `skills/ceo-advisor/SKILL.md`.

Delivers market-aware, business-oriented advice for a protocol team. Covers: ecosystem positioning, roadmap sequencing, what to build next, which chains to target, monetization, distribution, and narrative. Always verifies current market conditions before advising — does not give advice from stale memory.

**Argument:** $ARGUMENTS (optional — protocol name or question)

Examples:
- `Morpho Blue`
- `what should we build next`
- `go to market for a lending protocol on Base`
- `how does this compare to Aave`

---

## What Runs

1. Live market scan: current state of the protocol's category (DefiLlama, L2BEAT)
2. Builds a function-matched comparable set (direct peers + adjacent alternative + one-curve-ahead benchmark)
3. Runs positioning framing (competitive alternatives, differentiated value, best-fit user)
4. Evaluates: market timing, distribution, defensibility, monetization, ecosystem fit, UX conversion friction
5. Produces prioritized recommendations: NOW / NEXT / LATER with evidence confidence tags
6. Captures category signals and sentiment with source-backed interpretation
7. Writes strategy memo to `audit-output/[project]-strategy-[YYYYMMDD].md`

---

## After Strategy

- For the full executive package: `/diligence`
- For deeper competitive and roadmap analysis: `/expand-business`
- For a client-ready PDF: `/report business`

---

## Usage Examples

```
/strategy
/strategy Morpho Blue
/strategy what should we build next
/strategy go to market for a perpetuals protocol on Arbitrum
```
