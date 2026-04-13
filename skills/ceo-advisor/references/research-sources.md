# Market Research Sources — CEO Advisor

Always load `../../protocol-diligence/references/research-source-registry.md` first.
That file defines the full research landscape. This file adds strategy-specific guidance on top.

---

## Market Research Priority

Before giving any trend, positioning, or competitive advice, verify current state from live sources.
Do not rely on training data for:
- TVL and category rankings
- Chain activity and fee trends
- Protocol-level revenue and user metrics
- Narrative cycles (what is hot, what has cooled)
- Ecosystem incentive programs

---

## Primary Strategy Data Sources

| Source | Use For |
|--------|---------|
| DefiLlama — Categories | Category TVL, growth rates, protocol ranking within category |
| DefiLlama — Fees | Who is actually generating revenue vs who is subsidizing growth |
| DefiLlama — Yields | Where capital is being deployed, yield compression signals |
| L2BEAT | Which rollups are growing, which are declining, sequencer and bridge risk |
| Token Terminal | P/F ratios, protocol revenue, active user trends |
| Dune Analytics | Find dashboards for the specific protocol or category being analyzed |
| Messari | Sector reports, protocol profiles, market structure context |

## Narrative and Sentiment Inputs

Use these as supporting signals, not standalone truth:
- Messari sector notes and protocol profiles
- Ecosystem research posts from major chains and wallets
- Category-specific dashboards or commentary tied to on-chain metrics

Always pair narrative claims with at least one hard metric source (DefiLlama, Token Terminal, Dune, or L2BEAT).

---

## Competitive Benchmarking Rules

Find the **best peer for each specific capability**, not the most well-known protocol overall:

- The best tokenomics design may be from a protocol that launched 6 months ago
- The best oracle architecture may be from a mid-size lending market, not Aave
- The best governance structure may be from a newer DAO that learned from Compound's failures
- The best composability pattern may be from a vault protocol nobody has heard of yet

**Always ask:** who solved this problem best — regardless of TVL or age?

### Function-matched comparable protocol set

For each strategy memo, build a comparable set with explicit roles:
- 1-2 direct functional peers (same user job-to-be-done)
- 1 adjacent alternative (different mechanism, same user outcome)
- 1 one-curve-ahead benchmark (where the category appears to be moving)

Document why each comparable is included and what decision it informs.

Do not reuse the same comparable basket across every protocol. Build a fresh set each time based on function, user profile, and architecture context.

### Benchmark by specific question, not by protocol name

| Question | Who to research |
|----------|----------------|
| Best sustainable incentive model | Curve veCRV, Velodrome/Aerodrome, Balancer veBAL, Radiant Capital |
| Best oracle design | Morpho Blue (fully on-chain), Chronicle (Ethereum-native), Pyth (pull), RedStone (modular) |
| Best governance with low voter apathy | Optimism Citizens House, Nouns DAO, Tally deployments |
| Best fee capture → token value | GMX fee distribution, dYdX tokenomics, Pendle yield splitting |
| Best composability unlock | ERC-4626 adopters, Pendle PT/YT splitting, Morpho MetaMorpho |
| Best cross-chain strategy | Stargate (omnichain liquidity), Across (intents-based), Chainlink CCIP |
| Best RWA integration | Ondo Finance, Maple Finance, MakerDAO RWA vaults |
| Best restaking yield | EigenLayer AVS landscape, Symbiotic vaults, Karak network |

---

## Trend Verification Checklist

Before naming a trend as active, verify at least two of:

1. TVL growth in the category on DefiLlama in the last 90 days
2. Recent protocol launches or major upgrades in the category
3. Ecosystem incentive programs targeting the category
4. Ethereum Foundation or major L2 roadmap alignment
5. Major protocol (Aave, Uniswap, Coinbase, Binance) moving into the space

If a trend cannot be verified by at least two sources, call it a hypothesis, not a fact.

When citing sentiment or narrative momentum, include:
- What changed
- Over what time window
- Which metric confirms or contradicts the narrative

---

## Strategy Lenses (apply to every recommendation)

| Lens | Key question |
|------|-------------|
| Product | Does this matter to actual users right now, or only theoretically? |
| Distribution | How does the protocol reach users — and does this move help that? |
| Economics | Does this improve revenue, retention, or liquidity quality? |
| Security | Does this change the threat model — and is the team ready for that? |
| Timing | Is the market ready for this, or is it 12 months early? |

Downgrade any recommendation that fails two or more lenses.

---

## What NOT to say

- "The industry uses X" — too vague. Name the protocol and explain what they built.
- "You should go multichain" — too generic. Specify which chain, why, and what the user acquisition thesis is.
- "Launch a token" — only recommend this with a specific utility mechanism and distribution plan.
- "Consider improving your tokenomics" — specify what is broken and what the fix looks like with a named example.
- Any trend claim from memory alone without live data verification.
- "Aave/Uniswap/Curve always define best practice" — sometimes true, often incomplete. Verify by capability and timeframe.
