# Mode: compare — Multi-Lead Ranking

Compare and rank multiple protocol leads to prioritize pitching effort.

---

## When to Use

Run this when you have 3+ evaluated leads and need to decide which to pitch first.

---

## Comparison Table

For each lead, pull from its stage-3 sales brief:

```markdown
| # | Protocol | Chain | TVL | Bucket | Score | Treasury | Urgency | Recommended Action |
|---|----------|-------|-----|--------|-------|----------|---------|-------------------|
| 1 | [Best lead] | | | | | | 🔴 HIGH | Pitch today |
| 2 | [Second best] | | | | | | 🔴 HIGH | Pitch this week |
| 3 | [Third] | | | | | | 🟡 MEDIUM | Pitch next week |
...
```

## Ranking Logic

Rank by this priority order (not just by score):

1. **FIRE urgency** (Leaky Bucket declining now, Chain Migrator < 30 days post-launch, Security Risk with imminent V2) — always top of list regardless of score
2. **Score** (4.5+ before 4.0+ before 3.5+)
3. **Treasury size** (can they actually pay?)
4. **Bucket fit** (do you have a strong proof point for their specific bucket?)
5. **Chain** (is it one of your primary chains where you have credibility?)

## Decision Output

After the table:
> "Based on urgency and fit, pitch these in this order:
> 1. [Protocol A] — [specific reason: declining TVL + V2 imminent + audit gap]
> 2. [Protocol B] — [specific reason]
> 3. [Protocol C] — [specific reason]
>
> Want me to generate pitches for all three?"
