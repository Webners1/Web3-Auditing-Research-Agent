Load `skills/protocol-diligence/SKILL.md`.

Runs the full end-to-end engagement: product review → contract discovery → security audit → remediation planning → architecture advisory → CEO strategy → executive package. Use when you want a complete picture of a protocol: what is broken, how to fix it, how to improve it, and where to take it strategically.

**Argument:** $ARGUMENTS (optional — protocol name)

---

## What Runs (in order)

1. **Product assessment** — maps the product surface: frontend, backend, trust assumptions, user journey, contract discovery
	- includes one primary workflow pass and one failure-path UX pass
	- includes smart-wallet / account-abstraction readiness checks when claims exist
2. **Security audit** — Slither + Aderyn + 8-agent parallel analysis of all in-scope contracts
3. **Remediation plan** — best-practice fix recommendations for all findings
4. **Architecture review** — upgrade paths, integration opportunities, L2 strategy
5. **Market strategy** — ecosystem positioning, roadmap, what to build next
	- uses function-matched comparable set and one one-curve-ahead benchmark
6. **Executive package** — combined summary across all phases

Outputs:
- `audit-output/[project]-product-[YYYYMMDD].md`
- `audit-output/[project]-audit-[YYYYMMDD].md`
- `audit-output/[project]-remediation-[YYYYMMDD].md`
- `audit-output/[project]-arch-[YYYYMMDD].md`
- `audit-output/[project]-strategy-[YYYYMMDD].md`
- `audit-output/[project]-diligence-[YYYYMMDD].md`

---

## After Full Diligence

- Export everything to PDF: `/report diligence`
- Optional deep UX pass: `/ux-audit [protocol or url]`
- Optional smart wallet readiness pass: `/aa-readiness [protocol]`
- Expand major security findings: `/expand-security-audit [protocol or report]`
- Expand business and strategy depth: `/expand-business [protocol or question]`
- Expand UI/UX journey depth: `/expand-uiux [protocol, url, or report]`
- Save to protocol memory: use `/start [protocol]` to check memory state

---

## Usage Examples

```
/diligence
/diligence Morpho Blue
/diligence this protocol
```
