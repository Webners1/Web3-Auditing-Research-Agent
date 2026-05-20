# Sales Brief — Mycelium Perpetual Pools
**Date:** 2026-05-20  
**Analyst:** Muzammil Siddiqui  
**Stage:** Evaluated  
**Approach:** Responsible disclosure + targeted remediation offer  
**Conversion probability:** ~10–15% (wind-down protocol)

---

## Lead Summary

| Field | Value |
|---|---|
| Protocol | Mycelium Perpetual Pools (formerly Tracer) |
| Chain | Arbitrum One |
| TVL | ~$183k (declining) |
| Severity | HIGH finding |
| Status | Wind-down — UI shows "Close Positions" |
| Contact | @mycelium_xyz (Twitter) |
| GitHub | mycelium-ethereum |

---

## Why Send This Outreach

1. **Their own team documented the vulnerability** — GitHub Discussion #284 (Dec 2021) acknowledges the missing L2 sequencer health check. It was never fixed. That makes this a warm lead, not a cold pitch — they already know the problem exists.
2. **$183k of user funds are actively at risk.** Not a hypothetical — if Arbitrum sequencer goes offline (it has before), pool upkeep runs with stale Chainlink prices and drains the losing side on restoration.
3. **The fix is 20 lines of code.** But because the contracts are non-upgradeable minimal proxies, it requires a new OracleWrapper deployment and pool migration. That's where the paid work is.
4. **If they have a new product,** the disclosure opens a door — "here's what we found in your old contracts so you don't repeat it."

---

## Primary Pain
Missing Arbitrum L2 Sequencer Health Check in OracleWrapper. Their GitHub Discussion #284 acknowledged it in December 2021. Unresolved for 3+ years. $183k in non-upgradeable contracts.

## Pitch Hook
"Your team raised this in GitHub Discussion #284 back in 2021 and never shipped the fix. I'm a blockchain developer — I can spec and deliver the new OracleWrapper in 2 days. Happy to share the full finding regardless."

---

## Outreach Drafts

### Option A — Twitter/X DM (Recommended — under 100 words)

Subject: N/A (DM)

> Hey Mycelium team — I reviewed the Perpetual Pools contracts and noticed Discussion #284 in your GitHub (L2 sequencer health check) is still unresolved. With $183k still in the pools, this is a live risk — Chainlink explicitly calls this out for Arbitrum deployments, and GMX + Synthetix both have the fix shipped.
>
> I'm Muzammil, Senior Blockchain Dev at Zybra Labs (20+ DApps, Cyfrin security certified). I can spec and deliver a new OracleWrapper + migration guide in 2 days. Happy to share the full finding regardless — no pressure.
>
> muzammilsiddiqui001@gmail.com | github.com/Webners1

---

### Option B — Email

**To:** [team@mycelium.xyz or security contact — find on their site/GitHub]  
**Subject:** Unresolved L2 sequencer vulnerability in Perpetual Pools — 2-day fix available

> Hi Mycelium team,
>
> I've been reviewing the Perpetual Pools contracts and found that the L2 sequencer health check your team discussed in GitHub Discussion #284 (December 2021) was never implemented.
>
> With ~$183k still locked in the pools, this is a live exposure. When Arbitrum's sequencer goes offline, Chainlink oracles stop updating — but your PoolKeeper continues calling upkeep with stale prices. On sequencer restoration, the accumulated price delta drains the losing pool side in one cycle. GMX V2 and Synthetix both have this specific fix deployed.
>
> The fix is a new OracleWrapper deployment (~20 lines) plus a pool migration guide. Because the contracts use a non-upgradeable clone pattern, that's the only path to resolution.
>
> I'm Muzammil Siddiqui — Senior Blockchain Developer at Zybra Labs, Cyfrin-certified in smart contract security, with 20+ DApps shipped as a contractor across Ethereum, Arbitrum, and Base. I can spec and deliver the fix in 2 days.
>
> Happy to share the full finding regardless — no strings attached. If you have an active new product in development, I'd also be glad to share what we saw in Pools so it doesn't carry forward.
>
> Muzammil Siddiqui  
> muzammilsiddiqui001@gmail.com  
> github.com/Webners1  
> Senior Blockchain Developer, Zybra Labs

---

### Option C — Responsible Disclosure Only (no sell)

> Hey — your Perpetual Pools contracts are missing the Arbitrum L2 sequencer health check (Discussion #284, Dec 2021, still unresolved). $183k is still in the pools. Full finding at muzammilsiddiqui001@gmail.com — no sell.
> — Muzammil, github.com/Webners1

---

## After They Respond

| Response | Next Step |
|---|---|
| No reply after 7 days | Close lead — no follow-up for wind-down protocol |
| "Thanks, aware of it" | Ask: "Do you have a new product in development? Happy to apply these findings there." |
| "Can you spec the fix?" | Proposal: OracleWrapper remediation — $1,500–$3,000 |
| "Can you do a full review?" | Full audit scope: $4,000–$8,000 for full contract suite |
| "Here's our new product" | Full diligence run on new protocol — restart pipeline |

---

## Proposal Outline (if requested)

**Scope:** OracleWrapper Remediation — Mycelium Perpetual Pools on Arbitrum

**Deliverables:**
1. New `OracleWrapper.sol` with Chainlink Sequencer Uptime Feed check (Arbitrum: `0xFdB631F5EE196F0ed6FAa767959853A9F217697D`)
2. Deploy script for Arbitrum mainnet
3. Pool migration guide: steps to deploy new pools pointing to the fixed oracle
4. Written summary of remaining findings (keeper reward formula, circuit breaker gap, fee precision)

**Timeline:** 2–3 business days after kickoff  
**Price:** $1,500–$3,000 (targeted remediation — not a full audit)  
**Payment:** 50% upfront (USDC), 50% on delivery

**Not included:** Full audit, frontend changes, deploying new pools on your behalf (advisory only)

---

## Gmail Draft

**Contact Email:** [find at github.com/mycelium-ethereum or mycelium.xyz — check README/CONTRIBUTING for security email]  
**Draft created:** [pending Gmail OAuth setup]  
**Draft ID:** [pending]
