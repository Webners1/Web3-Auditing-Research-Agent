# DeFi Integration Playbook

Use this file when recommending external protocols, liquidity venues, oracle stacks, or yield layers.

---

## 1. Integration Categories

| Category | Typical options | Main question |
|----------|-----------------|---------------|
| Price data | Chainlink, Pyth, RedStone | Is the price source robust enough for your exposure? |
| Spot / routing | Uniswap, Curve, CowSwap, aggregators | Do you need deep liquidity, best execution, or deterministic routing? |
| Lending / idle capital | Aave, Morpho, Spark | Should idle assets earn yield or remain liquid and simple? |
| Yield / fixed income | Pendle and related systems | Does the added complexity justify the product advantage? |
| Messaging / bridging | CCIP, LayerZero, Hyperlane, canonical bridges | Do you truly need cross-chain messaging now? |

---

## 2. Recommendation Rules

- Recommend integrations that compress time-to-market or reduce risk, not integrations that only sound sophisticated.
- Every integration recommendation must include a threat model update.
- Prefer the simplest dependency that solves the product need.
- If an integration creates a new trust assumption, say it plainly.

---

## 3. Required Analysis For Each Integration

For each suggested integration, document:
- Product reason
- Technical fit
- Security implications
- Operational dependencies
- Exit path if the integration fails or is removed

---

## 4. Common Good Patterns

- Use battle-tested oracle providers instead of AMM spot price for solvency-critical logic.
- Use adapter contracts around external dependencies so you can swap providers later.
- Use explicit caps, allowlists, and kill-switches for integrations with meaningful economic exposure.
