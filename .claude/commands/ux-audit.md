Load `skills/product-assessor/SKILL.md`.

Runs a focused UX and wallet-flow assessment for a protocol or app journey. This command is product-first and should be used to identify conversion friction, trust breakpoints, and failure-path quality.

**Argument:** $ARGUMENTS (protocol name or URL)

---

## What Runs

1. Load protocol context and product surface
2. Walk one primary user flow end to end
3. Walk one failure path (reject/invalid/mismatch path)
4. Record friction points, trust breaks, and recovery quality
5. If installed, use `ux-audit` skill for deeper browser-driven walkthroughs
6. Write findings into the product report section set and/or append to active diligence notes

---

## Output Guidance

- Classify issues by user impact (`Critical` / `High` / `Medium` / `Low`)
- Include actionable fixes that the current team can implement
- Treat severe UX friction as business risk when it impacts activation or retention

---

## Usage Examples

```
/ux-audit
/ux-audit mars-poolin
/ux-audit https://mars.poolin.fi/
```

For a deeper journey teardown and prioritized UX backlog:

```
/expand-uiux [protocol or url]
```
