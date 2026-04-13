Load `skills/protocol-memory/SKILL.md`.
Load `skills/protocol-diligence/references/research-source-registry.md`.

This is the primary command for researching an EXTERNAL protocol — one you do not own but want to audit, analyze, or pitch improvements to. It runs discovery, security analysis, architecture review, and opportunity mapping in a single flow.

**Argument:** $ARGUMENTS — a URL, protocol name, or either followed by a focus keyword.

Example inputs:
- `https://fuji.finance/`
- `https://mars.poolin.fi/`
- `Uniswap v4`
- `https://app.aave.com/ bugs`
- `Morpho Blue improvements`
- `https://compound.finance/ both`

---

## Step 1 — Resolve Input to Protocol Identity

**If $ARGUMENTS is a URL (starts with `http`):**
1. Extract the domain — e.g., `mars.poolin.fi` → slug `mars-poolin`, `fuji.finance` → slug `fuji-finance`
2. Fetch the URL: `WebFetch(url, "Extract: protocol name, what it does, GitHub links, docs links, contract addresses, token names, chain")`
3. If the page is JS-rendered and returns no content, fall back to web search: `"[domain] protocol DeFi smart contract GitHub"`
4. Derive the protocol name and continue

**If $ARGUMENTS is a name:** use directly. Normalize to slug.

Check `memory/protocols/[slug]/` for any prior context. Load it if it exists. Create it if not.

---

## Step 2 — External Discovery

Use the source registry research order. For this protocol, find:

1. **Official sources**
   - Protocol website and docs
   - GitHub org and main repository
   - Deployment / addresses page
   - Prior public audits (search docs site + GitHub)
   - Bug bounty page
   - Wallet UX / smart-wallet claims and any account-abstraction disclosures

2. **On-chain footprint**
   - Verify deployed contract addresses
   - Check proxy / implementation via Etherscan or Blockscout
   - Note chains deployed on

3. **Market context** (from DefiLlama, L2BEAT)
   - TVL and category
   - Chain breakdown
   - Direct competitors

Record all source URLs. Every claim in the output must trace back to a source.

---

## Step 3 — Contract Acquisition

**Priority order — try each until source code is obtained:**

1. **GitHub clone (best):** if a repo URL was found:
```bash
git clone [repo-url] /tmp/[slug]-contracts 2>&1 | tail -5
find /tmp/[slug]-contracts -name "*.sol" -not -path "*/node_modules/*" -not -path "*/lib/*" -not -path "*/test*" | sort
```

2. **Etherscan source API:** for each contract address found:
```
WebFetch: https://api.etherscan.io/api?module=contract&action=getsourcecode&address=[ADDRESS]&apikey=YourApiKeyToken
```
Parse the `SourceCode` and `ContractName` fields from the JSON response.

3. **Etherscan UI fallback:**
```
WebFetch: https://etherscan.io/address/[ADDRESS]#code
```
Extract visible source code from the `#code` tab.

4. **Blockscout fallback** (for L2 chains — Arbitrum, Optimism, Base):
```
WebFetch: https://[chain].blockscout.com/address/[ADDRESS]/contracts
```

**Note if the site was JS-rendered and returned no content:**
Fall back immediately to web search: `"[domain] protocol GitHub smart contract"` — do not halt on a blank page fetch.

---

## Step 4 — Route by Focus

**Always first** → Run `skills/product-assessor/SKILL.md` to map trust boundaries and product risk.
Include:
- one primary workflow pass
- one failure-path workflow pass
- smart-wallet/account-abstraction readiness checks when claimed

**Focus: `bugs` or `both`** → Run `skills/web3-audit/SKILL.md` on the discovered contracts.
The audit must use proof discipline. Do not flag speculative issues.

**Focus: `improvements` or `both`** → Run `skills/arch-advisor/SKILL.md` on the discovered architecture.
Benchmark against the source registry. Identify upgrade paths, integration gaps, scaling limitations.

**Always** → Run `skills/ceo-advisor/SKILL.md` to identify:
- What market opportunities exist for this protocol category right now
- What the protocol is not doing that competitors or complementary protocols are
- What a well-positioned team would build next

---

## Step 5 — Save and Output

Update `memory/protocols/[slug]/`:
- `profile.md` — what the protocol is, its footprint, key contracts
- `findings.md` — security findings and leads
- `working-memory.md` — architecture gaps and improvement opportunities
- `next-actions.md` — recommended engagement next steps

Write outputs to `audit-output/`:
- `[slug]-product-[YYYYMMDD].md` from product assessor
- `[slug]-audit-[YYYYMMDD].md` if bugs were analyzed
- `[slug]-arch-[YYYYMMDD].md` if architecture was reviewed
- `[slug]-strategy-[YYYYMMDD].md` if market strategy was analyzed

Print a summary:
- Protocol overview (2 sentences)
- Top 3 security findings or leads
- Top 3 architecture improvement opportunities
- Top 2 strategic recommendations
- Suggested next command

---

## Usage Examples

```
/research https://fuji.finance/
/research https://mars.poolin.fi/
/research https://app.aave.com/ bugs
/research https://compound.finance/ both
/research Uniswap v4
/research Morpho Blue improvements
/research EigenLayer both
```
