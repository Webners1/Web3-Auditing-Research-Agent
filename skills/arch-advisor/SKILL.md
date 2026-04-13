# Web3 Architecture Advisor and Product Strategist

Analyzes smart contract architecture and delivers concrete upgrade recommendations. Goes beyond vulnerability findings to answer: how should this protocol be structured, what should it integrate, and how should it scale? Benchmarks against how Aave, Uniswap, Compound, and Morpho solved the same design problems.

**Trigger phrases:** `advise architecture`, `make it upgradeable`, `how should I upgrade`, `scale this protocol`, `integrate [protocol name]`, `what L2 should I deploy on`, `architecture review`, `product roadmap`, `what should I build next`, `suggest improvements`, `make it cross-chain`, `what protocol should I use for [use case]`, `architecture advisory`

---

## Execution Pipeline

### Phase 0 - Source Routing

Load `../protocol-diligence/references/research-source-registry.md` first.

If live chain or ecosystem data is needed to support a recommendation:
1. Official project docs and deployment addresses
2. L2BEAT for chain and rollup data
3. DefiLlama for TVL, ecosystem, and integration fit
4. OpenZeppelin, Aave, Uniswap docs for implementation benchmarking

Do not use generic search to make architecture recommendations. Ground every recommendation in the source registry.

### Phase 1 - Architecture Snapshot (run concurrently)

**1a. Map contract graph**
```bash
find . -name "*.sol" -not -path "*/node_modules/*" -not -path "*/lib/*" -not -path "*/test*" | sort
grep -rn "^contract \|^abstract contract \|^interface \|^library " --include="*.sol" .
grep -rn "^import " --include="*.sol" . | head -50
```

**1b. Detect upgradeability**
```bash
grep -rn "delegatecall\|upgradeable\|UUPSUpgradeable\|TransparentUpgradeableProxy\|Diamond\|BeaconProxy\|Initializable\|_disableInitializers" --include="*.sol" .
```

**1c. Detect DeFi integrations**
```bash
grep -rn "IUniswap\|ICurve\|IAave\|ICompound\|IMorpho\|IChainlink\|IPyth\|ILido\|IEigenLayer\|IPendle\|IWETH" --include="*.sol" .
```

**1d. Detect cross-chain patterns**
```bash
grep -rn "LayerZero\|Wormhole\|CCIP\|Axelar\|Hyperlane\|bridge\|lzReceive\|IMessagePassingInterface" --include="*.sol" .
```

**1e. Detect access control maturity**
```bash
grep -rn "Ownable2Step\|AccessControl\|TimelockController\|Pausable\|guardian\|multisig\|Safe" --include="*.sol" .
```

**1f. Check test coverage signal**
```bash
forge coverage 2>/dev/null | tail -10 || echo "FORGE_NOT_AVAILABLE"
```

### Phase 2 - Gap Analysis

Load these reference files based on what was detected:

| Condition | Load |
|-----------|------|
| No proxy pattern detected | `references/upgrade-patterns.md` |
| Single-chain only | `references/l2-ecosystem.md` |
| Missing DeFi integrations | `references/defi-integrations.md` |
| Always | `references/security-architecture.md` |

Apply the Architecture Gap Checklist:

| Category | Check | Flag If |
|----------|-------|---------|
| Upgradeability | Proxy pattern in place? | No proxy on a production or maturing protocol |
| Upgradeability | `__gap` in all upgradeable base contracts? | Missing gap in any upgradeable base |
| Access Control | `Ownable2Step` or `AccessControl`? | Single-step ownership transfer |
| Access Control | Timelock on admin functions? | Protocol-critical params changeable instantly |
| Emergency Controls | Pause mechanism present? | No way to halt on exploit |
| Emergency Controls | Guardian role distinct from owner? | Same key can both upgrade and pause |
| Oracle | Chainlink or equivalent for price-critical logic? | Spot price from AMM reserves |
| Oracle | Staleness and sanity checks present? | No `updatedAt` validation |
| DeFi | Idle capital earning yield? | Held assets generating nothing |
| DeFi | Protocol fee capture? | No path to sustainable funding |
| Cross-Chain | L2 deployment considered? | Mainnet-only with fee-sensitive users |
| Cross-Chain | Canonical bridge pattern? | Custom bridge with no exit path |
| Composability | Clean standard interfaces exposed? | Hard to integrate with |
| Size | Contract under 24KB limit? | Over limit or near limit without Diamond |

For each gap, assign: **URGENT** (security risk) / **HIGH** (significant capability gap) / **MEDIUM** (optimization) / **LOW** (polish).

### Phase 3 - Recommendation Generation

For each identified gap, produce:

```
### [PRIORITY] — [Category]: [Gap Title]

**Current state:** [what the protocol does now]
**Industry standard:** [how top protocols handle this, with a named example]
**Recommendation:** [specific action]
**Implementation steps:**
1. [step]
2. [step]
**Trade-offs:**
- Gains: [what the protocol gets]
- Costs: [complexity, gas, operational burden added]
**Estimated effort:** [HOTFIX / SHORT SPRINT / MULTI-SPRINT]
```

Always include an industry comparison. Vague architecture advice is not useful. A recommendation without a named protocol example or a concrete implementation path should not appear in this report.

### Phase 4 - Roadmap Output

Write the report using `references/report-format.md`:

```
audit-output/[project-name]-arch-[YYYYMMDD].md
```

Then hand off to `skills/client-reporting/SKILL.md` if the user wants an HTML or PDF deliverable.

---

## Architecture Advisor Rules

- Benchmark every recommendation against a named protocol that solved the same problem
- State both gains and costs for every upgrade recommendation
- Do not recommend multichain without explaining how liquidity, governance, and monitoring stay coherent
- Do not recommend integrations only because they sound sophisticated
- Every integration recommendation must include a threat model note
- Tie complexity to the product stage: recommend what the team can actually build and maintain
- If the safest recommendation is fewer dependencies or no upgrade, say so
- If the user asks about a specific integration or chain, verify current live data from the source registry before advising
