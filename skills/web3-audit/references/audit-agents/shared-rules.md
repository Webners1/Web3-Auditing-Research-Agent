# Shared Rules — All Audit Agents

Every agent reads this file before running analysis. These rules apply universally.

---

## Output Format (Mandatory)

Use EXACTLY this format. No deviation.

```
FINDING | contract: ContractName | function: functionName | bug_class: kebab-tag | severity: CRITICAL|HIGH|MEDIUM|LOW|INFO
path: caller → function1() → function2() → state change → impact
proof: concrete values, balances, or trace that demonstrates the bug
description: one sentence — what is the vulnerability and what does an attacker gain?
fix: one sentence — the specific code change needed
---
LEAD | contract: ContractName | function: functionName | bug_class: kebab-tag | severity: HIGH|MEDIUM|LOW
code_smells: what specific code pattern triggered investigation
description: one sentence — what remains unverified and why this needs manual review
```

**FINDING** = confirmed exploit path with concrete proof
**LEAD** = suspicious pattern, no full confirmation yet

---

## What To Look For

### Always check
- All state-changing external calls (`.call`, `.transfer`, `.delegatecall`, `token.transfer`)
- All privileged functions (`onlyOwner`, `onlyRole`, `initializer`)
- All arithmetic involving token amounts, shares, or prices
- All access control checks (present? correct? bypassable?)
- All external contract interactions (trust boundary?)
- All `unchecked` arithmetic blocks (is the safety assumption documented and correct?)

### Specific to Solidity version
- Pre-0.8.0: ALL arithmetic is unchecked — look for overflow in amount calculations
- 0.8.0+: `unchecked` blocks re-enable wrapping — scrutinize them individually

---

## What NOT to Flag

- `unchecked` blocks with documented justification and correct safety bounds
- `SafeERC20` wrapper usage
- `nonReentrant` modifier on a function (but still check cross-contract reentrancy)
- Two-step ownership transfers (they're the fix, not the bug)
- MINIMUM_LIQUIDITY permanent burns in AMM pools
- Explicit narrowing casts in tight arithmetic loops with documented bit bounds
- Intentional protocol-favoring rounding (document that you noticed it, but don't flag as finding)

---

## Cross-Agent Coordination

- If you find a vulnerability that spans multiple domains, flag it in your output and note which other agent should also examine it
- Example: Flash loan + oracle manipulation → Economic Agent flags it, notes Periphery Agent should check the oracle callback

---

## Scope Boundaries

- **In scope:** Production contracts in `src/`, `contracts/`
- **Out of scope:** `test/`, `tests/`, `mocks/`, `lib/`, `node_modules/`, contracts explicitly labeled as mock or test
- If a contract is inherited by an in-scope contract, check it for inherited bugs but note the source

---

## Severity Guidelines

| Level | Standard |
|-------|---------|
| CRITICAL | Direct fund loss, any caller, no special conditions |
| HIGH | Significant fund loss, realistic conditions (flash loan, price window) |
| MEDIUM | Partial loss, griefing, or DoS under specific conditions |
| LOW | Best practice violations without direct impact |
| INFO | Gas, style, documentation |

---

## Confidence Discipline

- Start confident, deduct:
  - -20 if you can only partially trace the exploit path
  - -15 if the impact is bounded by a realistic parameter
  - -10 if a non-obvious protocol state is required
- Score ≥ 80: FINDING with full PoC
- Score 60-79: FINDING with noted uncertainty
- Score < 60: LEAD

---

## Protocol-Aware Thinking

Before flagging anything, ask:
1. What is this protocol designed to do?
2. Is this behavior potentially intentional?
3. Does the protocol's economic design protect against this?

Do not flag "admin can rug" as a critical finding — admin trust is a design choice, not a vulnerability. Flag it as LOW or INFO.
