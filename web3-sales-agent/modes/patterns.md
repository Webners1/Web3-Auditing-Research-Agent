# Mode: patterns - Conversion Pattern Analyzer

Analyze the stage-3 sales funnel to see what is converting and where the process is leaking.

---

## Minimum Threshold

Before running analysis, check whether `data/leads.md` has at least 10 entries beyond `Evaluated`.

If not, tell the user there is not enough stage-3 outcome data yet.

---

## Analysis Dimensions

### 1. Funnel Conversion

Report counts and rates for:
- `Research Complete`
- `Evaluated`
- `Pitched`
- `Responded`
- `Call Scheduled`
- `Proposal Sent`
- `Negotiating`
- `Closed Won`
- `Closed Lost`

Key ratios:
- pitch -> response
- response -> call
- call -> proposal
- proposal -> close

### 2. Bucket Performance

For each bucket:
- pitched count
- response count
- close count
- conversion rate
- average score

### 3. Chain Performance

Show which chains produce:
- the highest response rates
- the best close rates
- the most research-complete leads that never get pitched

### 4. Score Vs Outcome

Compare score bands against actual outcomes to see whether stage-3 scoring is calibrated well.

### 5. Pitch Channel Performance

If the tracker notes include channel data, compare:
- Twitter/X DM
- email
- governance/forum
- Telegram

### 6. Timing Analysis

Measure:
- average days from `Research Complete` to `Evaluated`
- average days from `Evaluated` to `Pitched`
- average days from `Pitched` to `Responded`
- stalled leads that need follow-up

---

## Recommendations

Give 3-5 concrete recommendations.

Examples:

```text
1. Security Risk leads are converting better than Ghost Leads.
   -> Ask stage 1 to bias discovery toward audit-gap and upgrade-window signals.
   -> Tune ../career-ops-source/portals.yml rather than stage-3 pitch copy first.

2. Base leads are getting replies but not calls.
   -> Rework the CTA and offer framing for Base projects.

3. Too many Research Complete leads are sitting unpitched.
   -> The bottleneck is stage 3 throughput, not discovery.
```

---

## Save Report

Write the analysis to:

```text
reports/pattern-analysis-{YYYY-MM-DD}.md
```
