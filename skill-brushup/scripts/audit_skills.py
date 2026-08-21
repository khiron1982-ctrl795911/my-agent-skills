from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path

DEFAULT_ROOTS = [Path.home() / ".claude" / "skills", Path.home() / ".agents" / "skills", Path.home() / ".codex" / "skills"]
OUTPUT_ROOT = Path.home() / "ai-collaboration" / "reviews" / "codex" / "skill-brushup"
LINK_RE = re.compile(r"\[[^\]]+\]\((?!https?://|mailto:|#)([^)]+)\)")
NAME_RE = re.compile(r"^[a-z0-9-]{1,64}$")


@dataclass
class Finding:
    severity: str
    code: str
    path: str
    message: str


@dataclass
class Skill:
    name: str
    path: Path
    root: Path
    digest: str


def frontmatter(text: str) -> tuple[dict[str, str], str | None]:
    if not text.startswith("---"):
        return {}, "YAML frontmatterがありません"
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, "YAML frontmatterの終端がありません"
    data: dict[str, str] = {}
    current: str | None = None
    for line in parts[1].splitlines():
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if match:
            current = match.group(1)
            data[current] = match.group(2).strip().strip('"\'')
        elif current and line.startswith((" ", "\t")):
            data[current] += " " + line.strip()
    return data, None


def discover(roots: list[Path]) -> tuple[list[Skill], list[Finding]]:
    skills: list[Skill] = []
    findings: list[Finding] = []
    seen_paths: set[Path] = set()
    for root in roots:
        if not root.exists():
            findings.append(Finding("warning", "missing-root", str(root), "監査対象フォルダがありません"))
            continue
        for path in root.rglob("SKILL.md"):
            resolved = path.resolve()
            if resolved in seen_paths:
                continue
            seen_paths.add(resolved)
            text = path.read_text(encoding="utf-8-sig")
            meta, error = frontmatter(text)
            name = meta.get("name", "") if not error else path.parent.name
            if error:
                findings.append(Finding("error", "frontmatter", str(path), error))
            else:
                if not name:
                    findings.append(Finding("error", "missing-name", str(path), "nameがありません"))
                if not meta.get("description"):
                    findings.append(Finding("error", "missing-description", str(path), "descriptionがありません"))
                if name and not NAME_RE.fullmatch(name):
                    findings.append(Finding("error", "invalid-name", str(path), f"nameの形式が不正です: {name}"))
                if name and path.parent.name != name:
                    findings.append(Finding("warning", "folder-name", str(path), f"フォルダ名とnameが異なります: {path.parent.name} / {name}"))
            line_count = text.count("\n") + 1
            if line_count > 500:
                findings.append(Finding("warning", "sprawl", str(path), f"{line_count}行あります。参照ファイルへの分割候補です"))
            prose = re.sub(r"\x60\x60\x60.*?\x60\x60\x60", "", text, flags=re.S)
            for target in LINK_RE.findall(prose):
                clean = target.split("#", 1)[0].strip().strip("<>")
                if clean.lower() in {"link", "url"}:
                    continue
                if clean and not (path.parent / clean).exists():
                    findings.append(Finding("error", "broken-link", str(path), f"相対リンク先がありません: {target}"))
            digest = hashlib.sha256(text.replace("\r\n", "\n").encode("utf-8")).hexdigest()
            skills.append(Skill(name or path.parent.name, path, root, digest))
    return skills, findings


def find_diverged_copies(skills: list[Skill]) -> list[Finding]:
    grouped: dict[str, list[Skill]] = defaultdict(list)
    for skill in skills:
        grouped[skill.name].append(skill)
    findings: list[Finding] = []
    for name, copies in sorted(grouped.items()):
        if len(copies) > 1 and len({item.digest for item in copies}) > 1:
            locations = ", ".join(str(item.path) for item in copies)
            findings.append(Finding("warning", "diverged-copy", name, f"同名スキルの内容が異なります: {locations}"))
    return findings


def render(skills: list[Skill], findings: list[Finding], generated: str) -> str:
    counts = {level: sum(item.severity == level for item in findings) for level in ("error", "warning", "info")}
    lines = [f"# スキル監査レポート {generated}", "", f"- 点検: {len(skills)}ファイル / {len({s.name for s in skills})}種類", f"- error: {counts['error']}", f"- warning: {counts['warning']}", f"- info: {counts['info']}", ""]
    for level in ("error", "warning", "info"):
        selected = [item for item in findings if item.severity == level]
        lines.extend([f"## {level} ({len(selected)})", ""])
        lines.extend(f"- `{item.code}` — {item.message} — `{item.path}`" for item in selected)
        if not selected:
            lines.append("- なし")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Claude Code/Codexの全スキルを監査します")
    parser.add_argument("--root", action="append", type=Path, help="監査ルート。省略時は3領域すべて")
    parser.add_argument("--output", type=Path, default=OUTPUT_ROOT)
    args = parser.parse_args()
    skills, findings = discover(args.root or DEFAULT_ROOTS)
    findings.extend(find_diverged_copies(skills))
    findings.sort(key=lambda item: (item.severity, item.code, item.path))
    generated = datetime.now().astimezone().isoformat(timespec="seconds")
    args.output.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    md_path = args.output / f"audit-{stamp}.md"
    json_path = args.output / f"audit-{stamp}.json"
    md_path.write_text(render(skills, findings, generated), encoding="utf-8")
    payload = {"generated_at": generated, "skills": [{"name": s.name, "path": str(s.path), "root": str(s.root), "sha256": s.digest} for s in skills], "findings": [asdict(f) for f in findings]}
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Audited {len(skills)} files / {len({s.name for s in skills})} skills")
    print(f"Errors: {sum(f.severity == 'error' for f in findings)}")
    print(f"Warnings: {sum(f.severity == 'warning' for f in findings)}")
    print(md_path)
    print(json_path)
    return 1 if any(item.severity == "error" for item in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
