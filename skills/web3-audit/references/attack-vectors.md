# EVM Vulnerability Taxonomy

Reference for all 8 audit agents. Each agent focuses on its designated categories but should cross-reference related categories when paths intersect.

---

## 1. Reentrancy

### 1.1 Classic ETH Reentrancy
- External `.call{value}()` before state update
- Pattern: check → interact → effects (wrong CEI order)
- Fix: checks-effects-interactions; `nonReentrant`

### 1.2 ERC-20 Reentrancy
- Tokens with transfer hooks (ERC-777, fee-on-transfer, rebase)
- `token.transfer()` or `token.transferFrom()` before state update
- Fix: update balances before token transfers

### 1.3 Cross-Function Reentrancy
- State updated in `functionA` but read in `functionB` before `functionA` completes
- Example: `deposit()` sets shares, `withdraw()` reads shares — attacker reenters `withdraw()` during `deposit()`
- Fix: `nonReentrant` on all state-touching entry points; or use commit-reveal

### 1.4 Cross-Contract Reentrancy
- Protocol calls external contract; external contract calls a different function in the same protocol
- Common in AMMs with flash swaps and lending protocols with flash loans
- Fix: ensure all state is finalized before any external call

### 1.5 Read-Only Reentrancy
- Attacker reenters a `view` function during a state-changing call
- Relevant if another protocol reads state via that view function
- Example: Curve LP price `get_virtual_price()` manipulation during remove_liquidity

### 1.6 ERC-721/1155 Reentrancy
- `onERC721Received`, `onERC1155Received`, `onERC1155BatchReceived` hooks
- `safeTransfer*` triggers receiver hooks
- Fix: state updates before safe transfers; `nonReentrant`

---

## 2. Access Control

### 2.1 Missing Access Control
- Function missing `onlyOwner`, `onlyRole`, or equivalent guard
- Especially dangerous on: `mint`, `burn`, `setPrice`, `upgradeTo`, `initialize`, `emergencyWithdraw`

### 2.2 Incorrect Role Assignment
- Admin can grant arbitrary roles to any address
- Role hierarchy confusion (role A should not implicitly grant role B)

### 2.3 Privilege Escalation
- A user with limited role calls a function that grants them a higher role
- Example: `MINTER_ROLE` can call `grantRole(ADMIN_ROLE, self)`

### 2.4 tx.origin Authentication
- `require(tx.origin == owner)` — bypassed by any intermediary contract
- Fix: always use `msg.sender`

### 2.5 Signature Replay
- Signed messages without nonce or domain separator
- Same signature can be replayed on a different chain or re-used
- Fix: EIP-712 with nonce + domain separator; track used signatures

### 2.6 ecrecover Misuse
- `ecrecover` returns `address(0)` on invalid signatures
- `require(signer == ecrecover(...))` passes if `signer == address(0)`
- Fix: `require(recovered != address(0) && recovered == signer)`

### 2.7 Function Selector Clashing
- Two functions with same 4-byte selector (intentional or collision)
- In proxy contracts: malicious implementation can shadow proxy admin functions
- Fix: check for selector collisions in proxy/diamond patterns

### 2.8 Unprotected Initializer
- `initialize()` function without `initializer` modifier
- Can be called again by anyone after deployment
- Fix: OpenZeppelin `Initializable` pattern; `_disableInitializers()` in constructor

---

## 3. Arithmetic & Precision

### 3.1 Integer Overflow/Underflow
- Pre-Solidity 0.8.0: unchecked arithmetic wraps around
- Post-0.8.0: reverts by default; but `unchecked` blocks re-enable wrapping
- Check all `unchecked` blocks for safety assumption correctness

### 3.2 Precision Loss via Integer Division
- Solidity truncates: `1000 / 3 = 333` (not 333.33)
- Accumulated rounding errors can drain a contract over many transactions
- Fix: multiply before dividing; use fixed-point libraries (PRBMath, FixedPoint)

### 3.3 Rounding Direction
- Protocol should always round in its own favor (against the user)
- Lending: round UP when calculating debt owed; round DOWN when calculating collateral
- Violations can be exploited to extract dust amounts at scale

### 3.4 Decimal Mismatch
- Token A: 18 decimals, Token B: 6 decimals — arithmetic must normalize
- Oracle prices: ensure price decimals match token decimals before division/multiplication

### 3.5 Phantom Overflow
- Expression intermediate exceeds uint256 range before assignment
- Example: `a * b / c` where `a * b` overflows before `/c` is applied
- Fix: restructure operations; use 512-bit multiplication for intermediates

### 3.6 Off-By-One Errors
- Boundary condition bugs: `>` vs `>=`, `<` vs `<=`
- Common in loops, epoch calculations, grace periods
- Always check that boundary values are correctly included/excluded

### 3.7 Type Casting Truncation
- `uint256` → `uint128` → `uint64` silently truncates bits
- Slither's `divide-before-multiply` and `tautology` detectors catch many of these

---

## 4. Oracle & Price Manipulation

### 4.1 Spot Price Oracle
- Using `reserve0/reserve1` from AMM as price feed
- Manipulable in a single transaction via flash loans
- Fix: use TWAP (time-weighted average price)

### 4.2 TWAP Manipulation
- Short TWAP windows (< 30 min) manipulable over multiple blocks
- Cascading oracle: TWAP derived from another manipulable price
- Fix: 30-minute minimum TWAP; Chainlink as primary oracle

### 4.3 Stale Price
- Chainlink `latestRoundData()` without staleness check
- Check: `require(block.timestamp - updatedAt < STALE_THRESHOLD)`
- Also check `answeredInRound >= roundId`

### 4.4 Oracle Downtime
- Protocol breaks or freezes when Chainlink oracle is down or in grace period
- Fix: fallback oracle; circuit breaker to pause protocol on oracle failure

### 4.5 Price Deviation
- Large single-block price movement exploited before on-chain oracle updates
- Use multiple independent oracles; revert if prices diverge beyond threshold

### 4.6 Sandwich Attack via Oracle
- Attacker manipulates oracle price, executes favorable trade, restores price
- All in one transaction via flash loan + AMM manipulation

---

## 5. Flash Loan Attacks

### 5.1 Governance Flash Loan
- Borrow tokens, vote, repay in one transaction
- Fix: snapshot voting power at prior block; require token lock period

### 5.2 Collateral Flash Loan
- Flash borrow collateral to pass health factor check, drain lending protocol
- Fix: health factor checks should use oracle price, not spot balance

### 5.3 Pool Ratio Manipulation
- Flash loan one asset, skew AMM ratio, exploit slippage calculation
- Fix: TWAP-based pricing for any rate-sensitive logic

### 5.4 Price Flash Loan
- Borrow large amount, move spot price, liquidate others, repay
- Common in combined lending + AMM protocols

---

## 6. MEV & Transaction Ordering

### 6.1 Front-Running
- Attacker sees pending transaction, submits same action with higher gas
- Victims: `approve` + `transferFrom` pattern; large trades with no slippage protection

### 6.2 Sandwich Attack
- Front-run + back-run a trade to extract value from slippage
- Fix: `minAmountOut` parameter in all swap functions

### 6.3 Commit-Reveal Manipulation
- Revealing phase can be front-run if reveal value is profitable
- Fix: time-delayed reveals; zero-knowledge commitments

### 6.4 Liquidation Race
- Multiple bots front-run each other on liquidation; MEV block stuffing
- Impact on protocol: partial liquidations, bad debt accumulation

---

## 7. Denial of Service

### 7.1 Unbounded Loop
- `for (uint i = 0; i < users.length; i++)` — gas limit DoS if array grows large
- Fix: off-chain enumeration; pagination; pull-based reward distribution

### 7.2 Push Payment DoS
- Contract pushes ETH to recipients; if one reverts, entire batch fails
- Fix: pull payment pattern — let users withdraw rather than pushing to them

### 7.3 Block Gas Limit
- Single operation requiring more gas than the block gas limit
- Fix: batch operations with size limits; asynchronous execution

### 7.4 Griefing via Revert
- Attacker creates state that forces other users' transactions to revert
- Example: frontrun `setApprovalForAll` to cause `transferFrom` in same tx to fail

### 7.5 Self-Destruct Griefing
- `selfdestruct` sending ETH to a contract breaks contracts that check `balance == 0`
- Never rely on `address(this).balance == 0` as an invariant

---

## 8. Proxy & Upgrade

### 8.1 Uninitialized Proxy Implementation
- Implementation contract deployed without calling `_disableInitializers()`
- Anyone can initialize the implementation directly and potentially selfDestruct it
- Fix: call `_disableInitializers()` in implementation constructor

### 8.2 Storage Collision (Transparent/Custom Proxy)
- Proxy and implementation use the same storage slots
- Fix: use EIP-1967 standardized slots; always use OpenZeppelin proxy patterns

### 8.3 Missing Storage Gap
- Upgradeable contract inherits base contract without `uint256[50] __gap`
- Adding storage variables in a future upgrade shifts all derived contract slots
- Fix: add `__gap` to all base upgradeable contracts

### 8.4 Unsafe upgradeTo
- `upgradeTo(address)` callable by non-admin
- New implementation can be malicious (selfDestruct, drain funds)
- Fix: `onlyOwner` or `onlyUpgradeAdmin` on all upgrade functions

### 8.5 Function Clashing in Diamond
- Diamond (EIP-2535) facets with overlapping function selectors
- One facet's function shadows another
- Fix: loupe functions + selector collision check before diamond cut

### 8.6 Constructor Logic in Upgradeable
- Logic in `constructor` runs only for the implementation, not the proxy
- Fix: move all initialization logic to `initialize()` function

---

## 9. ERC Standard Violations

### 9.1 Non-Standard ERC-20 (Missing Return Value)
- Some tokens (USDT, BNB) don't return `bool` from `transfer()`
- `require(token.transfer(...))` reverts on these tokens
- Fix: use OpenZeppelin `SafeERC20`

### 9.2 Fee-on-Transfer Tokens
- Protocol assumes `amountIn == amountReceived` — wrong for rebasing/fee tokens
- Fix: measure balance before and after transfer; use the delta

### 9.3 Rebasing Tokens
- Token balance changes without explicit transfer (Aave aTokens, stETH)
- Internal accounting based on stored amounts becomes stale

### 9.4 ERC-777 Callbacks
- ERC-777 tokens call `tokensReceived` hook before balance update
- Creates reentrancy vector in protocols that treat them as ERC-20
- Fix: use `nonReentrant`; explicitly block ERC-777 in token whitelist if needed

---

## 10. Logic & State Machine Errors

### 10.1 State Machine Violations
- Protocol can skip states or enter invalid state combinations
- Map all valid state transitions; check every transition function

### 10.2 Incorrect Accounting
- Shares/amounts diverge over time due to rounding or deposit/withdrawal ordering
- Especially dangerous in ERC-4626 vaults

### 10.3 Timestamp Dependence
- `block.timestamp` manipulable by miner (±15 seconds on Ethereum)
- Don't use `block.timestamp` for randomness; use with tolerance for time-sensitive logic

### 10.4 Block Number Dependence
- `block.number` not consistent across chains; Arbitrum uses L1 block numbers in some contexts
- Use `block.timestamp` for time-sensitive logic; explicit sequencer considerations for L2

### 10.5 Front-Runnable Deadline
- Deadline checks `require(block.timestamp <= deadline)` with no grace period
- Users can manipulate tx timing to cause deadline failures for victims

---

## 11. Cross-Chain & Bridge

### 11.1 Message Replay Across Chains
- Signed message valid on Ethereum replayed on Arbitrum/Optimism
- Fix: include `block.chainid` in signed data

### 11.2 Bridge Validation
- Bridge contract doesn't validate message source chain or sender
- Attacker sends fake bridge message from a different chain
- Fix: validate `srcChainId` + `trustedRemote` in all bridge message handlers

### 11.3 Sequencer Downtime (L2)
- Arbitrum/Optimism sequencer goes offline; protocol has time-sensitive positions that need updating
- Fix: grace period after sequencer downtime; use sequencer uptime feed

### 11.4 L1 → L2 Message Ordering
- Messages sent from L1 to L2 may arrive in non-deterministic order
- Don't assume L1 state is reflected on L2 instantly

---

## 12. Governance

### 12.1 Proposal Threshold Bypass
- Large token holder (or flash loan) creates and immediately executes malicious proposal
- Fix: minimum voting period; token lock during vote; quorum requirement

### 12.2 Timelock Bypass
- Governance action bypasses timelock via alternative admin function
- All admin functions must go through timelock

### 12.3 Governance Takeover
- Attacker accumulates enough tokens to pass any proposal unilaterally
- Fix: veto mechanism; guardian role with emergency pause
