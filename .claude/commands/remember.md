Load `skills/protocol-memory/SKILL.md`.

Saves a fact, decision, constraint, idea, or finding to protocol memory so it persists across sessions.

**Argument:** $ARGUMENTS — `[protocol]: [thing to remember]`

Examples:
- `Morpho Blue: the team wants to avoid any cross-chain messaging for now`
- `Uniswap v4: hooks are the primary integration surface — focus audit there`
- `this protocol: admin key is a 3-of-5 Gnosis Safe on mainnet`
- `Aave v3: client confirmed they are planning a UUPS upgrade in Q3`

---

## What It Does

1. Identifies the protocol from $ARGUMENTS (before the colon)
2. Classifies the note: fact / decision / constraint / finding / question
3. Writes it to the correct memory file:
   - Facts and constraints → `working-memory.md`
   - Decisions and rejected options → `decisions.md`
   - Findings or security notes → `findings.md`
   - Open unknowns → `open-questions.md`
   - Next tasks → `next-actions.md`
4. Updates `memory/index.md`
5. Confirms: "Saved to [protocol] memory under [file]."
