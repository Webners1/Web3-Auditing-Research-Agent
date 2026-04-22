# Mode: pitch - Outreach Generator

Generate outreach only after stage 2 is complete and stage 3 has enough context to pitch responsibly.

---

## Required Inputs

Read:
1. `service-profile.md`
2. `modes/_profile.md`
3. `data/research-handoffs/{slug}.md`
4. the linked stage-2 report from `../audit-output/`
5. the stage-3 sales brief in `reports/` if one exists

If the handoff is missing, stop and tell the user that stage 2 must run first.

If the stage-3 sales brief is missing, run `evaluate` first so the pitch is grounded in a sales decision rather than raw diligence alone.

---

## Ground Rules

- Never write a generic pitch.
- Never pretend you personally discovered facts that came from stage 2. Reference them accurately.
- Use the handoff's `Pitch Hook`, `Recommended Service`, `Proof Points To Use`, and `Cautions` as the primary framing inputs.
- If the sales brief verdict is `WATCH` or `SKIP`, strongly recommend not pitching yet.

---

## Step 1 - Choose Pitch Type

Map user intent to one of these:
- Cold DM
- Cold email
- Full proposal
- Governance/forum reply
- Discovery call prep note

If the user does not specify, default to the lowest-friction option that fits the lead:
- DM for urgent or founder-led leads
- email for more formal or enterprise-leaning leads

---

## Step 2 - Build The Message

Every pitch must contain:
1. one specific observation from the handoff or stage-2 report
2. one concrete proof point from `service-profile.md`
3. one offer matched to the recommended service
4. one low-friction ask

Use this structure:

### Cold DM

```text
Opening: specific pain or milestone from the handoff
Middle: one relevant proof point
Close: one small ask
```

### Cold Email

```text
Subject: specific pain or milestone
Body line 1: what you noticed
Body line 2: why it matters now
Body line 3: your most relevant proof
Body line 4: exact offer
Body line 5: single CTA
```

### Proposal

Only write a proposal when:
- the user explicitly asks for it, or
- the protocol has already engaged

Structure:
- problem statement
- proposed scope
- deliverables
- timeline
- investment
- why us
- next steps

---

## Step 3 - Respect Cautions

Before finalizing, check the handoff `Cautions:` section.

If cautions indicate:
- reputational risk
- weak budget
- no real urgency
- weak service fit

then either:
- soften the ask, or
- recommend waiting instead of sending.

Do not bury serious cautions.

---

## Step 4 - Output

1. Show the pitch in a code block.
2. Add these notes:
   - `What to personalize before sending`
   - `Why this angle fits`
   - `Follow-up plan`
3. Ask whether to save it to:

```text
output/{slug}-pitch-{YYYY-MM-DD}.md
```

---

## Step 5 - Tracker Update

If the user confirms the pitch was sent:
- update the status in `data/leads.md` to `Pitched`
- record the channel and date in Notes
- append a follow-up row to `data/follow-ups.md`

Never mark a lead as pitched unless the user confirms it.
