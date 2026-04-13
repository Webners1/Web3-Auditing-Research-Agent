Load `skills/protocol-memory/SKILL.md`.
Load `skills/protocol-memory/references/memory-schema.md`.

The user is starting a new protocol engagement or resuming an existing one.

**Argument:** $ARGUMENTS (protocol name, optional)

---

## Step 1 — Identify the Protocol

**If $ARGUMENTS starts with `http`:** treat it as a URL.
- Extract the domain as the slug base: `mars.poolin.fi` → `mars-poolin`, `fuji.finance` → `fuji-finance`
- Fetch the URL to get the protocol name and description
- If JS-rendered with no content, search: `"[domain] protocol DeFi"`

**If $ARGUMENTS is a name:** use it directly.
**If $ARGUMENTS is empty:** ask "Which protocol are you working on? You can paste a URL or type the name."

Normalize to a slug. Examples: `"Aave v3"` → `aave-v3`, `"https://fuji.finance/"` → `fuji-finance`.

---

## Step 2 — Check Existing Memory

Check if `memory/protocols/[slug]/` already exists.

**If it exists:**
- Read `profile.md`, `working-memory.md`, `next-actions.md`
- Print a brief status:
  - What the protocol is
  - Current phase (discovery / audit / remediation / architecture / strategy)
  - Last known findings or open questions
  - Recommended next action

**If it does not exist:**
- Create `memory/protocols/[slug]/` with blank files from `memory/templates/`
- Ask 5 short questions to bootstrap the profile:
  1. What does this protocol do? (one sentence)
  2. Which chain(s) is it on?
  3. Is the code public? (GitHub URL if yes)
  4. What are you trying to achieve — audit, architecture review, strategy, or all of the above?
  5. Is there a deadline or specific concern to prioritize?
- Write answers into `memory/protocols/[slug]/profile.md`
- Update `memory/index.md`

---

## Step 3 — Environment Check

Run concurrently:
```bash
slither --version 2>&1 | head -1 || echo "SLITHER: not installed"
aderyn --version 2>&1 | head -1 || echo "ADERYN: not installed"
forge --version 2>&1 | head -1 || echo "FORGE: not installed"
```

If local contracts exist:
```bash
find . -name "*.sol" -not -path "*/node_modules/*" -not -path "*/lib/*" -not -path "*/test*" | wc -l
```

---

## Step 4 — Confirm and Suggest Next Command

Print a clear startup summary:
- Active protocol: [name]
- Phase: [current phase]
- Tools ready: [list]
- Contracts in scope: [count if local]

Then suggest the most logical next command based on the phase:
- No prior work → suggest `/research [protocol]` for external, or `/product-assessor [protocol]` when mixed-surface product review is needed
- Audit done, no fixes → suggest `/fix [protocol]`
- Fixes done → suggest `/arch [protocol]`
- Architecture done → suggest `/strategy [protocol]`
- All done → suggest `/diligence [protocol]` for the executive package

If the protocol claim includes gasless onboarding or smart wallets, also suggest:
- `/ux-audit [protocol or url]`
- `/aa-readiness [protocol]`
