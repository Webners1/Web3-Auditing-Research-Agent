Load `skills/client-reporting/SKILL.md`.

Exports a completed analysis as a styled HTML and PDF client deliverable. Run this after any audit, architecture review, strategy memo, or full diligence to produce something you can send to a client, investor, or team.

**Argument:** $ARGUMENTS — report type and optional file path.

Types: `product`, `security`, `architecture`, `business`, `diligence`

---

## What It Does

1. Identifies the most recent matching report in `audit-output/`
2. Applies the client-facing format (clean, professional, source-linked)
3. Runs `scripts/render_report.py` to produce:
   - `audit-output/[report-file].html`
   - `audit-output/[report-file].pdf`
4. Confirms the PDF was created and the sources appendix is complete
5. Verifies the selected report includes current required intelligence sections for that report type

---

## Usage Examples

```
/report security
/report architecture
/report business
/report diligence
/report product
/report security audit-output/myprotocol-audit-20260413.md
```

---

## Requirements

Chrome or Edge must be installed for PDF export. HTML is always produced regardless.

If PDF export fails, the HTML version is still usable for sharing or printing.
