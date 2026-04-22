# My Service Profile Template
# Copy this to modes/_profile.md and fill in your details.
# This file is NEVER auto-updated — it's yours to customize freely.

## My Identity

<!-- Replace with your actual identity -->
name: "Your Name / Team Name"
contact:
  email: "you@example.com"
  twitter: "@yourhandle"
  telegram: "@yourhandle"
  ens: "yourname.eth"

## My Services

<!-- List your actual services with a one-line pitch for each -->

### Primary Lead Hook (highest close rate)
service: "Smart Contract Security Audit"
hook: "With your treasury and TVL on the line, you can't ship V2 without a safety check."
turnaround: "5–10 business days for contracts up to 1200 LOC"
price_range: "$3,000 – $15,000 depending on scope"

### Secondary Services
- "UI/UX Overhaul — redesign and rebuild the dApp frontend for conversion and trust"
- "Smart Contract Porting — migrate contracts to new chain with security-first approach"
- "Frontend Chain Integration — wallet, RPC, and contract integration for new chain deployment"
- "Architecture Advisory — protocol design, upgradeability, and scaling review"

## My Pitch Narrative

<!-- Your personal opening line. Keep it to 2–3 sentences max. -->
headline: |
  "I audit smart contracts and rebuild the UX for Web3 protocols that have outgrown their MVP 
   but aren't ready to hire a full team. I've found [X] critical vulnerabilities and helped 
   [N] protocols improve their conversion within 30 days."

## Proof of Work

<!-- Your best case studies — the ones you lead with in every conversation -->

### Top Case Study
protocol: "Protocol Name"
result: "Found a reentrancy vulnerability that would have drained $120k. Patched before launch."
link: "https://your-audit-link-or-github"

### Other Proof Points
- "Ported [Protocol] from Ethereum to Base — 0 incidents, on-time delivery"
- "Rebuilt [Protocol] UX — active wallets up 40% in 30 days post-launch"

## My Pitch Rules

### Non-Negotiables (Deal-Breakers)
- No anonymous teams with no verifiable history
- No meme coins or pure speculative tokens with no utility
- Minimum treasury: $100,000 (they need to be able to pay)
- No engagements below $3,000

### Pricing Strategy
- Entry point: free logic-sanity check for Security Risk leads (converts to paid audit)
- Standard engagement: $3k–$15k depending on scope and chain complexity
- Preferred: fixed scope + fixed price (not hourly — protects both sides)
- Payment: 50% upfront, 50% on delivery — in USDC or equivalent stablecoin

## My Objection Responses

### "We don't have the budget right now"
response: |
  "Understood — what does your treasury look like in 60 days? 
   I can reserve a slot now and start then. A lot of teams wait until after V2 ships, 
   but that's exactly when the vulnerability window is widest."

### "We already had an audit"
response: |
  "Great — who did it, and was it on the current deployed version or a prior commit? 
   Most audits don't cover the upgrade or the frontend integration, which is where 
   most real-world exploits enter. I can do a targeted gap check in 2 days."

### "We can handle it internally"
response: |
  "I believe you — but fresh eyes catch things that familiarity hides. 
   I'm not replacing your team. I'm the second set of eyes before you go live with real money."

## My Target Chains

<!-- Chains I actively target for leads -->
primary_chains:
  - Base
  - Arbitrum
  - Ethereum
secondary_chains:
  - Berachain
  - Mantle
  - Hyperliquid
  - Monad

## Lead Prioritization Rules

<!-- These override the default scoring when evaluating leads -->
- Boost score by +0.5 if: protocol is on my primary_chains list
- Boost score by +0.5 if: TVL is declining (Leaky Bucket — higher urgency = higher close rate)
- Boost score by +0.3 if: protocol recently announced V2 or migration (Security Risk timing)
- Reduce score by -0.5 if: treasury < $150k (just above deal-breaker — flag as Watch)
- Flag as Watch instead of Skip: if treasury is $75k–$100k and team is responsive (may close in 60 days)

## Discovery Call Prep Template

When prepping for a call with a protocol team, structure research around:
1. What specific pain point are they most aware of? (not what I think — what THEY're saying publicly)
2. Who am I talking to — founder, lead dev, community manager?
3. What's their biggest upcoming milestone (V2, new chain, governance launch)?
4. What proof point from my service-profile.md is most relevant to their moment?
5. What's the one thing I would show them in the first 5 minutes to create "aha" moment?
