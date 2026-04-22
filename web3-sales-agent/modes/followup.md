# Mode: followup — Follow-up Cadence Tracker

Tracks follow-up timing for all active leads, flags overdue outreach, and generates tailored follow-up messages.

---

## Cadence Rules

| Status | Follow-up window | Action |
|--------|-----------------|--------|
| `Pitched` (cold DM/email) | Follow up after 5–7 days if no response | One follow-up, then mark Watch |
| `Responded` | Follow up within 48 hours | Don't let warm leads cool |
| `Call Scheduled` | Reminder day before, recap same day | |
| `Proposal Sent` | Follow up after 3–5 business days | Gentle nudge — "any questions?" |
| `Negotiating` | Follow up within 2 days of last message | Keep momentum |
| `Watch` | Check-in after 30 days | Check if their situation has changed |

---

## Follow-up Dashboard

Read `data/leads.md` and calculate days since last status change with today's date.

Display:

```
Follow-up Dashboard — {DATE}
{N} active leads, {N} require action today

| Priority | Protocol | Chain | Status | Days | Action |
|----------|----------|-------|--------|------|--------|
| 🔴 URGENT | ... | ... | Responded | 2d | Reply within 24h |
| 🔴 OVERDUE | ... | ... | Pitched | 9d | Follow-up needed now |
| 🟡 DUE | ... | ... | Proposal Sent | 4d | Send gentle nudge |
| 🟢 ON TRACK | ... | ... | Pitched | 3d | Follow up in 2 days |
| ⚪ WATCH | ... | ... | Watch | 32d | Check if situation changed |
```

---

## Follow-up Message Generation

For each **OVERDUE** or **URGENT** lead:

1. Read the stage-3 sales brief from `reports/` (for protocol context and your original pitch angle)
2. Read `service-profile.md` (for relevant proof points)
3. Read `modes/_profile.md` (for tone and objection scripts)
4. Check their recent Twitter/X activity (browser_navigate) — has anything changed since your last touch?

### First Follow-up Template (Pitched, no response, day 6–8)

```
Subject: Re: [same subject as original] / Re: [same DM thread]

Hey [team name],

Just checking in on this — wanted to share one more quick thing:

[New, relevant observation since the first pitch — recent TVL movement, a competitor announcement, 
 their V2 news, or a live UX issue you spotted this week. Make it feel timely, not copy-paste.]

Still happy to [specific low-friction offer from original pitch].

[Name]
```

**Rules:**
- Do NOT just say "following up on my previous message"
- Add new information — a timely hook that shows you stayed interested in their protocol
- Keep it shorter than the original pitch
- One follow-up maximum per cold lead. If still no response → mark Watch

### Re-approach after Watch (30+ days)

```
Subject: [Protocol] — update on [chain] or [relevant market event]

Hey [team name],

I came across [specific recent development — their V2 tweet, a competitor exploit, their chain's TVL surge]
and thought of you.

Back in [original pitch date] I had mentioned [recall your specific offer briefly]. Still stands.

If timing is better now, I'm around.

[Name]
```

---

## Update `data/follow-ups.md`

After generating any follow-up draft, append to `data/follow-ups.md`:

```markdown
| Date | Protocol | Type | Channel | Sent? | Response? | Notes |
|------|----------|------|---------|-------|-----------|-------|
| {TODAY} | [Protocol] | First follow-up | Twitter DM | ❌ | — | Drafted — user to review |
```

If the user confirms they sent it, update `Sent?` to ✅.
