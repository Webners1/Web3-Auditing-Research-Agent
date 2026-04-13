from __future__ import annotations

import argparse
import html
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path


CSS = """
@page {
  size: A4;
  margin: 18mm 16mm 18mm 16mm;
}
body {
  font-family: Georgia, 'Times New Roman', serif;
  color: #18212b;
  margin: 0 auto;
  max-width: 920px;
  line-height: 1.55;
  background: #ffffff;
}
.report-shell {
  padding: 18px 10px 36px 10px;
}
.report-meta {
  margin-bottom: 24px;
  color: #5a6776;
  font-size: 0.92rem;
}
h1, h2, h3, h4, h5, h6 {
  color: #10263f;
  margin-top: 1.4em;
  margin-bottom: 0.45em;
  line-height: 1.2;
}
h1 {
  font-size: 2.0rem;
  padding-bottom: 0.25em;
  border-bottom: 2px solid #d8e1eb;
}
h2 {
  font-size: 1.38rem;
  border-bottom: 1px solid #e5ebf2;
  padding-bottom: 0.2em;
}
h3 {
  font-size: 1.12rem;
}
p {
  margin: 0.55em 0;
}
ul, ol {
  margin: 0.5em 0 0.8em 1.35em;
}
li {
  margin: 0.2em 0;
}
blockquote {
  border-left: 4px solid #7a8ea3;
  margin: 0.9em 0;
  padding: 0.4em 0.9em;
  color: #394857;
  background: #f7f9fc;
}
code {
  font-family: Consolas, 'Courier New', monospace;
  background: #f4f6f8;
  padding: 0.1em 0.3em;
  border-radius: 4px;
  font-size: 0.95em;
}
pre {
  background: #0f1720;
  color: #f8fafc;
  padding: 14px;
  border-radius: 8px;
  overflow-x: auto;
  line-height: 1.45;
}
pre code {
  background: transparent;
  padding: 0;
  color: inherit;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin: 0.9em 0 1.1em 0;
  font-size: 0.95rem;
}
th, td {
  border: 1px solid #d8e1eb;
  padding: 8px 10px;
  text-align: left;
  vertical-align: top;
}
th {
  background: #eef4fa;
  color: #12263a;
}
hr {
  border: 0;
  border-top: 1px solid #d8e1eb;
  margin: 1.2em 0;
}
a {
  color: #0c62b5;
  text-decoration: none;
}
.footer {
  margin-top: 28px;
  color: #6a7683;
  font-size: 0.86rem;
}
"""


BROWSER_CANDIDATES = {
    "chrome": [
        Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
        Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
    ],
    "edge": [
        Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
        Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
    ],
}


def inline_format(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<a href="\2">\1</a>', escaped)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", escaped)
    return escaped


def is_table_separator(line: str) -> bool:
    trimmed = line.strip()
    if "|" not in trimmed:
        return False
    pieces = [piece.strip() for piece in trimmed.strip("|").split("|")]
    return bool(pieces) and all(re.fullmatch(r":?-{3,}:?", piece) for piece in pieces)


def parse_table(lines: list[str]) -> str:
    rows = []
    for line in lines:
        if not line.strip():
            continue
        rows.append([inline_format(cell.strip()) for cell in line.strip().strip("|").split("|")])
    if len(rows) < 2:
        return "<p>" + inline_format(" ".join(lines).strip()) + "</p>"
    header = rows[0]
    body = [row for idx, row in enumerate(rows[1:], start=1) if idx != 1 or not is_table_separator(lines[1])]
    thead = "".join(f"<th>{cell}</th>" for cell in header)
    tbody = []
    for row in body:
        tbody.append("<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>")
    return "<table><thead><tr>" + thead + "</tr></thead><tbody>" + "".join(tbody) + "</tbody></table>"


def markdown_to_html(markdown: str) -> tuple[str, str]:
    lines = markdown.splitlines()
    parts: list[str] = []
    title = ""
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        if stripped.startswith("```"):
            lang = stripped[3:].strip()
            i += 1
            block = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                block.append(lines[i])
                i += 1
            code = html.escape("\n".join(block))
            lang_attr = f' data-lang="{html.escape(lang)}"' if lang else ""
            parts.append(f"<pre><code{lang_attr}>{code}</code></pre>")
            i += 1
            continue

        heading = re.match(r"^(#{1,6})\s+(.*)$", line)
        if heading:
            level = len(heading.group(1))
            text = inline_format(heading.group(2).strip())
            plain = re.sub(r"<[^>]+>", "", text)
            if level == 1 and not title:
                title = plain
            parts.append(f"<h{level}>{text}</h{level}>")
            i += 1
            continue

        if stripped in {"---", "***"}:
            parts.append("<hr>")
            i += 1
            continue

        if stripped.startswith(">"):
            block = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                block.append(lines[i].strip()[1:].strip())
                i += 1
            content = "<br>".join(inline_format(item) for item in block)
            parts.append(f"<blockquote>{content}</blockquote>")
            continue

        if i + 1 < len(lines) and "|" in line and is_table_separator(lines[i + 1]):
            block = [line, lines[i + 1]]
            i += 2
            while i < len(lines) and "|" in lines[i]:
                block.append(lines[i])
                i += 1
            parts.append(parse_table(block))
            continue

        if re.match(r"^\s*[-*]\s+", line):
            items = []
            while i < len(lines) and re.match(r"^\s*[-*]\s+", lines[i]):
                items.append(re.sub(r"^\s*[-*]\s+", "", lines[i]).strip())
                i += 1
            parts.append("<ul>" + "".join(f"<li>{inline_format(item)}</li>" for item in items) + "</ul>")
            continue

        if re.match(r"^\s*\d+\.\s+", line):
            items = []
            while i < len(lines) and re.match(r"^\s*\d+\.\s+", lines[i]):
                items.append(re.sub(r"^\s*\d+\.\s+", "", lines[i]).strip())
                i += 1
            parts.append("<ol>" + "".join(f"<li>{inline_format(item)}</li>" for item in items) + "</ol>")
            continue

        block = [line.strip()]
        i += 1
        while i < len(lines):
            next_line = lines[i]
            next_stripped = next_line.strip()
            if not next_stripped:
                break
            if next_stripped.startswith(("```", ">", "#")):
                break
            if next_stripped in {"---", "***"}:
                break
            if re.match(r"^\s*[-*]\s+", next_line) or re.match(r"^\s*\d+\.\s+", next_line):
                break
            if "|" in next_line and i + 1 < len(lines) and is_table_separator(lines[i + 1]):
                break
            block.append(next_line.strip())
            i += 1
        parts.append("<p>" + inline_format(" ".join(block)) + "</p>")

    if not title:
        title = "Client Report"

    document = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>{CSS}</style>
</head>
<body>
  <div class="report-shell">
    <div class="report-meta">Generated {datetime.now().strftime("%Y-%m-%d %H:%M")}</div>
    {''.join(parts)}
    <div class="footer">Generated by Web3 Auditing Agent report renderer.</div>
  </div>
</body>
</html>
"""
    return title, document


def choose_browser(preference: str) -> Path | None:
    if preference != "auto":
        for candidate in BROWSER_CANDIDATES[preference]:
            if candidate.exists():
                return candidate
        return None
    for browser in ("chrome", "edge"):
        selected = choose_browser(browser)
        if selected:
            return selected
    return None


def export_pdf(browser: Path, html_path: Path, pdf_path: Path) -> None:
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    uri = html_path.resolve().as_uri()
    attempts = [
        [
            str(browser),
            "--headless=new",
            "--disable-gpu",
            "--no-first-run",
            "--allow-file-access-from-files",
            "--print-to-pdf-no-header",
            f"--print-to-pdf={pdf_path.resolve()}",
            uri,
        ],
        [
            str(browser),
            "--headless",
            "--disable-gpu",
            "--no-first-run",
            "--allow-file-access-from-files",
            "--print-to-pdf-no-header",
            f"--print-to-pdf={pdf_path.resolve()}",
            uri,
        ],
    ]

    last_error = None
    for command in attempts:
        try:
            completed = subprocess.run(command, check=True, capture_output=True, text=True)
            if pdf_path.exists():
                return
            last_error = RuntimeError(completed.stderr or completed.stdout or "PDF export did not create a file.")
        except Exception as exc:
            last_error = exc
    raise RuntimeError(f"PDF export failed: {last_error}")


def build_outputs(input_path: Path, html_output: Path, pdf_output: Path | None, browser_pref: str) -> None:
    markdown = input_path.read_text(encoding="utf-8")
    _, rendered = markdown_to_html(markdown)
    html_output.parent.mkdir(parents=True, exist_ok=True)
    html_output.write_text(rendered, encoding="utf-8")

    if pdf_output is None:
        return

    browser = choose_browser(browser_pref)
    if browser is None:
        raise RuntimeError("No supported browser found for PDF export. Install Chrome or Edge, or use --html-only.")
    export_pdf(browser, html_output, pdf_output)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a Markdown report to HTML and PDF.")
    parser.add_argument("input", help="Path to the Markdown report.")
    parser.add_argument("--html-output", help="Optional HTML output path.")
    parser.add_argument("--pdf-output", help="Optional PDF output path.")
    parser.add_argument("--browser", choices=["auto", "chrome", "edge"], default="auto")
    parser.add_argument("--html-only", action="store_true", help="Only write HTML, skip PDF export.")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Input file not found: {input_path}", file=sys.stderr)
        return 2

    html_output = Path(args.html_output) if args.html_output else input_path.with_suffix(".html")
    pdf_output = None if args.html_only else Path(args.pdf_output) if args.pdf_output else input_path.with_suffix(".pdf")

    try:
        build_outputs(input_path, html_output, pdf_output, args.browser)
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(f"HTML: {html_output}")
    if pdf_output is not None:
        print(f"PDF: {pdf_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
