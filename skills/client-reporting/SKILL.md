# Web3 Client Reporting and PDF Export

Turns agent findings into client-ready reports for security, architecture, business proposition, and full diligence. Use when the user wants a shareable deliverable rather than just chat output. Produces Markdown first, then exports styled HTML and PDF.

**Trigger phrases:** `create report`, `export report`, `make this client ready`, `security report`, `architecture report`, `business proposition report`, `export pdf`, `client deliverable`, `board memo`

---

## Report Types

Supported report families:
- Security audit report
- Architecture advisory report
- Business proposition / strategy report
- Full protocol diligence report

Load these before writing:
- `references/client-report-style.md`
- `references/source-citation-policy.md`
- `../protocol-diligence/references/research-source-registry.md`

Then load the relevant format file:
- Security -> `../web3-audit/references/report-format.md`
- Architecture -> `../arch-advisor/references/report-format.md`
- Business proposition -> `../ceo-advisor/references/report-format.md`
- Full diligence -> `../protocol-diligence/references/report-format.md`

---

## Execution Pipeline

### Phase 1 - Choose Report Type

Decide which report the user wants:
- `security`
- `architecture`
- `business`
- `diligence`

If the user asks vaguely for a `report`, pick the narrowest report that fits the request and say what you assumed.

### Phase 2 - Build The Markdown Report

Write the report in Markdown first using the selected format.

Rules:
- keep the tone professional and decisive
- include exact source links in a final `Sources` or `Appendix: Sources` section
- avoid unsupported claims
- keep the report client-facing, not prompt-facing

### Phase 3 - Export To HTML And PDF

After writing the Markdown file, run:

```bash
py -3 scripts/render_report.py audit-output/[report-file].md
```

This creates:
- `audit-output/[report-file].html`
- `audit-output/[report-file].pdf`

### Phase 4 - Final Check

Before handing the report to the user:
- confirm the PDF was created
- confirm the report includes exact external source links
- confirm the report does not rely on broad unsupported market statements

---

## Reporting Rules

- Markdown is the source of truth; HTML and PDF are export artifacts
- Every client report that uses external research must include linked sources
- Prefer one strong report over multiple overlapping documents unless the user asked for a bundle
- Business proposition reports must connect strategy to execution reality
- Architecture reports must state both the gains and the complexity costs
- Security reports must keep proof discipline and severity calibration intact
