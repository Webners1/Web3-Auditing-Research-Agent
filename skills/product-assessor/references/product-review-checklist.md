# Product Review Checklist

Use this checklist to make the non-contract review concrete and repeatable.

---

## 1. Product Clarity

- What problem does the product solve?
- Who is the intended user?
- What is the core action a user takes?
- What must happen onchain vs offchain?
- Is the value proposition clear without insider context?

Red flags:
- The frontend does many things but the protocol has no clear wedge
- Revenue depends on future token appreciation rather than present utility
- The docs overstate decentralization or automation

---

## 2. User Journey and Wallet Safety

- Are approvals bounded or unlimited by default?
- Are message signatures understandable to users?
- Are slippage and deadline controls exposed?
- Is chain switching explicit and safe?
- Can users verify the contract addresses they are interacting with?

Red flags:
- Blind signature requests
- Hidden approvals or silent router changes
- No warning for stale price or bridge delays

---

## 3. App Flow and UX Maturity

- Can a first-time user complete one core flow without external help?
- Is the next action obvious on each screen?
- How many decision points and dead ends appear in the core flow?
- Are loading, empty, and error states explicit and actionable?
- Can users recover from mistakes (wrong network, rejected tx, stale quote) quickly?

Red flags:
- Users must guess where to go next after wallet connect
- Core actions require excessive clicks or backtracking
- Failed transactions provide generic errors with no next step
- Refresh/back-button behavior loses critical context unexpectedly

---

## 4. Smart Wallet and Account Abstraction Readiness (Conditional)

Run this section only when the product uses or claims smart-wallet/account-abstraction capabilities. If it does not, mark `Not Applicable` with a brief reason.

- Is the wallet model explicit (EOA, multisig, ERC-4337 smart account)?
- If gas sponsorship is claimed, is paymaster behavior documented and bounded?
- Is UserOperation failure handling clear (bundler rejection, paymaster depletion, fallback path)?
- Are replay and nonce assumptions explicit?
- Is there support for contract signatures where needed (EIP-1271)?
- If session keys exist, are permissions, limits, expiry, and revocation enforceable?

Red flags:
- "Gasless" claims without a concrete paymaster policy
- No fallback UX when ERC-4337 infrastructure is unavailable
- Session keys with broad permissions and no revocation path
- Smart wallet support exists in docs but not in deployment/config

If not applicable:
- Product has no smart-account path and does not rely on delegated signatures
- No gas sponsorship promises exist in docs or UI

---

## 5. Trust Boundary Map

Map each component and record who controls it:

| Component | Role | Controlled by | Fails how |
|-----------|------|---------------|-----------|
| Frontend config | Address routing | Team admin | Points users to wrong contracts |
| Relayer | Gas abstraction | Team backend | Censors or delays actions |
| Oracle | Price feed | Third party | Bad pricing and liquidations |
| Multisig | Emergency powers | Team signers | Abuse or key compromise |

Always answer:
- What can the team change immediately?
- What can the team pause?
- What can the team drain or redirect?
- What can users verify independently?

---

## 6. Offchain Infrastructure

- Does the product rely on a private API?
- Is there an indexer or offchain matching engine?
- Are keepers or liquidation bots required?
- Are there cross-chain relayers?
- Is there a cloud dependency that can halt the product?

Red flags:
- A single offchain worker is necessary for solvency or withdrawals
- No fallback when the indexer or API fails
- The protocol markets itself as trustless but settlement depends on centralized operators

---

## 7. Governance and Operations

- Are admin keys on EOAs or multisigs?
- Are upgrades behind a timelock?
- Is there an emergency pause?
- Is there an incident response plan?
- Are there roles for guardian, risk manager, or operations?

Red flags:
- Single signer controls upgrades and treasury
- No pause, no kill-switch, and no monitoring
- Incident response is implied but not documented

---

## 8. Token, Incentives, and Business Model

- How does the protocol capture value today?
- Does the token do something other than emissions and governance theater?
- Are incentives sustainable without constant subsidies?
- Is liquidity sticky or purely mercenary?
- Is the fee model compatible with user behavior?

Red flags:
- Token exists without real utility or governance rights
- Rewards exceed credible revenue
- Product requires liquidity mining forever to function

---

## 9. Scoring Guide

Use a simple score for each category:

| Score | Meaning |
|-------|---------|
| 5 | Clear, robust, and well-disclosed |
| 4 | Mostly strong with minor gaps |
| 3 | Functional but meaningful gaps remain |
| 2 | Weak and likely to create user or execution risk |
| 1 | Broken, opaque, or dangerously centralized |

Convert low scores into plain-language recommendations, not just numbers.

---

## 10. 2026 Web3 Market-Readiness Scorecard

Score and evidence required for each dimension:

| Dimension | Score (1-5) | Evidence | Gap to Close |
|-----------|-------------|----------|--------------|
| UI/UX and flow resilience | | | |
| Security posture and incident readiness | | | |
| Smart contract quality and test maturity | | | |
| Docs, GitHub, and presentation quality | | | |
| Product clarity and category fit | | | |
| Business durability and future relevance | | | |
| Stack competitiveness vs function-matched peers | | | |

Rules:
- Use at least one direct functional peer and one one-curve-ahead peer when scoring competitiveness.
- Avoid protocol-name defaults; match by user job and architecture fit.
- For each score <= 3, provide a concrete fix with owner and expected impact.
