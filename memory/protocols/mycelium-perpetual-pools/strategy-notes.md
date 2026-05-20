# Mycelium Perpetual Pools — Strategy Notes
Date: 2026-05-20

## Market Position

**Comparable protocols (derivatives/leverage pools on Arbitrum):**
- GMX V2: $800M+ TVL — dominant Arbitrum derivatives protocol
- Hyperliquid: $3B+ TVL — now the benchmark for on-chain perps UX
- Synthetix Perps V3: Migrated to Optimism/Base
- dYdX V4: Migrated to its own chain

**Mycelium's position:** The tokenized leveraged pool model (like Tracer/Mycelium Pools) was innovative in 2021 but has been superseded by GMX-style liquidity pools and the Hyperliquid model. The fundamental UX of "wait for keeper to rebalance" doesn't compete with sub-second execution that traders now expect.

## Pitch Strategy Assessment

**Standard pitch (new audit contract): NOT recommended**
- Protocol is winding down — no active development, no new features
- Team will not commission a full audit for a deprecated product
- Response probability: <10%

**Targeted remediation pitch: POSSIBLE but limited**
- $183k of user funds remain exposed to HIGH finding (L2 sequencer)
- Outreach angle: "responsible disclosure + offer to remediate OracleWrapper for residual users"
- Team may appreciate the heads-up but won't pay for it
- Response probability: ~20%, conversion to paid work: <5%

**Mycelium as company (not just Pools): UNKNOWN**
- The company (mycelium.xyz / mycelium-ethereum) may have pivoted to something new
- Worth checking if they have a new product or ongoing development
- If they have an active new protocol, the security findings + credibility from Pools analysis could open a door

## Recommendation

This lead should be marked **Evaluated — Low Fit**. Not worth a full pitch effort. Options:
1. Send a brief responsible disclosure email about FINDING-001 (good karma, may build relationship)
2. Skip and move to next lead
3. Research mycelium-ethereum GitHub for any new product in development — if active, repitch on that

## Phase Handoff
- Protocol: Mycelium Perpetual Pools
- Chain: Arbitrum One
- Key finding from this phase: Protocol is in wind-down. Not a strong paid-work target. Responsible disclosure of HIGH finding may be more appropriate than a sales pitch.
- Open question for next phase: Does Mycelium have an active new product worth pitching to?
- Skip Report phase: No — write the report for completeness, but mark pitch as low priority.
