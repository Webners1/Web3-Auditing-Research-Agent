# Security Architecture Baseline

This file defines the minimum architecture controls expected from a serious Web3 product.

---

## 1. Control Stack

Recommended baseline:
1. Multisig ownership for protocol-critical authority
2. Timelock for non-emergency governance actions
3. Guardian or pause authority for emergencies
4. Monitoring and alerting around critical events
5. Runbooks for incident response and upgrades

---

## 2. Contract Controls

- `Ownable2Step` or role-based access with explicit admin separation
- Pause mechanism for high-blast-radius actions
- Rate limits or caps for minting, borrowing, bridging, or withdrawals
- Oracle staleness and deviation checks
- Upgrade authorization isolated from day-to-day operations

---

## 3. Operational Controls

- Multisig signer policy and signer rotation
- Deployment checklist and fork-based rehearsal for upgrades
- Alerting on admin events, pauses, large fund movements, and oracle failures
- Public disclosure of trust assumptions and emergency controls

---

## 4. Validation Controls

- Unit tests for all critical branches
- Invariant tests for solvency and accounting
- Fuzz tests for edge-case math and state transitions
- Independent review before major launch or upgrade
