# Finding Validation Framework — 4-Gate Model

Every FINDING must pass all 4 gates sequentially. Failure at any gate downgrades to LEAD or drops.

---

## Gate 1 — Refutation (Does a guard block it?)

Ask: Is there an existing mechanism that concretely prevents this exploit?

**Concrete guards that refute findings:**
- `nonReentrant` modifier blocking the specific call path
- Access control check (`onlyOwner`, `onlyRole`, `require(msg.sender == admin)`) protecting the vulnerable function
- `address(0)` check preventing null-target delegatecall
- Explicit input validation that bounds the exploitable parameter
- `Pausable` with demonstrated pause being active (only if invariant — not just "could be paused")

**What does NOT refute:**
- "The admin would notice" — not a code-level guard
- "It would be uneconomical" — economic argument, not a code guard (flag as MEDIUM if threshold is meaningful)
- "The probability is low" — irrelevant; likelihood affects severity, not validity
- Comments saying "this is safe"

**Result:** If a concrete, unconditional guard exists → drop to LEAD or remove.

---

## Gate 2 — Reachability (Can the vulnerable state exist?)

Ask: Is there a valid transaction sequence that reaches the vulnerable code path?

Check:
- Can the function be called when the precondition for vulnerability holds?
- Is the state transition required to reach the bug actually possible?
- Are there implicit invariants from the protocol design that prevent the state?

**Example (pass):** `withdraw()` is publicly callable, balance mapping can hold non-zero value after `deposit()` — state is reachable.

**Example (fail):** Vulnerability in `_emergencyWithdraw()` which is only callable by `msg.sender == address(0)` — state is unreachable.

**Result:** If state is provably unreachable → drop.

---

## Gate 3 — Trigger (Can an unprivileged actor cause it?)

Ask: Who can actually trigger this? Is the triggering actor realistic?

**Unprivileged actor** = any EOA or contract that interacts with the protocol without special permissions.

Considerations:
- If only admin can trigger it: severity → LOW or INFO (admin trust assumption)
- If governance multisig can trigger it: flag as governance risk, severity based on timelock delay
- If requires MEV bot or specific block timing: still HIGH if economically viable
- If requires flash loan: still valid if flash loan is available on that chain

**Result:** If only owner/admin can trigger with no realistic path to key compromise → downgrade severity by 1 level.

---

## Gate 4 — Impact (Is the harm material?)

Ask: What does the attacker concretely gain or what does the protocol/user lose?

**Material impacts:**
- ETH or token theft (any amount)
- Permanent contract lock (not self-DoS)
- Unauthorized minting or burning
- State corruption affecting future transactions
- Bypassing slippage/price guarantees to extract value

**Non-material (INFO/LOW):**
- Revert-causing calls with no state change
- Single-user self-DoS (attacker can only harm themselves)
- Events emitted with wrong values but no state effect

**Confidence scoring:**
- Start at 100
- Partial call path only (cannot trace end-to-end): -20
- Impact bounded by a parameter value: -15
- Requires specific, non-obvious protocol state: -10
- Score ≥ 80 → FINDING with full description + PoC
- Score 60-79 → FINDING with description, note uncertainty
- Score < 60 → LEAD

---

## Escalating a LEAD

A LEAD can be escalated to FINDING if:
- Subsequent analysis fills the proof gap
- Another agent independently confirms the same path
- Slither/Aderyn output corroborates the finding

Document escalation reason in the finding notes.
