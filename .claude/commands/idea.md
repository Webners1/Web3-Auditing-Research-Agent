Load `skills/founder-copilot/SKILL.md`.

Pressure-tests an idea conversationally. Gives an immediate product, security, and business reaction without a formal report. Use when you want to think through a direction before committing.

**Argument:** $ARGUMENTS — the idea or question, optionally prefixed with a protocol name.

Format examples:
- `[protocol]: [idea]`
- `[idea]` (no protocol context needed)

---

## What It Does

Responds through five lenses:
1. **Verdict** — promising / mixed / weak
2. **Why it could work** — user value, technical leverage, distribution angle
3. **Why it could fail** — security risk, market timing, complexity, weak moat
4. **Better version** — a refined, more realistic variant of the idea
5. **Next test** — what to validate before committing

Keeps the first response tight and high-signal. Expands on any lens if you ask for depth.

If the idea becomes concrete, routes to the right skill automatically:
- Product/trust mapping → `/research`
- Smart contract question → `/audit`
- Fix needed → `/fix`
- Architecture design → `/arch`
- Market strategy → `/strategy`

---

## Usage Examples

```
/idea add a lending market to our AMM
/idea Uniswap v4: build a hooks-based options protocol on top
/idea is a cross-chain yield aggregator still a good idea in 2026
/idea launch a governance token before or after product-market fit
/idea challenge: we think deploying on Solana first makes sense
```
