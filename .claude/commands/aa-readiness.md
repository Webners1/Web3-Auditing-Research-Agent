Load `skills/product-assessor/SKILL.md`.

Runs smart wallet and account-abstraction readiness assessment for a protocol. Use when the team claims gasless onboarding, smart wallets, or ERC-4337 support.

**Argument:** $ARGUMENTS (protocol name or URL)

---

## What Runs

1. Identify wallet model used in product and contracts (EOA, multisig, smart account)
2. Check for ERC-4337 implementation evidence (entrypoint/paymaster/bundler handling)
3. Validate paymaster sponsorship constraints and failure handling behavior
4. Review session-key controls (scope, spend limits, expiry, revocation)
5. Verify EIP-1271 compatibility where contract signatures are relevant
6. If installed, use `account-abstraction` skill references for sharp-edge checks
7. Emit readiness verdict: `Ready` / `Partial` / `Not Ready`

---

## Output Guidance

- Separate marketing claims from deployed behavior
- Report operational dependencies and fallback paths
- Flag missing nonce/replay protections and broad delegated permissions

---

## Usage Examples

```
/aa-readiness
/aa-readiness mars-poolin
/aa-readiness https://mars.poolin.fi/
```
