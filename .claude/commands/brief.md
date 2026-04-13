Load `skills/protocol-memory/SKILL.md`.

Gives a concise status summary for a protocol: what we know, where we are, what is open, and what to do next. Use at the start of any session to get back into context fast.

**Argument:** $ARGUMENTS (protocol name)

---

## What It Outputs

```
Protocol: [name]
Phase:    [discovery / audit / remediation / architecture / strategy / complete]
Stage:    [idea / build / testnet / mainnet / mature]

Key facts:
- [3-5 bullet points from profile.md and working-memory.md]

Open findings:
- [from findings.md, CRITICAL and HIGH only]

Open questions:
- [from open-questions.md]

Next actions:
- [from next-actions.md]

Suggested command: /[command]
```

---

## Usage Examples

```
/brief Uniswap v4
/brief Morpho Blue
/brief this protocol
```
