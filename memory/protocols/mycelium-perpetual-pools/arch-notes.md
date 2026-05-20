# Mycelium Perpetual Pools — Architecture Notes
Date: 2026-05-20

## Architecture Assessment

**Upgrade Path:** None. Contracts use minimal proxy (Clones) pattern — individual pool contracts are NOT upgradeable. Only a fresh deployment can fix issues. The PoolFactory owner could deploy new pools with fixed OracleWrapper contracts, but existing pools cannot be patched.

**This is the core architectural constraint for the pitch:** fixing FINDING-001 requires either:
1. A new OracleWrapper deployment + migrating TVL to new pools (complex, requires user action)
2. The pool remains vulnerable until the last user withdraws

**Modularity:** Reasonable separation — PoolFactory, PoolKeeper, LeveragedPool are distinct. But:
- Oracle abstraction (OracleWrapper) is deployed per pool at construction time
- Can't swap oracle implementation without redeploying pools
- No oracle upgrade path = architectural gap for a maturing protocol

**Keeper Architecture:** Permissionless with economic incentive. The design is correct in principle (permissionless keepers improve liveness), but the keeper reward bug (FINDING-002) undermines it. If rewards are ~0, only protocol-operated keepers will run upkeep. This creates a single point of failure.

**Protocol Status Assessment:**
- Perpetual Pools: $183k TVL, "Close Positions" UI — in wind-down
- Perpetual Swaps: $0 TVL — effectively defunct
- No evidence of active development since 2022

## Phase Handoff
- Protocol: Mycelium Perpetual Pools
- Chain: Arbitrum One
- Key finding from this phase: Non-upgradeable contracts mean existing pools cannot be patched. The L2 sequencer vulnerability persists until all users withdraw.
- Open question for next phase: Is responsible disclosure more appropriate than a sales pitch here?
- Skip next phase? Run a brief strategy pass — need to determine correct pitch angle.
