# L2 and Chain Deployment Decision Guide

Use this file to structure chain and cross-chain recommendations. Validate live metrics before making a final recommendation.

---

## 1. Decision Criteria

Score each candidate chain on:

| Criterion | What to ask |
|-----------|-------------|
| User fit | Where are the target users already transacting? |
| Liquidity adjacency | Which chain already has the assets and protocols you need? |
| Cost and latency | Are fees and finality acceptable for the product's main action? |
| Ethereum alignment | How strong is the settlement and security model? |
| Tooling and infra | Are wallets, indexers, oracle providers, and RPC options mature enough? |
| Bridge safety | Is there a credible canonical path for asset movement? |
| Ecosystem support | Are there grants, BD help, or distribution advantages? |

---

## 2. Deployment Heuristics

- Stay on Ethereum mainnet when the product depends on maximum trust, deepest liquidity, or institutional credibility.
- Favor L2s when the main user action is fee-sensitive, frequent, or consumer-facing.
- Favor a single initial chain over premature multichain expansion unless distribution or liquidity clearly requires otherwise.
- Prefer battle-tested bridges and messaging layers over custom bridge logic.

---

## 3. Cross-Chain Rules

- Canonical bridge first, generalized messaging second, custom bridge last.
- Treat sequencer downtime, message delay, replay risk, and out-of-order delivery as first-class design constraints.
- Never recommend multichain without answering how liquidity, governance, and monitoring stay coherent.

---

## 4. Recommendation Format

For each chain recommendation, always include:
- Why this chain fits the product now
- What the team gains
- What new operational or trust risks appear
- What integrations become easier
- What future chains should wait until later
