# Remediation Fix Patterns

Use these patterns as a starting point, then adapt them to the protocol.

---

## 1. Reentrancy

Preferred order:
1. Reorder to checks-effects-interactions
2. Add `nonReentrant` if the call graph allows it
3. Split state mutation from external interaction if needed

Do not stop at `add nonReentrant` if the underlying accounting remains fragile.

---

## 2. Access Control

Preferred order:
1. Restrict privileged entry points
2. Move sensitive actions to multisig or timelock
3. Use `Ownable2Step` or role-based access with explicit admin separation
4. Add event coverage for all admin actions

Good pattern:
- Guardian for emergency pause
- Timelock for normal governance changes
- Multisig as the owner of upgrade and treasury roles

---

## 3. Oracle and Pricing

Preferred order:
1. Replace spot price reads with robust oracle sources
2. Add staleness and sanity checks
3. Add deviation bounds and kill-switches
4. Design fallback behavior for oracle downtime

Good pattern:
- Chainlink or equivalent primary oracle
- Secondary validation source where economic exposure is material

---

## 4. Accounting and Invariants

Preferred order:
1. State the invariant explicitly
2. Recompute the critical math path with rounded direction in mind
3. Add invariant tests and edge-case fixtures
4. Isolate conversions between assets, shares, debt, and price units

Good pattern:
- Centralize conversion helpers
- Normalize decimals once
- Round against the user when the protocol must stay solvent

---

## 5. Upgradeability

Preferred order:
1. Harden upgrade authorization
2. Validate storage layout
3. Add `_disableInitializers()` and storage gaps where needed
4. Put upgrades behind timelock and simulation

Good pattern:
- UUPS or Transparent proxy with multisig/timelock control
- Dry-run upgrade in staging or fork before production

---

## 6. External Integrations

Preferred order:
1. Minimize trust in external callbacks
2. Validate return values and balances
3. Add allowlists or routing constraints where needed
4. Add emergency off-switches for integrations

Good pattern:
- Integration adapter layer
- Explicit per-protocol limits
- Monitoring around dependency failure

---

## 7. Deployment and Rollout

Always answer:
- Can this be hotfixed in place?
- Does this require migration?
- What user communication is needed?
- Does the patch change trust assumptions?
- What must be re-audited after the fix?
