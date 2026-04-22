# Mode: evaluate - Stage 3 Sales Brief

Build a **sales brief** from the completed stage-2 research handoff. This mode does not replace protocol diligence. It packages the diligence into a sales decision.

---

## Required Inputs

Before doing anything else, read:
1. `service-profile.md`
2. `modes/_profile.md`
3. `data/research-handoffs/{slug}.md`
4. The linked report from `../audit-output/`

If the handoff file is missing, incomplete, or its report path does not exist, stop and tell the user to run stage 2 first.

Required handoff fields:
- `**Protocol:**`
- `**Slug:**`
- `**Chain:**`
- `**Bucket:**`
- `**Report Type:**`
- `**Report Path:**`
- `**Status:** Research Complete`
- `**Recommended Service:**`
- `**Primary Pain:**`
- `**Pitch Hook:**`
- `**Proof Points To Use:**`
- `**Cautions:**`

---

## Goal

Turn stage-2 diligence into a stage-3 decision:
- is this lead worth pitching?
- what service should lead the conversation?
- which proof should be used first?
- what caution or disqualifier should be surfaced before outreach?

---

## Step 1 - Confirm Sales Readiness

From the handoff and report, extract:
- protocol name
- slug
- primary chain
- bucket
- report type
- report path
- recommended service
- primary pain
- pitch hook
- proof points to use
- cautions

Then answer:
- does the protocol still appear reachable and active?
- does the recommended service match `service-profile.md`?
- do the cautions make this a bad or risky lead?

If the service does not match your real proof, mark the lead `Not a Fit`.

---

## Step 2 - Build The Sales Brief

Write these sections:

### 1. Protocol Snapshot

| Field | Value |
|-------|-------|
| Protocol | |
| Chain | |
| Bucket | |
| Report type | |
| Stage-2 report | |
| Recommended service | |

### 2. Why This Lead Exists

One short paragraph that explains:
- the pain stage 2 found
- why it matters now
- why that pain maps to a service you actually sell

### 3. Buyer Hypothesis

State who you are likely selling to:
- founder
- core engineer
- product lead
- growth lead
- protocol ops

Then explain why that person is the likely owner of the problem.

### 4. Proof Angle

Choose the best 1-2 proof points from `service-profile.md` for this protocol and explain why they fit.

### 5. Risks And Cautions

Surface every caution from the handoff and add any sales-specific concern:
- anonymous team
- low budget confidence
- weak urgency
- crowded vendor situation
- governance or reputational risk

### 6. Recommended First Move

Choose one:
- cold DM
- cold email
- governance/forum reply
- warm-intro note
- watchlist only

Explain why this is the correct first move.

---

## Step 3 - Stage 3 Score

Score the lead using these categories:

| Category | Weight | What it measures |
|----------|--------|------------------|
| Urgency | 25% | How time-sensitive the pain is right now |
| Budget Confidence | 20% | Whether they look able and willing to pay |
| Service Fit | 25% | How well the pain maps to your strongest offer |
| Proof Leverage | 20% | How well your proof of work matches this case |
| Friction / Risk | 10% | Sales blockers and execution risk |

Rate each category `1-5`, compute the weighted score, and classify:
- `FIRE` - 4.5 to 5.0
- `STRONG` - 4.0 to 4.4
- `MODERATE` - 3.5 to 3.9
- `WATCH` - 3.0 to 3.4
- `SKIP` - below 3.0

If cautions are severe, lower the final verdict even if the numeric score looks high.

---

## Step 4 - Report Output

Write the sales brief to:

```text
reports/{NUM}-{slug}-{YYYY-MM-DD}.md
```

Required header:

```markdown
**Protocol:** [Name]
**Slug:** [slug]
**Chain:** [Chain]
**Bucket:** [Bucket]
**Research Handoff:** data/research-handoffs/{slug}.md
**Research Report:** ../audit-output/[file].md
**Recommended Service:** [Service]
**Score:** [X.X/5]
**Verdict:** [FIRE / STRONG / MODERATE / WATCH / SKIP]
**Status:** Evaluated
**Pitch:** ❌
```

Then append the full sales brief sections.

---

## Step 5 - Tracker Registration

Write one TSV file:

```text
batch/tracker-additions/{NUM}-{slug}.tsv
```

Format:

```text
{NUM}\t{DATE}\t{PROTOCOL}\t{CHAIN}\t{TVL_OR_NA}\t{BUCKET}\t{SCORE}/5\tEvaluated\t❌\t[{NUM}](reports/{NUM}-{slug}-{DATE}.md)\t{ONE-LINE SALES SUMMARY}
```

If TVL is not available in the handoff or report, write `n/a`.

Then remind the user:

```text
node scripts/merge-tracker.mjs
```

---

## Final Output To User

Summarize:
- protocol
- recommended service
- score
- verdict
- first move
- report path

If the verdict is `WATCH` or `SKIP`, explicitly recommend against immediate outreach.
