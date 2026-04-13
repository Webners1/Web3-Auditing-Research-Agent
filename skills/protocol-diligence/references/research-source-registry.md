# Web3 Research Source Registry

This agent does **comprehensive, broad research** — not surface-level comparisons against a fixed set of blue-chip protocols.

When producing the Industry Gap Analysis, Feature Opportunities, and Business Observations sections, the agent must research across the full Web3 landscape: established protocols, emerging categories, new ERC/EIP standards, exploit post-mortems, security research, academic work, and live market data. The goal is to find the **best standard that exists anywhere**, not just what Aave and Uniswap happen to do.

---

## Research Order

Start narrow and widen only when needed:

```
1. Official project surface          → what this protocol says it is
2. On-chain data and explorers       → what the protocol actually does
3. Live DeFi market data             → how it compares to the category
4. Security and exploit databases    → known vulnerabilities in this pattern
5. Standards and EIPs                → what the specification landscape says
6. Broad protocol benchmarking       → who does this pattern best, anywhere
7. Academic and research layer       → what serious researchers say about this
8. General search fallback           → only after exhausting the above
```

---

## 1. Official Project Surface

Always start here:

- Protocol website, docs, litepaper, whitepaper
- GitHub org and all repositories
- Governance forum (Snapshot, Tally, Commonwealth, on-chain)
- Official audit page and all published audit PDFs
- Bug bounty page (Immunefi, HackerOne, Code4rena scope)
- Deployment / addresses page
- Official blog and announcement channels

---

## 2. On-Chain Data and Explorers

| Source | URL | Use For |
|--------|-----|---------|
| Etherscan | `https://etherscan.io` | Contract source, proxy/impl, events, tx history |
| Blockscout | `https://blockscout.com` | Alternative explorer, multi-chain |
| Arbiscan | `https://arbiscan.io` | Arbitrum contracts |
| Basescan | `https://basescan.org` | Base contracts |
| Polygonscan | `https://polygonscan.com` | Polygon contracts |
| Tenderly | `https://tenderly.co` | Transaction simulation and trace analysis |

---

## 3. Live DeFi Market Data

| Source | URL | Use For |
|--------|-----|---------|
| DefiLlama | `https://defillama.com` | TVL, fees, revenue, yields, protocol comparisons |
| DefiLlama MCP | `https://defillama.com/mcp` | Structured metrics if MCP is configured |
| L2BEAT | `https://l2beat.com` | Rollup stages, TVS, risk summaries, bridge risk |
| Token Terminal | `https://tokenterminal.com` | Revenue, P/F ratios, user metrics |
| Dune Analytics | `https://dune.com` | On-chain query dashboards for protocol-specific data |
| The Block | `https://theblock.co` | Market intelligence and category research |
| Messari | `https://messari.io` | Protocol profiles, market context, sector reports |

---

## 4. Security and Exploit Databases

Use these to ground security recommendations in real incidents — not hypotheticals:

| Source | URL | Use For |
|--------|-----|---------|
| Solodit | `https://solodit.xyz` | Aggregated findings from all major audit firms and contests |
| Rekt News | `https://rekt.news` | Exploit post-mortems, attack narratives |
| DeFiHack Database | `https://github.com/SunWeb3Sec/DeFiHacks` | Indexed list of real DeFi exploits with PoC |
| Immunefi Disclosed | `https://immunefi.com/explore` | Disclosed vulnerability reports from live programs |
| Code4rena | `https://code4rena.com` | Public contest findings — all severities |
| Sherlock | `https://app.sherlock.xyz` | Protocol audit contest reports |
| SWC Registry | `https://swcregistry.io` | Canonical smart contract weakness classification |
| Trail of Bits Blog | `https://blog.trailofbits.com` | Deep technical security research |
| Spearbit Blog | `https://spearbit.com/blog` | Security research and pattern analysis |
| Pashov Blog | `https://pashov.net` | Solidity auditing methodology and findings |
| Halborn Blog | `https://halborn.com/blog` | Security research across chains |
| OtterSec Blog | `https://osec.io/blog` | Multi-chain security research |
| BlockSec Blog | `https://blocksec.com/blog` | Exploit analysis and incident response |

---

## 5. Standards, EIPs, and ERCs

Always check whether a standard already exists before recommending a custom solution:

| Source | URL | Use For |
|--------|-----|---------|
| EIPs | `https://eips.ethereum.org` | All Ethereum Improvement Proposals |
| ERCs | `https://eips.ethereum.org/erc` | Token and application standards |
| Ethereum Magicians | `https://ethereum-magicians.org` | Standards under active discussion |
| Ethereum Roadmap | `https://ethereum.org/en/roadmap` | Protocol direction, upcoming upgrades |
| OpenZeppelin Contracts | `https://docs.openzeppelin.com/contracts/5.x` | Reference implementations |
| ERC-4626 | `https://eips.ethereum.org/EIPS/eip-4626` | Tokenized vault standard |
| ERC-7540 | `https://eips.ethereum.org/EIPS/eip-7540` | Async deposit/redeem vaults |
| ERC-7683 | `https://eips.ethereum.org/EIPS/eip-7683` | Cross-chain intents |
| ERC-7702 | `https://eips.ethereum.org/EIPS/eip-7702` | Account abstraction (EOA code injection) |
| ERC-4337 | `https://eips.ethereum.org/EIPS/eip-4337` | Account abstraction standard |
| EIP-1967 | `https://eips.ethereum.org/EIPS/eip-1967` | Proxy storage slots standard |
| EIP-2535 | `https://eips.ethereum.org/EIPS/eip-2535` | Diamond multi-facet proxy |

---

## 6. Protocol Benchmarking by Category

When benchmarking, find the **best protocol for the specific pattern** — not just the biggest protocol overall. The best oracle design may come from a mid-size protocol that solved it better than Aave. The best veToken model may come from a protocol newer than Curve.

Use category-appropriate benchmarks:

| Category | Who to research |
|----------|----------------|
| **Lending / Credit** | Aave, Morpho Blue, Euler v2, Spark, Compound v3, Silo Finance, Fraxlend |
| **DEX / AMM** | Uniswap v3/v4, Curve, Balancer v3, Trader Joe v2, Maverick, Ambient |
| **Yield / Vaults** | Yearn v3, Pendle, ERC-4626 adopters, Beefy, Convex, Sommelier |
| **Liquid Staking** | Lido, Rocket Pool, EtherFi, StakeWise v3, Renzo, Kelp DAO |
| **Restaking** | EigenLayer, Symbiotic, Karak, Babylon Protocol |
| **Stablecoins** | MakerDAO/Sky, Ethena, Frax, crvUSD, GHO, USDS |
| **Bridges / Cross-chain** | Stargate, Across, Hop, Connext, LayerZero, Chainlink CCIP |
| **Oracle** | Chainlink, Pyth, Chronicle, RedStone, Tellor, API3 |
| **Governance** | Compound Governor Bravo, Tally, Snapshot, Aragon, OpenZeppelin Governor |
| **Derivatives / Perps** | GMX v2, dYdX v4, Synthetix v3, Kwenta, Drift |
| **RWA / Tokenization** | Ondo Finance, Maple Finance, Centrifuge, Goldfinch, TrueFi |
| **Intent / Order Flow** | CoW Protocol, UniswapX, 1inch Fusion, Anoma |
| **Account Abstraction** | Safe, Biconomy, ZeroDev, Alchemy Account Kit |
| **NFT / Gaming** | OpenSea, Blur, Seaport, Piranesi, Treasure DAO |
| **Privacy** | Tornado Cash, Aztec, Railgun, Penumbra |
| **Hashrate / Mining** | Mars Poolin, Stratum V2, Ocean Protocol mining layer |

Research **both the established leaders and the protocols that solved specific sub-problems best**. A newer protocol may have a better solution for one specific component.

---

## 7. Academic and Technical Research

| Source | URL | Use For |
|--------|-----|---------|
| Ethereum Research | `https://ethresear.ch` | Core Ethereum protocol research |
| a16z Crypto Research | `https://a16zcrypto.com/research` | Applied crypto research, formal analysis |
| Paradigm Research | `https://www.paradigm.xyz/writing` | Deep protocol and mechanism design |
| Flashbots Research | `https://writings.flashbots.net` | MEV, PBS, block building research |
| Chainalysis Reports | `https://chainalysis.com/blog` | On-chain analytics and market intelligence |
| Ethereum Foundation Blog | `https://blog.ethereum.org` | Core protocol updates and roadmap context |

---

## 8. General Search Fallback

Only after exhausting the above. Use targeted queries — never start with a broad search.

Preferred query patterns:
- `site:github.com [protocol] [vulnerability type]`
- `[EIP number] site:ethereum-magicians.org`
- `[pattern] audit finding site:solodit.xyz`
- `[protocol category] best practices 2024 OR 2025`

---

## Research Discipline Rules

1. **Find the best example, not the most famous example.** Aave, Compound, and Uniswap are mentioned often because they are large — not always because they did something best. Always ask: is there a protocol that solved this more elegantly?

2. **Ground recommendations in live data.** TVL claims, adoption numbers, and trend claims must come from DefiLlama, L2BEAT, or Token Terminal — not from memory.

3. **Ground security comparisons in real incidents.** When calling out a vulnerability pattern, find the real exploit (Solodit, Rekt.news, DeFiHacks) or the real audit finding (Code4rena, Sherlock, Immunefi). Hypothetical comparisons are weaker than real ones.

4. **Check if a standard already exists.** Before recommending a custom solution, check EIPs and ERCs. If ERC-4626 solves the vault problem, recommend ERC-4626 — don't recommend building a custom vault interface.

5. **Emerging protocols count.** A 6-month-old protocol that solved oracle manipulation in a genuinely novel way is a valid benchmark. Recency is not a disqualifier.

6. **Industry gaps must be specific.** "Other protocols use better oracles" is not a gap. "Morpho Blue uses a fully on-chain oracle with a 30-minute TWAP minimum and a Chainlink fallback with a staleness check — this protocol uses a paramSetter-controlled AMM spot price with no minimum window" is a gap.
