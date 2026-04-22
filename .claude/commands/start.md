Load `skills/protocol-memory/SKILL.md`.

Start or resume a protocol engagement.

**Argument:** $ARGUMENTS (protocol name or URL, optional)

---

## Step 1 — Identify the Protocol

**If URL:** extract domain as slug base (`mars.poolin.fi` → `mars-poolin`). Fetch to get name; fall back to web search if JS-rendered.
**If name:** use directly, normalize to slug (`"Aave v3"` → `aave-v3`).
**If empty:** ask "Which protocol? Paste a URL or type the name."

---

## Step 2 — Check Existing Memory

**If `memory/protocols/[slug]/` exists:** read `profile.md`, `working-memory.md`, `next-actions.md`. Print: what the protocol is · current phase · last findings or open questions · recommended next action.

**If it does not exist:** create the directory from `memory/templates/`. Ask 5 short questions:
1. What does this protocol do? (one sentence)
2. Which chain(s)?
3. Is the code public? (GitHub URL if yes)
4. Goal — audit, architecture review, strategy, or all?
5. Any deadline or specific concern to prioritize?

Write answers to `memory/protocols/[slug]/profile.md`. Update `memory/index.md`.

---

## Step 3 — Environment Check

```bash
slither --version 2>&1 | head -1 || echo "SLITHER: not installed"
aderyn --version 2>&1 | head -1 || echo "ADERYN: not installed"
forge --version 2>&1 | head -1 || echo "FORGE: not installed"
find . -name "*.sol" -not -path "*/node_modules/*" -not -path "*/lib/*" -not -path "*/test*" | wc -l
```

---

## Step 4 — Confirm and Suggest Next Command

Print startup summary: active protocol · phase · tools ready · local contract count.

Suggest the most logical next step:
- No prior work → `/research [protocol]` (external) or `/product-assessor [protocol]` (local/mixed)
- Audit done, no fixes → `/fix [protocol]`
- Fixes done → `/arch [protocol]`
- Architecture done → `/strategy [protocol]`
- All done → `/diligence [protocol]`
- If smart-wallet claims are in scope → also suggest `/ux-audit` and `/aa-readiness`
