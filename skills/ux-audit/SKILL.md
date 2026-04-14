---
name: ux-audit
description: Web3 UX audit — scores a dApp's design quality, user flow, wallet experience, trust signals, error handling, and competitive design positioning. Part of the Product Trust pillar.
---

# Web3 UX Auditor

Assesses the real user experience of a Web3 dApp — not just whether it works, but whether it communicates trust, converts new users, retains existing ones, and differentiates from competitors through design quality. This is the Pillar 2 UX component: good UX is a trust signal, a retention lever, and a competitive differentiator. Poor UX is a business risk with measurable TVL and conversion cost.

**Trigger phrases:** `ux audit`, `check the ux`, `review the ui`, `audit the app`, `check the design`, `how does the product look`, `is the ux good`, `user experience review`, `app flow audit`, `/ux-audit`

---

## Execution Pipeline

### Phase 1 — Surface Collection

Collect all available UX evidence before scoring anything:

1. **Live app** — primary URL and any staging/testnet URLs
2. **Frontend source** — `app/`, `src/`, `frontend/`, `web/` directories if available
3. **Design system** — component libraries, Tailwind config, design tokens if present
4. **Mobile presence** — whether a mobile version or PWA exists
5. **Screenshots or recordings** — if the user provides them
6. **Competitor references** — identify 2–3 function-matched protocols in the same category to use as design benchmarks (find protocols that are growing in this category per DefiLlama data — not just the largest by TVL)

If source code is unavailable, work from the live URL, the docs site, and any available screenshots. Record what was and was not accessible.

---

### Phase 2 — UX Dimension Scoring

Score each dimension: **Strong** / **Mixed** / **Weak**

For every dimension rated Mixed or Weak: identify the specific failing, cite a named protocol doing it better, and state the specific trust or conversion cost.

---

#### 2.1 Visual Design & Brand Trust

**What it measures:** Whether design quality communicates professionalism, safety, and competence to a first-time visitor.

Check:
- Does the visual language feel consistent and intentional — or does it look like a template or rushed bootstrap?
- Is typography legible and hierarchy clear for key data (APY, TVL, balances, contract addresses)?
- Are colors, spacing, and component styles consistent, or is there visual fragmentation?
- Does the brand have a distinct identity, or is it visually identical to a generic fork?
- Does the design look current for 2026, or does it feel like it hasn't been touched since 2021?

**Specificity requirement:** If rated Weak, name a protocol in the same category with a demonstrably stronger design and say specifically what it does better. "Pendle Finance redesigned their dashboard in 2024 with a component-based design system that made complex yield split positions readable at a glance — this drove a reported 3x increase in dashboard session length" is a finding. "Your design could be improved" is not.

---

#### 2.2 First Impression & Value Clarity

**What it measures:** Whether a new visitor understands what the protocol does and who it's for within 10 seconds, without reading a whitepaper.

Check:
- What is visible above the fold before connecting a wallet?
- Is the primary value proposition (what you can do, what you earn, why this vs alternatives) stated clearly?
- Is there a clear primary call to action?
- Is the language plain enough for a non-expert, or does it assume deep DeFi literacy?
- Are key metrics (TVL, APY, active users) shown prominently to establish credibility?

**Trust connection:** Clarity = trust. A protocol that cannot explain itself in 10 seconds signals poor communication and makes users question whether the team knows their users.

---

#### 2.3 Wallet Connection Flow

**What it measures:** How many steps, decisions, and potential failures stand between a user opening the app and having a connected wallet ready to transact.

Check:
- How many clicks to go from landing page to connected state?
- Which wallets are supported (MetaMask, WalletConnect, Coinbase Wallet, Safe, Rainbow)?
- Is network detection automatic — does the app detect wrong network and prompt a switch, or does it silently break?
- Is network switching a single click with a confirmation prompt?
- What happens if the user has no wallet installed? (Clear install guidance, or blank state/error?)
- What happens if WalletConnect fails to connect? (Retry option or broken state?)

**Severity classification for issues found:**
- Wrong network breaks all functions silently → CRITICAL UX
- No support for WalletConnect (mobile users excluded) → HIGH UX
- Multi-step network switching with no guidance → MEDIUM UX
- No wallet install guidance for new users → MEDIUM UX

---

#### 2.4 Core Transaction Flow

**What it measures:** The experience of completing the primary user action — staking, swapping, depositing, borrowing, claiming.

Walk through the primary flow step by step and record:
1. Entry point — where does the user start?
2. Input — is it clear what to enter, what units, what limits?
3. Risk communication — are slippage, price impact, liquidation risk, or lock-up periods shown before signing?
4. Gas estimation — shown before the wallet prompt, or discovered at wallet?
5. Wallet prompt — is the signing request readable (decoded) or a hex blob?
6. Pending state — is there a clear in-progress indicator?
7. Success state — confirmation with relevant outcome data (what the user now has, what changed)?
8. Failure state — decoded error or raw revert?

**Multi-step flows:** If the action requires approve + execute (two transactions), is this explained upfront or does it surprise the user?

**Specificity requirement:** For every step that fails, name a protocol that handles it correctly and describe the specific implementation. "Uniswap v3 shows gas cost, price impact, and minimum received before any wallet prompt — users make an informed decision before signing. This protocol presents the wallet prompt without any of these, leading to uninformed transaction confirmations and higher abandonment at the signing step."

---

#### 2.5 Error Handling & Failure Recovery

**What it measures:** What users see when things go wrong — which is where trust is won or permanently lost.

Check every failure path that is reachable:
- Transaction reverted: is the error message decoded and human-readable, or is it a raw hex code or "execution reverted"?
- Insufficient balance or allowance: does the UI prevent submission or only fail at wallet prompt?
- Gas estimation failure: is there a clear explanation and retry path?
- Network timeout or RPC failure: graceful degradation or blank state?
- Contract under maintenance or paused: is there a clear notice?
- User rejects the wallet prompt: does the UI recover cleanly or freeze?

**Trust connection:** Bad error handling is a trust failure. A user who sees an opaque error message loses confidence in the protocol regardless of the smart contract quality underneath. This is often the first impression for new users who encounter problems.

---

#### 2.6 Trust Signals in the UI

**What it measures:** Whether the app itself actively communicates trustworthiness through its design — not just through what you find by Googling.

Check:
- Is the deployed contract address(es) visible in the app and linked to a block explorer?
- Are audit reports linked from within the app (footer, about page, or risk disclaimer)?
- Is there a clearly stated security risk disclosure?
- Is the team or entity behind the protocol identified somewhere accessible?
- Is there a link to a bug bounty program?
- Is the HTTPS certificate valid and not flagged?
- Are governance and admin controls disclosed (e.g., "this parameter is controlled by a 3/5 multisig")?

**Competitive context:** Aave, Compound, and Morpho all surface audit reports and contract addresses within 2 clicks from the main app. Protocols that do not surface this information signal opacity, which suppresses institutional and serious retail adoption. In 2026, omitting trust signals from the UI is a competitive disadvantage, not a neutral choice.

---

#### 2.7 Mobile & Cross-Browser Experience

**What it measures:** Whether users on mobile devices can transact — relevant because mobile WalletConnect and MetaMask Mobile represent a significant share of DeFi users in 2026.

Check:
- Is the layout responsive and usable on common mobile screen sizes (375px and 430px width)?
- Does WalletConnect v2 work for mobile wallet pairing?
- Are touch targets large enough (minimum 44×44px for buttons)?
- Does the UI degrade gracefully on mobile or break key functionality?
- Does it work across Chrome, Firefox, and Safari (important for iOS users)?

---

#### 2.8 Information Architecture & Navigation

**What it measures:** Whether users can find what they need — their positions, history, docs, help — without searching.

Check:
- Can a user find their current position (deposited amounts, earned rewards, lock-up end date) within 2 clicks?
- Is transaction history accessible?
- Is navigation labeled in plain language or in protocol-internal jargon?
- Are DeFi concepts explained inline (tooltips, help text) at the point of use?
- Is there a clear path to documentation or support?

---

#### 2.9 Performance & Loading States

**What it measures:** Whether the app signals life during loading — critical in DeFi where RPC calls, price feeds, and blockchain data can take several seconds.

Check:
- Are loading states shown for data that takes time to fetch (balances, APYs, positions)?
- Are skeleton screens or spinners used, or does the page appear broken while loading?
- Does the app handle stale data gracefully (show last-known state while refreshing)?
- Are there obvious performance problems (slow load, janky scroll, unresponsive inputs)?

---

### Phase 3 — UX Score Summary

Produce a summary table:

```markdown
| Dimension | Status | Key Finding | Named Comparison |
|-----------|--------|-------------|-----------------|
| Visual Design & Brand Trust | Strong / Mixed / Weak | [specific finding] | [protocol doing it better] |
| First Impression & Value Clarity | Strong / Mixed / Weak | | |
| Wallet Connection Flow | Strong / Mixed / Weak | | |
| Core Transaction Flow | Strong / Mixed / Weak | | |
| Error Handling & Recovery | Strong / Mixed / Weak | | |
| Trust Signals in UI | Strong / Mixed / Weak | | |
| Mobile & Cross-Browser | Strong / Mixed / Weak | | |
| Information Architecture | Strong / Mixed / Weak | | |
| Performance & Loading States | Strong / Mixed / Weak | | |
```

Then assign an overall **UX Posture**:

| Posture | Criteria |
|---------|---------|
| **Production-Ready** | 7+ Strong, no Critical/High issues |
| **Needs Work** | Mixed across dimensions, 1–2 High issues |
| **Significant Gap** | 3+ Weak dimensions or any Critical issue |
| **Blocking** | Primary user action cannot be completed |

---

### Phase 4 — UX Findings (Severity-Ranked)

For each issue found, produce a structured finding:

```
UX-[N] | [CRITICAL / HIGH / MEDIUM / LOW]
Flow: [which flow — connection / transaction / error / navigation / mobile]
Observation: [specific observable problem with evidence]
Trust / Conversion Impact: [what this costs — abandonment rate, trust failure, integration blocker]
Named Reference: [protocol that handles this correctly + what they do specifically]
Fix: [concrete, implementable action — not "improve this" but "add a decoded error message using ethers.js parseError() + display it above the retry button"]
Effort: [Easy / Medium / Hard]
```

**Severity definitions:**
- **CRITICAL** — primary user action is blocked or impossible
- **HIGH** — significant conversion or retention damage, or trust signal failure visible to first-time users
- **MEDIUM** — professional standing gap or friction that experienced users work around but new users abandon
- **LOW** — polish, differentiation, and competitive positioning opportunity

---

### Phase 5 — Competitive UX Position

Rate this protocol's UX against its function-matched category peers:

```markdown
| Protocol | UX Posture | Key Differentiator | Gap vs This Protocol |
|----------|-----------|-------------------|---------------------|
| [Peer 1] | | | |
| [Peer 2] | | | |
| [This protocol] | | | |
```

End with one honest paragraph on where UX is currently a competitive disadvantage and what the single highest-leverage UX investment would be.

---

### Phase 6 — Output

If running standalone:
```
audit-output/[project-name]-ux-[YYYYMMDD].md
```

If running as part of `product-assessor`, return results directly for Phase 2 integration — the UX Posture, the summary table, and all HIGH/CRITICAL findings.

---

## UX Audit Rules

- **Specificity over generality** — "your design looks outdated" is not a finding. "The protocol uses a non-standard grey background color scheme that does not match the dark/light mode convention used by every comparable protocol in this category since 2023, creating a first-impression trust gap" is a finding.
- **Named comparisons required** — every Medium or above finding must name a protocol doing it better and say specifically what they do.
- **Trust lens always on** — frame every UX issue in terms of its trust or conversion consequence, not just its cosmetic impact. UX is part of Pillar 2 (Product Trust), not cosmetic polish.
- **Do not conflate UX with smart contract security** — a beautiful UI can sit on top of broken contracts. Keep the layers separate.
- **Primary flows first** — do not spend time auditing edge cases until the primary flow is fully assessed.
- **Distinguish platform constraint from design choice** — some limitations come from wallet providers or chain constraints. Separate what the protocol team owns vs what is external infrastructure.
