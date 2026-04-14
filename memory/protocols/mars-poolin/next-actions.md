# Mars Poolin — Next Actions

**Last updated:** 2026-04-13
**Current phase:** Audit complete → Remediation + Architecture advisory pending

## Immediate (if engaging with the protocol team)

1. **Share audit report** — `audit-output/mars-poolin-audit-20260413.md`
2. **Share strategy audit deep dive** — `audit-output/mars-poolin-business-expand-20260413.md`
3. **Request confirmation** on M-06 design intent — is the `exchange(to)` pattern deliberate or a bug?
4. **Verify owner EOA** is still active and not compromised

## Next Workflow Steps

- Run `/remediation-architect mars-poolin` to design precise fixes for M-01 through M-06
- Run `/arch-advisor mars-poolin` to plan multisig + timelock + Chainlink oracle upgrade path
- Run `/ceo-advisor mars-poolin` if team wants to relaunch with v2 (MARS emission ended, protocol is in maintenance mode)
- Run `/expand-business mars-poolin` to enforce KPI-based strategy execution gates (trust -> composability -> expansion)

## Strategy Audit Priority Gates (2026)

1. **Gate A: trust hardening complete** before any expansion campaign
2. **Gate B: composability integration pilots live** before multichain expansion
3. **Gate C: KPI loop active** (retention, integration conversion, incentive efficiency) before advanced product launches

## Open Questions

- Is there a team contact? The protocol appears to be in maintenance/wind-down mode post Dec 2024
- Does the team intend to upgrade the proxy to a modern EIP-1967 implementation?
- What is the current wBTC balance in POWToken? (determines M-01 blast radius)
- Is paramSetter still an active EOA or a contract?
