Load `skills/web3-audit/SKILL.md`.

Runs a full smart contract security audit on the contracts in the current working directory or a named protocol.

**Argument:** $ARGUMENTS (optional — protocol name or path)

---

## Routing

**If $ARGUMENTS is empty or a local path:**
Run the audit on local contracts. The skill handles discovery, Slither, Aderyn, and 8-agent analysis automatically.

**If $ARGUMENTS is a URL (starts with `http`):**
Derive slug from domain. Load memory. Use contracts discovered via `/research` or fetch from Etherscan/GitHub.

**If $ARGUMENTS is a protocol name (e.g., `Aave v3`):**
First load memory: `skills/protocol-memory/SKILL.md`.
Then proceed — the web3-audit skill will use any contracts already in memory or cloned.

---

## What Runs

The full web3-audit pipeline:
1. Enumerate in-scope `.sol` files
2. Run Slither + Aderyn static analysis concurrently
3. Spawn 8 parallel specialized agents:
   - Reentrancy agent
   - Access control agent
   - Math precision agent
   - Economic security agent
   - Storage layout agent
   - Invariant agent
   - Periphery and callbacks agent
   - Upgrade and proxy agent
4. Validate all findings through the 4-gate framework
5. Write full audit report to `audit-output/[project]-audit-[YYYYMMDD].md`
6. Include protocol-intelligence sections (health, gaps, feature opportunities, business risks, UX friction, smart-wallet/AA readiness)

---

## After the Audit

- For fix planning: `/fix`
- For deeper major-finding remediation design: `/expand-security-audit`
- For architecture improvements: `/arch`
- For a client-ready PDF: `/report security`

---

## Usage Examples

```
/audit
/audit https://fuji.finance/
/audit https://mars.poolin.fi/
/audit Aave v3
/audit src/contracts/
```
