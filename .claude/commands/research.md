Load `skills/protocol-memory/SKILL.md`.
Load `skills/protocol-diligence/references/research-source-registry.md`.

Research an external protocol — runs discovery, security analysis, architecture review, and opportunity mapping.

**Argument:** $ARGUMENTS — a URL, protocol name, or either followed by a focus keyword (`bugs` / `improvements` / `both`).

---

## Step 1 — Resolve Protocol Identity

**If URL:** fetch it → extract protocol name, GitHub, docs, contract addresses, chain. If JS-rendered with no content, fall back to web search: `"[domain] protocol DeFi smart contract GitHub"`. Derive slug from domain (e.g. `mars.poolin.fi` → `mars-poolin`).

**If name:** use directly, normalize to slug.

Check `memory/protocols/[slug]/` for prior context. Load it if it exists; create it if not.

---

## Step 2 — External Discovery

Find:
1. **Official sources** — website, docs, GitHub org, deployment/addresses page, prior public audits, bug bounty page, smart-wallet/AA claims
2. **On-chain footprint** — verify deployed contracts, proxy/implementation via Etherscan or Blockscout, chains deployed on
3. **Market context** — TVL and category from DefiLlama; chain breakdown; direct competitors

Record all source URLs. Every claim must trace back to a source.

---

## Step 3 — Contract Acquisition

Try each in order until source code is obtained:

1. **GitHub clone:** `git clone [repo-url] /tmp/[slug]-contracts` → enumerate `.sol` files
2. **Etherscan API:** `https://api.etherscan.io/api?module=contract&action=getsourcecode&address=[ADDRESS]`
3. **Etherscan UI:** `https://etherscan.io/address/[ADDRESS]#code`
4. **Blockscout (L2):** `https://[chain].blockscout.com/address/[ADDRESS]/contracts`

If any page is JS-rendered and returns no content, fall back to web search immediately — do not halt.

---

## Step 4 — Route by Focus

**Always first** → Run `skills/product-assessor/SKILL.md`: one primary workflow pass, one failure-path pass, AA readiness when claimed.

**Focus `bugs` or `both`** → Run `skills/web3-audit/SKILL.md`. Proof discipline — no speculative findings.

**Focus `improvements` or `both`** → Run `skills/arch-advisor/SKILL.md`. Benchmark against the source registry; identify upgrade paths, integration gaps, scaling limitations.

**Always** → Run `skills/ceo-advisor/SKILL.md`: market opportunities in this category, what competitors are doing, what the team should build next.

---

## Step 5 — Save and Output

Update `memory/protocols/[slug]/`: `profile.md` · `findings.md` · `working-memory.md` · `next-actions.md`

Write to `audit-output/`: `[slug]-product-[YYYYMMDD].md` · `[slug]-audit-[YYYYMMDD].md` (if bugs) · `[slug]-arch-[YYYYMMDD].md` (if improvements) · `[slug]-strategy-[YYYYMMDD].md`

Print summary: protocol overview (2 sentences) · top 3 security findings or leads · top 3 architecture opportunities · top 2 strategic recommendations · suggested next command.
