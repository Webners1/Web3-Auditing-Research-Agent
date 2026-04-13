# Access Control Agent

**Domain:** Role mismanagement, privilege escalation, missing auth checks, signature security, initializer bugs

Read `shared-rules.md` first. Then execute this analysis.

---

## Step 1 — Map All Privileged Functions

Find all functions with access control:
```bash
grep -n "onlyOwner\|onlyRole\|onlyAdmin\|onlyMinter\|require(msg.sender\|_checkRole\|_onlyOwner\|modifier only" --include="*.sol" -r .
```

Build a table: function name → required role/address.

Then find ALL state-changing functions WITHOUT access control:
```bash
grep -n "function.*external\|function.*public" --include="*.sol" -r .
```
Cross-reference: which public/external state-changing functions have NO access control? Each one needs a justification (permissionless design) or is a potential bug.

---

## Step 2 — Role Hierarchy Check

Find role definitions:
```bash
grep -n "bytes32.*ROLE\|keccak256.*ROLE\|AccessControl\|grantRole\|revokeRole" --include="*.sol" -r .
```

Check:
- Who can grant each role? (DEFAULT_ADMIN_ROLE holder can grant all OZ roles — is this intended?)
- Can a low-privilege role escalate to a higher one?
- Is there a separation between admin, operator, and emergency roles?

---

## Step 3 — tx.origin Check

```bash
grep -n "tx\.origin" --include="*.sol" -r .
```

Any `require(tx.origin == ...)` is an immediate HIGH:
- Bypass by deploying an intermediary contract
- Phishing attack vector

---

## Step 4 — Signature Security Audit

Find all signature verification:
```bash
grep -n "ecrecover\|recover\|ECDSA\|_hashTypedDataV4\|EIP712\|permit\|signedMessage" --include="*.sol" -r .
```

For each signature check:
1. **Nonce present?** — missing nonce = replay attack
2. **Domain separator present?** — missing = cross-chain replay
3. **ecrecover address(0) check** — `require(signer != address(0) && signer == recovered)`
4. **Deadline present?** — missing = signatures valid forever
5. **EIP-712 typed hash** — raw `abi.encodePacked` without struct type = hash collision risk

---

## Step 5 — Initializer Security

```bash
grep -n "initialize\|__init\|initializer\|_disableInitializers" --include="*.sol" -r .
```

Check:
- Does every `initialize()` function have the `initializer` modifier?
- Does the implementation contract constructor call `_disableInitializers()`?
- Can `initialize()` be called multiple times if modifier is omitted?
- Are all inherited `__X_init()` functions called in the correct order?

---

## Step 6 — Emergency/Pause Functions

```bash
grep -n "pause\|unpause\|emergency\|circuit\|guardian\|setEmergency" --include="*.sol" -r .
```

Check:
- Who can pause? Is this appropriate for the trust level?
- Can pause be used to freeze user funds indefinitely? (rug risk)
- Is unpause appropriately restricted?

---

## Step 7 — Ownership Transfer

```bash
grep -n "transferOwnership\|Ownable2Step\|pendingOwner\|acceptOwnership\|renounceOwnership" --include="*.sol" -r .
```

Check:
- Is `Ownable2Step` used (two-step transfer)? Single-step = HIGH risk of owner being set to wrong address
- Is `renounceOwnership()` accessible? If yes, could irrecoverably brick the protocol
- After ownership transfer, are all roles transferred too?

---

## Step 8 — Sensitive State Setter Functions

Find all setters for important protocol parameters:
```bash
grep -n "set[A-Z]\|update[A-Z]\|change[A-Z]\|configure" --include="*.sol" -r .
```

For each setter of a price-sensitive or security-sensitive value:
- Is there a timelock? (should be for mainnet protocols)
- Is there an upper/lower bound check? (admin setting 0 fee = full drain, etc.)
- Is there an event emitted for transparency?

---

## Output Template

```
FINDING | contract: Vault | function: initialize | bug_class: unprotected-initializer | severity: CRITICAL
path: attacker → Vault.initialize(attackerAddress) → owner = attackerAddress
proof: no initializer modifier; Vault impl deployed without _disableInitializers(); anyone can call initialize() on the implementation
description: Unprotected initializer on implementation contract allows anyone to take ownership and selfdestruct it, bricking all proxy deployments
fix: add _disableInitializers() to constructor; ensure initializer modifier is present on initialize()
```
