Load `skills/arch-advisor/SKILL.md`.

Analyzes the current protocol architecture and delivers a concrete upgrade roadmap. Covers: proxy patterns, DeFi integrations, L2 deployment strategy, cross-chain architecture, access control maturity, and composability. Benchmarks against Aave, Uniswap, Compound, and Morpho.

**Argument:** $ARGUMENTS (optional — protocol name or focus area)

Focus area examples: `upgradeability`, `L2`, `integrations`, `cross-chain`, `oracle`, `full`

---

## What Runs

1. Snapshots the current architecture (contracts, proxy pattern, integrations, access controls)
2. Runs the gap analysis checklist
3. Loads relevant reference files (upgrade-patterns, l2-ecosystem, defi-integrations, security-architecture)
4. Produces prioritized recommendations (URGENT / HIGH / MEDIUM / LOW)
5. Writes a technical roadmap with phased implementation plan
6. Writes report to `audit-output/[project]-arch-[YYYYMMDD].md`

---

## After Architecture Review

- For market and product strategy: `/strategy`
- For a client-ready PDF: `/report architecture`

---

## Usage Examples

```
/arch
/arch Uniswap v4
/arch upgradeability
/arch L2
/arch full
```
