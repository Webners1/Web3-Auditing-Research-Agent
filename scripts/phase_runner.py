#!/usr/bin/env python3
"""
scripts/phase_runner.py — Manager/Worker research orchestrator for Web3 Rabbit Stage 2.

Architecture: this Python script is the Manager. For each research phase it spawns
a completely isolated, stateless Claude Code CLI subprocess (the Worker). The Worker
terminates when the phase completes. The only data that survives between phases is a
strictly typed JSON Phase Handoff — no shared memory, no context bleed.

No Anthropic API keys needed. Uses local Claude Pro subscription via the `claude` CLI.

Usage:
    python scripts/phase_runner.py <slug>
    python scripts/phase_runner.py <slug> --dry-run
    python scripts/phase_runner.py <slug> --resume-from 2

Phases:
    1  Product Assessment   -> Phase1Handoff  (target contracts + suspected vuln)
    2  Smart Contract Audit -> Phase2Handoff  (business risk summary + severity)
    3  Report Assembly      -> writes diligence report + sales handoff to disk

Requirements:
    pip install pydantic   (strongly recommended — falls back to dataclass validation)
    claude CLI must be in PATH
"""

import argparse
import dataclasses
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# ── Paths ─────────────────────────────────────────────────────────────────────

REPO_ROOT    = Path(__file__).parent.parent
DB_PATH      = REPO_ROOT / "web3-sales-agent" / "data" / "rabbit_pipeline.db"
SKILLS_DIR   = REPO_ROOT / "skills"
MEMORY_DIR   = REPO_ROOT / "memory" / "protocols"
AUDIT_DIR    = REPO_ROOT / "audit-output"
HANDOFFS_DIR = REPO_ROOT / "web3-sales-agent" / "data" / "research-handoffs"

CLAUDE_MODEL  = "claude-sonnet-4-6"
PHASE_TIMEOUT = 600  # 10 minutes per phase; override with --timeout

# ── Pydantic / dataclass validation layer ─────────────────────────────────────
# Pydantic gives richer validation errors and coercion. Falls back to dataclasses
# with __post_init__ checks when pydantic is not installed.

try:
    from pydantic import BaseModel, field_validator
    _USE_PYDANTIC = True

    class Phase1Handoff(BaseModel):
        slug: str
        protocol_name: str
        primary_chain: str
        contract_addresses: list[str]
        suspected_vulnerability: str
        product_summary: str

        @field_validator("contract_addresses")
        @classmethod
        def at_least_one(cls, v: list[str]) -> list[str]:
            if not v:
                raise ValueError("contract_addresses must not be empty")
            return v

        @field_validator("suspected_vulnerability", "product_summary", "slug", "protocol_name")
        @classmethod
        def not_blank(cls, v: str) -> str:
            if not v.strip():
                raise ValueError("field must not be blank")
            return v.strip()

    class Phase2Handoff(BaseModel):
        slug: str
        business_risk_summary: str
        findings_saved: bool
        severity: str

        @field_validator("severity")
        @classmethod
        def valid_severity(cls, v: str) -> str:
            allowed = {"CRITICAL", "HIGH", "MEDIUM", "LOW", "NONE"}
            if v.upper() not in allowed:
                raise ValueError(f"severity must be one of {allowed}, got {v!r}")
            return v.upper()

        @field_validator("business_risk_summary")
        @classmethod
        def not_blank(cls, v: str) -> str:
            if not v.strip():
                raise ValueError("business_risk_summary must not be blank")
            return v.strip()

except ImportError:
    _USE_PYDANTIC = False

    @dataclasses.dataclass
    class Phase1Handoff:  # type: ignore[no-redef]
        slug: str
        protocol_name: str
        primary_chain: str
        contract_addresses: list
        suspected_vulnerability: str
        product_summary: str

        def __post_init__(self) -> None:
            required = ["slug", "protocol_name", "primary_chain",
                        "suspected_vulnerability", "product_summary"]
            for f in required:
                if not str(getattr(self, f, "")).strip():
                    raise ValueError(f"Phase1Handoff.{f} must not be blank")
            if not self.contract_addresses:
                raise ValueError("Phase1Handoff.contract_addresses must not be empty")

    @dataclasses.dataclass
    class Phase2Handoff:  # type: ignore[no-redef]
        slug: str
        business_risk_summary: str
        findings_saved: bool
        severity: str

        def __post_init__(self) -> None:
            if not self.business_risk_summary.strip():
                raise ValueError("Phase2Handoff.business_risk_summary must not be blank")
            allowed = {"CRITICAL", "HIGH", "MEDIUM", "LOW", "NONE"}
            if self.severity.upper() not in allowed:
                raise ValueError(f"Phase2Handoff.severity must be one of {allowed}")
            self.severity = self.severity.upper()


def _build_handoff(cls, data: dict):
    """Construct a handoff model from a dict, works for both pydantic and dataclass."""
    if _USE_PYDANTIC:
        return cls(**data)
    # dataclass: manually map, ignore extra fields
    fields = {f.name for f in dataclasses.fields(cls)}
    missing = fields - set(data.keys())
    if missing:
        raise ValueError(f"{cls.__name__} missing required fields: {sorted(missing)}")
    return cls(**{k: data[k] for k in fields})


# ── DB helpers ─────────────────────────────────────────────────────────────────

def get_lead(slug: str) -> Optional[dict]:
    if not DB_PATH.exists():
        return None
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    row = conn.execute(
        "SELECT * FROM leads WHERE slug = ? LIMIT 1", (slug,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def mark_researched(slug: str) -> None:
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute(
        "UPDATE leads SET status = 'researched', updated_at = datetime('now') WHERE slug = ?",
        (slug,),
    )
    conn.commit()
    conn.close()


# ── Skill loader ───────────────────────────────────────────────────────────────

def load_skill(skill_name: str) -> str:
    path = SKILLS_DIR / skill_name / "SKILL.md"
    if path.exists():
        return path.read_text(encoding="utf-8")
    return f"[SKILL {skill_name} not found — apply general Web3 security knowledge]"


# ── JSON extractor (bulletproof) ──────────────────────────────────────────────

def extract_json(text: str) -> dict:
    """
    Extract a JSON object from LLM output regardless of wrapping noise.

    Attempts four strategies in order:
      1. Direct json.loads (clean output)
      2. ```json ... ``` fenced block
      3. Any ``` ... ``` fenced block
      4. Outermost { ... } brace extraction
    """
    if not text or not text.strip():
        raise ValueError("Response text is empty")

    text = text.strip()

    # Strategy 1: direct parse
    try:
        result = json.loads(text)
        if isinstance(result, dict):
            return result
    except json.JSONDecodeError:
        pass

    # Strategy 2: ```json block
    m = re.search(r"```json\s*([\s\S]*?)\s*```", text, re.IGNORECASE)
    if m:
        try:
            result = json.loads(m.group(1).strip())
            if isinstance(result, dict):
                return result
        except json.JSONDecodeError:
            pass

    # Strategy 3: any fenced block
    m = re.search(r"```\s*([\s\S]*?)\s*```", text)
    if m:
        try:
            result = json.loads(m.group(1).strip())
            if isinstance(result, dict):
                return result
        except json.JSONDecodeError:
            pass

    # Strategy 4: outermost braces (handles preamble/postamble)
    brace_start = text.find("{")
    brace_end   = text.rfind("}")
    if brace_start != -1 and brace_end > brace_start:
        candidate = text[brace_start : brace_end + 1]
        try:
            result = json.loads(candidate)
            if isinstance(result, dict):
                return result
        except json.JSONDecodeError:
            pass

    raise ValueError(
        f"Could not extract a JSON object from the response.\n"
        f"First 400 chars of output:\n{text[:400]!r}"
    )


# ── Claude CLI subprocess runner ───────────────────────────────────────────────

def _find_claude_cmd() -> list[str]:
    """Return the correct command list to invoke the Claude Code CLI."""
    # shutil.which handles PATH lookup including .cmd/.exe on Windows
    claude_exec = shutil.which("claude")
    if claude_exec:
        # npm-installed on Windows produces claude.cmd — must be invoked through cmd.exe
        if sys.platform == "win32" and claude_exec.lower().endswith(".cmd"):
            return ["cmd", "/c", claude_exec]
        return [claude_exec]
    # Fallback: let subprocess try directly (may fail with FileNotFoundError)
    return ["claude"]


def run_claude_worker(
    prompt: str,
    phase_label: str,
    timeout: int = PHASE_TIMEOUT,
) -> str:
    """
    Spawn an isolated, stateless Claude Code CLI subprocess.

    The prompt is passed via stdin to avoid Windows command-line length limits.
    `--output-format json` is requested for reliable response parsing.
    `--dangerously-skip-permissions` enables headless MCP tool use (no interactive prompts).

    Returns the response text. Raises RuntimeError on failure or timeout.
    """
    base_cmd = _find_claude_cmd()
    cmd = base_cmd + [
        "--print",
        "--output-format", "json",
        "--model", CLAUDE_MODEL,
        "--dangerously-skip-permissions",
    ]

    try:
        result = subprocess.run(
            cmd,
            input=prompt,              # prompt delivered via stdin — no shell arg length limit
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            env=os.environ.copy(),     # inherit parent env: picks up .mcp.json, API creds, PATH
            cwd=str(REPO_ROOT),        # run from repo root so .mcp.json is found
        )
    except subprocess.TimeoutExpired:
        raise RuntimeError(
            f"Phase '{phase_label}' timed out after {timeout}s.\n"
            f"Increase timeout with --timeout or retry with --resume-from."
        )
    except FileNotFoundError:
        raise RuntimeError(
            "claude CLI not found in PATH.\n"
            "Install Claude Code: https://claude.ai/code\n"
            "Then ensure `claude --version` works in this terminal."
        )

    if result.returncode != 0:
        stderr_summary = (result.stderr or "").strip()[:600]
        stdout_summary = (result.stdout or "").strip()[:300]
        raise RuntimeError(
            f"Phase '{phase_label}' subprocess exited {result.returncode}.\n"
            f"STDERR: {stderr_summary or '(empty)'}\n"
            f"STDOUT: {stdout_summary or '(empty)'}"
        )

    raw = (result.stdout or "").strip()
    if not raw:
        stderr_hint = (result.stderr or "").strip()[:300]
        raise RuntimeError(
            f"Phase '{phase_label}' produced empty stdout.\n"
            f"STDERR hint: {stderr_hint or '(empty)'}"
        )

    # Unwrap --output-format json envelope: {"type":"result","result":"...","is_error":false}
    try:
        envelope = json.loads(raw)
        if isinstance(envelope, dict):
            if envelope.get("is_error"):
                raise RuntimeError(
                    f"Phase '{phase_label}' reported an error:\n{str(envelope.get('result',''))[:400]}"
                )
            if "result" in envelope:
                return str(envelope["result"])
    except json.JSONDecodeError:
        pass  # not an envelope — return raw text

    return raw


# ── Phase prompts ─────────────────────────────────────────────────────────────

def _lead_block(lead: dict) -> str:
    return (
        f"- Name   : {lead['name']}\n"
        f"- Slug   : {lead['slug']}\n"
        f"- URL    : {lead['url']}\n"
        f"- Chain  : {lead.get('chain', 'Unknown')}\n"
        f"- TVL    : {lead.get('tvl', '---')}\n"
        f"- Type   : {lead.get('lead_type', 'TVL Sweet Spot')}\n"
        f"- Signal : {lead.get('signal_score', 'MEDIUM')}\n"
        f"- Evidence: {lead.get('evidence', '')}"
    )


def build_phase1_prompt(lead: dict) -> str:
    skill = load_skill("product-assessor")
    return f"""\
You are the Product Assessment agent in a Web3 research pipeline (Phase 1 of 3).

## Target Protocol
{_lead_block(lead)}

## Instructions
{skill}

## Required Output
After completing research, output ONLY a ```json block containing this exact structure.
No text after the closing ```.

```json
{{
  "slug": "{lead['slug']}",
  "protocol_name": "<official name>",
  "primary_chain": "<primary deployment chain>",
  "contract_addresses": ["<0x...>"],
  "suspected_vulnerability": "<one sentence: the most likely security issue given the protocol type>",
  "product_summary": "<2-3 sentences: what the protocol does and its current operational state>"
}}
```
"""


def build_phase2_prompt(h1: "Phase1Handoff") -> str:
    skill = load_skill("web3-audit")
    contracts_block = "\n".join(f"  - {addr}" for addr in h1.contract_addresses)
    return f"""\
You are the Smart Contract Audit agent in a Web3 research pipeline (Phase 2 of 3).

## Context (from Phase 1)
- Protocol  : {h1.protocol_name}
- Slug      : {h1.slug}
- Chain     : {h1.primary_chain}
- Product   : {h1.product_summary}
- Primary suspicion: {h1.suspected_vulnerability}

## Contracts to Audit
{contracts_block}

## Instructions
{skill}

After completing the audit:
1. Save your structured findings to the Vector DB using the MCP tools available to you.
2. Distill the most critical finding into a single business-language sentence.

## Required Output
Output ONLY a ```json block. No technical jargon (no reentrancy, calldata, Solidity) in the summary.

```json
{{
  "slug": "{h1.slug}",
  "business_risk_summary": "<one sentence in plain business language: what goes wrong, who loses money>",
  "findings_saved": true,
  "severity": "<CRITICAL|HIGH|MEDIUM|LOW|NONE>"
}}
```
"""


def build_phase3_prompt(h1: "Phase1Handoff", h2: "Phase2Handoff") -> str:
    skill = load_skill("client-reporting")
    date        = datetime.now().strftime("%Y%m%d")
    report_path = AUDIT_DIR / f"{h1.slug}-diligence-{date}.md"
    handoff_path = HANDOFFS_DIR / f"{h1.slug}.md"

    return f"""\
You are the Report Assembly agent in a Web3 research pipeline (Phase 3 of 3).

## Research Summary
- Protocol : {h1.protocol_name}  ({h1.slug})
- Chain    : {h1.primary_chain}
- Product  : {h1.product_summary}
- Suspected issue : {h1.suspected_vulnerability}
- Business risk   : {h2.business_risk_summary}
- Severity        : {h2.severity}

## Instructions
{skill}

Using the above summary AND any findings stored in the Vector DB (query slug={h1.slug}),
write two files to disk:

### File 1 — Diligence Report
Path: {report_path}
Write a complete Three-Pillar diligence report (Security / Protocol Health / Market Position).

### File 2 — Sales Handoff
Path: {handoff_path}
Write ONLY the following block — no extra text:

**Protocol:** {h1.protocol_name}
**Slug:** {h1.slug}
**Chain:** {h1.primary_chain}
**Recommended Service:** <service type + price range>
**Primary Pain:** <one sentence: what is structurally wrong>
**Pitch Hook:** <one sentence: why now, why this team>
**Proof Points To Use:** <1-2 findings in business language — no CVE names, no Solidity terms>
**Cautions:** <conversion risk, team signals, wind-down indicators>

After writing both files, output the single line:
PHASE 3 COMPLETE
"""


# ── Handoff persistence (disk cache for --resume-from) ────────────────────────

def _save_handoff(slug: str, phase: int, data: dict) -> Path:
    path = MEMORY_DIR / slug / f"phase{phase}_handoff.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return path


def _load_handoff(slug: str, phase: int) -> dict:
    path = MEMORY_DIR / slug / f"phase{phase}_handoff.json"
    if not path.exists():
        raise FileNotFoundError(
            f"--resume-from {phase + 1} requires {path}.\n"
            f"Run phase {phase} first or start from --resume-from 1."
        )
    return json.loads(path.read_text(encoding="utf-8"))


# ── Main orchestrator ─────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Manager/Worker research orchestrator — Web3 Rabbit Stage 2",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python scripts/phase_runner.py mycelium-perpetual-pools\n"
            "  python scripts/phase_runner.py mycelium-perpetual-pools --dry-run\n"
            "  python scripts/phase_runner.py mycelium-perpetual-pools --resume-from 2\n"
        ),
    )
    parser.add_argument("slug", help="Protocol slug from the DB")
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print prompt lengths; write placeholder files; skip subprocess calls",
    )
    parser.add_argument(
        "--resume-from", type=int, default=1, metavar="N",
        help="Skip phases before N (1=Phase1, 2=Phase2, 3=Phase3)",
    )
    parser.add_argument(
        "--timeout", type=int, default=PHASE_TIMEOUT, metavar="SECS",
        help=f"Per-phase subprocess timeout in seconds (default: {PHASE_TIMEOUT})",
    )
    args = parser.parse_args()

    slug = args.slug
    lead = get_lead(slug)
    if not lead:
        sys.exit(
            f"ERROR: No lead found for slug '{slug}'.\n"
            f"       Run /web3-rabbit scan to populate leads first."
        )

    # ── Header ────────────────────────────────────────────────────────────────
    print("\nWeb3 Rabbit -- Phase Runner")
    print("-" * 50)
    print(f"Protocol : {lead['name']} ({slug})")
    print(f"Chain    : {lead.get('chain', 'Unknown')}  |  TVL: {lead.get('tvl', '---')}")
    print(f"Model    : {CLAUDE_MODEL}")
    print(f"Timeout  : {args.timeout}s per phase")
    print(f"Pydantic : {'yes' if _USE_PYDANTIC else 'no (fallback validation)'}")
    if args.dry_run:
        print("Mode     : DRY RUN -- no subprocesses will be spawned")
    print("-" * 50 + "\n")

    # Ensure output dirs exist
    for d in [AUDIT_DIR, HANDOFFS_DIR, MEMORY_DIR / slug]:
        d.mkdir(parents=True, exist_ok=True)

    h1: Optional["Phase1Handoff"] = None
    h2: Optional["Phase2Handoff"] = None

    # ── Phase 1: Product Assessment ───────────────────────────────────────────
    print("[Phase 1] Product Assessment")
    if args.resume_from <= 1:
        prompt = build_phase1_prompt(lead)
        print(f"  Prompt  : {len(prompt):,} chars  |  Spawning worker...", end="", flush=True)

        if args.dry_run:
            print("  (skipped -- dry-run)")
            raw = json.dumps({
                "slug": slug,
                "protocol_name": lead["name"],
                "primary_chain": lead.get("chain", "Unknown"),
                "contract_addresses": ["0xDRY_RUN"],
                "suspected_vulnerability": "dry-run placeholder",
                "product_summary": "dry-run placeholder",
            })
        else:
            raw = run_claude_worker(prompt, "Product Assessment", args.timeout)
            print()  # newline after inline status

        try:
            h1_data = extract_json(raw)
            h1 = _build_handoff(Phase1Handoff, h1_data)
        except (ValueError, TypeError) as exc:
            print(f"\n  PARSE ERROR: {exc}", file=sys.stderr)
            print(f"  Raw output (first 500): {raw[:500]!r}", file=sys.stderr)
            print(f"  Fix the Phase 1 prompt or retry. Exiting.", file=sys.stderr)
            sys.exit(1)

        saved = _save_handoff(slug, 1, h1_data)
        print(f"  Contracts: {len(h1.contract_addresses)}  |  Suspicion: {h1.suspected_vulnerability[:80]}")
        print(f"  Handoff  : {saved.relative_to(REPO_ROOT)}\n")

    else:
        print("  Skipped (--resume-from)")
        try:
            h1 = _build_handoff(Phase1Handoff, _load_handoff(slug, 1))
        except (FileNotFoundError, ValueError) as exc:
            sys.exit(f"  ERROR: {exc}")
        print(f"  Loaded from phase1_handoff.json\n")

    # ── Phase 2: Smart Contract Audit ─────────────────────────────────────────
    print("[Phase 2] Smart Contract Audit")
    if args.resume_from <= 2:
        prompt = build_phase2_prompt(h1)
        print(f"  Prompt  : {len(prompt):,} chars  |  Spawning worker...", end="", flush=True)

        if args.dry_run:
            print("  (skipped -- dry-run)")
            raw = json.dumps({
                "slug": slug,
                "business_risk_summary": "dry-run: liquidity pool exposed under specific conditions",
                "findings_saved": True,
                "severity": "MEDIUM",
            })
        else:
            raw = run_claude_worker(prompt, "Smart Contract Audit", args.timeout)
            print()

        try:
            h2_data = extract_json(raw)
            h2 = _build_handoff(Phase2Handoff, h2_data)
        except (ValueError, TypeError) as exc:
            print(f"\n  PARSE ERROR: {exc}", file=sys.stderr)
            print(f"  Raw output (first 500): {raw[:500]!r}", file=sys.stderr)
            sys.exit(1)

        saved = _save_handoff(slug, 2, h2_data)
        print(f"  Severity : {h2.severity}  |  Risk: {h2.business_risk_summary[:80]}")
        print(f"  Handoff  : {saved.relative_to(REPO_ROOT)}\n")

    else:
        print("  Skipped (--resume-from)")
        try:
            h2 = _build_handoff(Phase2Handoff, _load_handoff(slug, 2))
        except (FileNotFoundError, ValueError) as exc:
            sys.exit(f"  ERROR: {exc}")
        print(f"  Loaded from phase2_handoff.json\n")

    # ── Phase 3: Report Assembly ───────────────────────────────────────────────
    print("[Phase 3] Report Assembly")
    if args.resume_from <= 3:
        prompt = build_phase3_prompt(h1, h2)
        date  = datetime.now().strftime("%Y%m%d")
        print(f"  Prompt  : {len(prompt):,} chars  |  Spawning worker...", end="", flush=True)

        if args.dry_run:
            print("  (skipped -- dry-run)")
            (AUDIT_DIR / f"{slug}-diligence-{date}.md").write_text(
                f"[dry-run diligence report for {slug}]\n", encoding="utf-8"
            )
            (HANDOFFS_DIR / f"{slug}.md").write_text(
                f"[dry-run handoff for {slug}]\n", encoding="utf-8"
            )
        else:
            run_claude_worker(prompt, "Report Assembly", args.timeout)
            print()

        # Verify files were written
        report_path  = AUDIT_DIR / f"{slug}-diligence-{date}.md"
        handoff_path = HANDOFFS_DIR / f"{slug}.md"
        for path, label in [(report_path, "Report"), (handoff_path, "Handoff")]:
            if path.exists():
                print(f"  {label:8}: {path.relative_to(REPO_ROOT)}")
            else:
                print(f"  {label:8}: NOT FOUND -- Phase 3 may have failed to write {path.name}",
                      file=sys.stderr)

    else:
        print("  Skipped (--resume-from)\n")

    # ── Finalize ───────────────────────────────────────────────────────────────
    if not args.dry_run:
        mark_researched(slug)
        print(f"\nDone. '{slug}' marked 'researched' in DB.")
    else:
        print(f"\n[dry-run] Would mark '{slug}' as 'researched' in DB.")

    print(f"\nNext: /web3-rabbit pitch {slug}")


if __name__ == "__main__":
    main()
