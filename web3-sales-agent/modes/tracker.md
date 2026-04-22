# Mode: tracker — Pipeline Status Overview

Read and display `data/leads.md`, the master pipeline tracker.

---

## Display Format

Show the current pipeline as a table:

```markdown
| # | Date | Protocol | Chain | TVL | Bucket | Score | Status | Pitch | Report |
```

## Status Legend

| Status | Meaning |
|--------|---------|
| `Evaluated` | Report done, no outreach yet |
| `Pitched` | Cold DM / email sent |
| `Responded` | Team replied to outreach |
| `Call Scheduled` | Discovery call booked |
| `Proposal Sent` | Formal proposal delivered |
| `Negotiating` | Active discussion |
| `Closed Won` | Engagement signed |
| `Closed Lost` | Lost or ghosted after reply |
| `Not a Fit` | Below threshold or deal-breaker |
| `Watch` | Revisit in 30–60 days |

## Summary Statistics

After the table, show:

```
## Pipeline Summary — {DATE}

Total leads: {N}
By status:
  - Evaluated: {N}
  - Pitched: {N}
  - Responded: {N}
  - Call Scheduled: {N}
  - Proposal Sent: {N}
  - Negotiating: {N}
  - Closed Won: {N}
  - Closed Lost: {N}
  - Not a Fit: {N}
  - Watch: {N}

By bucket:
  - Ghost Leads: {N}
  - Leaky Bucket: {N}
  - Security Risk: {N}
  - Chain Migrators: {N}

Avg score (Evaluated+): {X.X}/5
Conversion rate (Pitched → Closed Won): {X}%
Hottest open lead: {Protocol} — {STATUS} since {N} days ago
```

## Status Update

If the user says "update [Protocol] to [status]" or "mark [Protocol] as [status]":
- Find the matching row in `data/leads.md`
- Update the Status column
- Add a note with the date of the change: `[Status changed {DATE}]`
- If updating to `Pitched`: ask "What channel? (Twitter DM / Email / Telegram / Forum)" and record in Notes

## Watch List Highlights

If there are any leads in `Watch` status older than 30 days:
> "⚠️ These Watch leads are aged 30+ days. Check if their situation has changed before re-approaching:
> [List protocols with dates last evaluated]"
