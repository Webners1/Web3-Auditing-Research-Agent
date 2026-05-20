# Sales Brief — Mycelium Perpetual Pools
**Date:** 2026-05-20  
**Stage:** Evaluated  
**Recommended Approach:** Responsible disclosure + targeted remediation offer  
**Confidence:** Medium-Low (wind-down protocol, ~10–15% response, ~5% conversion to paid)

---

## Lead Summary

| Field | Value |
|---|---|
| Protocol | Mycelium Perpetual Pools (formerly Tracer) |
| Chain | Arbitrum One |
| TVL | ~$183k (declining) |
| Bucket | HIGH (finding severity) |
| Status | Wind-down — UI shows "Close Positions" |
| Contact | @mycelium_xyz (Twitter) |

---

## Why This Is Worth an Outreach (Despite Wind-Down)

1. **$183k of user funds are at risk from an unpatched HIGH finding.** The team acknowledged the exact vulnerability in their own GitHub (Discussion #284, Dec 2021) and never fixed it.
2. The vulnerability (missing Arbitrum L2 sequencer health check) is a well-known class of issue — the fix is 20 lines of code, not a full re-audit.
3. Reaching out positions you as the person who found and can fix this — not as someone trying to sell a service.
4. If they have an active new product in development, this opens a door.

---

## Sales Brief

**Primary pain:** Missing L2 sequencer health check in OracleWrapper — if Arbitrum sequencer goes offline (which has happened), pool upkeep runs with stale Chainlink prices. On restoration, accumulated price delta drains the losing pool side. Their team discussed this in GitHub Discussion #284 in December 2021 and never shipped the fix.

**Why now:** Non-upgradeable contracts mean the fix requires new OracleWrapper deployment. Every day this is unaddressed with $183k in the pool is a day the risk is live. The longer the protocol runs in wind-down without fixing this, the more reputational risk accumulates.

**Proof points:**
- GitHub Discussion #284: team's own acknowledgment of the gap
- Code4rena Oct 2021 audit: keeper reward formula also broken (users depend on altruistic keepers)
- No re-audit in 3+ years
- GMX V2 and Synthetix implement the exact fix — this is solved, standard code

**Offer:** Targeted remediation consulting — not a full audit. Spec the fix, implement new OracleWrapper, write migration instructions. 2–3 days of work.

---

## Outreach Drafts

### Option A — Direct Message (Twitter/X or Telegram)

> Hey Mycelium team — I was reviewing Perpetual Pools contracts for a research piece and noticed Discussion #284 in your GitHub (the L2 sequencer health flag) is still unresolved.
>
> With $183k still in the pools, this is a live risk — Chainlink explicitly calls out that Arbitrum deployments need the sequencer uptime check or stale prices can execute during outages. GMX and Synthetix both have this fix deployed.
>
> I can spec and deliver a new OracleWrapper + migration guide in 2–3 days. Happy to share the full finding if it's useful regardless. [Name] — [contact]

---

### Option B — Email (if team email is findable)

> Subject: Unresolved L2 sequencer vulnerability in Perpetual Pools — quick fix available
>
> Hi [Name],
>
> I've been reviewing the Mycelium Perpetual Pools contracts as part of protocol research and wanted to flag something that's still open: the L2 sequencer health check your team discussed in GitHub Discussion #284 back in December 2021 was never implemented.
>
> With ~$183k still locked in the pools, this represents a live risk. When Arbitrum's sequencer goes offline, Chainlink oracles stop updating — but your contracts continue executing upkeep with stale prices. The Chainlink docs explicitly flag this for L2 deployments. GMX V2 and Synthetix both have the fix deployed.
>
> The fix is about 20 lines in OracleWrapper.sol, but because the contracts use a non-upgradeable clone pattern, it requires a new deployment and pool migration. I can spec and deliver this in 2–3 days.
>
> I'm happy to share the full finding regardless — no strings attached. If you have a new product in development, I'd also be glad to discuss what we saw in Pools to make sure it doesn't carry over.
>
> [Your name]  
> [Link to proof-of-work or brief bio]  
> [Contact: email, Telegram, Twitter]

---

### Option C — Responsible Disclosure Only (no ask)

> Hey team — your Perpetual Pools contracts are missing the Arbitrum L2 sequencer health check in OracleWrapper (your Discussion #284 from Dec 2021). $183k is still in the pools. Happy to share the full finding at [link/email]. No sell.

---

## Pitch Routing

| Response | Next Step |
|---|---|
| No response after 7 days | No follow-up — wind-down protocol |
| "Thanks, we know about it" | Ask if they have a new product — pivot pitch |
| "Can you spec the fix?" | Move to proposal: OracleWrapper remediation, $1,500–$3,000 |
| "Can you do a full audit?" | Full audit scope discussion — $5,000–$12,000 range |

---

## Proposal Outline (if requested)

**Scope:** Targeted OracleWrapper Remediation for Mycelium Perpetual Pools

**Deliverables:**
1. Updated `OracleWrapper.sol` with Chainlink Sequencer Uptime Feed check
2. Deploy script for new OracleWrapper on Arbitrum
3. Pool migration guide (steps for deploying new pools pointing to fixed oracle)
4. Written summary of other findings (FINDING-002 keeper rewards, FINDING-003 circuit breaker)

**Timeline:** 3–5 business days  
**Price range:** $1,500–$4,000 (targeted remediation; not a full audit)

**Not included:** Full audit of all contracts, frontend changes, new pool deployment execution (advisory only).

---

## Tracker Update

```tsv
mycelium-perpetual-pools	2026-05-20	Mycelium Perpetual Pools	Arbitrum	$183k	HIGH	Evaluated	Option A DM	audit-output/mycelium-perpetual-pools-diligence-20260520.md	Wind-down; responsible disclosure angle; check for new product
```
