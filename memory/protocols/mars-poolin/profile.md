# Mars Poolin (MARS Project)

- Slug: mars-poolin
- Category: Hashrate Tokenization / PoW-DeFi Bridge
- Stage: Live → Declining (MARS emission ended Dec 2024)
- Chains: Ethereum Mainnet
- Website: https://mars.poolin.fi/
- GitHub: https://github.com/MarsFi/POWToken
- Framework: Truffle (Solidity ^0.5.17)
- Audit status: NONE submitted on Etherscan

## Core Contracts

| Contract | Address | Notes |
|----------|---------|-------|
| pBTC35A Token (Proxy) | `0xA8b12Cc90AbF65191532a12bb5394A714A46d358` | ZeppelinOS TransparentProxy |
| pBTC35A Implementation | `0xDDF23427abe061cd10408661bd3a7d051efe7fed` | ERC-20 + mint/burn |
| MARS Governance Token | `0x66C0DDEd8433c9EA86C8cf91237B14e10b4d70B7` | Direct impl, Comp-style voting |
| LP Pair (pBTC35A/USDT) | `0x5b1e45ca08fa4d65aa7fdcf9e116990fb7fce73b` | Uniswap V2 |
| TokenDistribute | (in repo) | Whitelist-gated mint via exchange |
| Staking | (in repo) | Stake pBTC35A → wBTC + MARS |
| LpStaking | (in repo) | Stake LP → wBTC + MARS |
| BTCParamV2 | (in repo) | BTC price oracle, difficulty params |

## What It Does

- pBTC35A = tokenized 1 TH/s Bitcoin hashrate backed by physical ASIC miners in Poolin custody
- Users stake pBTC35A or pBTC35A/USDT LP → earn wBTC (mining yield) + MARS (governance rewards)
- MARS token: 2.1B total, linearly released Jan 2021 – Dec 2024 (emission NOW COMPLETE)
- wBTC rewards sourced from actual BTC mined by underlying hardware after 2.5% fee + electricity

## Trusted Actors

- Owner (deployer): `0x65785917bc751f6506bd4818527b1909d0b1e57a` — single EOA
- paramSetter: controls BTC price oracle, difficulty, exchange rates
- No multisig, no timelock detected
