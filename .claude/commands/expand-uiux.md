Load `skills/product-assessor/SKILL.md`.

Expands the UI/UX and app-flow audit into a detailed journey and conversion-readiness review.

**Argument:** $ARGUMENTS (optional — protocol name, URL, or product report path)

---

## What Runs

1. Resolve target product context:
   - Use URL if supplied
   - Use provided product report path if supplied
   - Otherwise use latest `audit-output/[project]-product-[YYYYMMDD].md`
2. Walk one primary conversion flow end-to-end:
   - Connect -> first key action -> confirmation -> post-action state
3. Walk at least two failure paths:
   - Wrong network / rejected signature / failed transaction / stale quote
4. Measure friction:
   - Click and decision count
   - Error recoverability
   - Trust clarity at signature and approval points
5. Evaluate wallet experience:
   - EOA baseline behavior
   - Smart-wallet/AA behavior only if applicable
6. Build prioritized UX fix backlog with expected conversion or trust impact
7. Write output to `audit-output/[project]-uiux-expand-[YYYYMMDD].md`

---

## Output Guidance

- Classify issues by user impact and recovery cost
- Include concrete UI copy/state changes, not just abstract principles
- Tie severe friction to business impact (activation, retention, or trust)

---

## Usage Examples

```
/expand-uiux
/expand-uiux mars-poolin
/expand-uiux https://mars.poolin.fi/
/expand-uiux audit-output/mars-poolin-product-20260413.md
```
