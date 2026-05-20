# Pitch — Mycelium Perpetual Pools
**Date:** 2026-05-20  
**Analyst:** Muzammil Siddiqui  
**Stage:** Evaluated  

---

## Internal Sales Brief
*This section is internal only. Never included in outreach.*

**Recommended service:** Targeted remediation consulting — new OracleWrapper deployment + pool migration guide  
**Price range:** $1,500–$3,000 (fixed scope, 50% upfront in USDC)  
**Conversion probability:** ~10–15% (protocol in wind-down, but responsible disclosure angle has genuine upside)  
**Fallback:** If they have an active new product, pivot — "here's what we found in Pools so you don't repeat it"

**Proposal scope if requested:**
- Updated OracleWrapper.sol with Chainlink Sequencer Uptime Feed check
- Deploy script for Arbitrum mainnet
- Pool migration guide (steps to point existing pools to fixed oracle)
- Written summary of remaining findings

**Contact search:** Check github.com/mycelium-ethereum README and CONTRIBUTING for a security disclosure email. Fallback: @mycelium_xyz on Twitter/X.

---

## Insight Extraction
*Internal only. Never sent.*

**Finding selected:** FINDING-001 HIGH — Missing Arbitrum L2 Sequencer Health Check  
**Why selected:** Highest severity, concrete business consequence, documented by the team themselves (GitHub Discussion #284)

**Business risk translation (Derivatives / oracle staleness):**  
"If Arbitrum's network experiences downtime, your upkeep mechanism runs on stale price data — pool balances get corrupted in a way that can't be cleanly unwound when the network comes back."

---

## Outreach Email
*This is the only thing that goes into the Gmail draft.*

**Subject:** quick note on Mycelium Pools

I reviewed the oracle integration in your Perpetual Pools contracts on Arbitrum and flagged something your team actually raised in your own GitHub back in 2021 but never closed out.

If Arbitrum's network experiences any downtime, your upkeep mechanism runs on stale price data — pool balances get corrupted in a way that's difficult to unwind cleanly, and there's still ~$183k sitting in those contracts.

I documented the specifics — want me to send over the summary?

Muzammil  
github.com/Webners1

---

## Gmail Draft
**To:** [find at github.com/mycelium-ethereum or mycelium.xyz security page]  
**Subject:** quick note on Mycelium Pools  
**Draft Created:** [pending Gmail OAuth setup]  
**Draft ID:** [pending]
