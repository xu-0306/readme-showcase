#!/usr/bin/env python3
"""Check the media and links of a README before publishing.

Usage:
    python check_readme_assets.py README.md [--max-mb 8] [--first-screen-lines 40]
    python check_readme_assets.py --self-test

Reports (errors make the exit code 1, warnings do not):
  error    local image / video / link target does not exist
  error    local media file larger than GitHub's hard 100 MB limit
  warning  image without alt text
  warning  local media file larger than --max-mb
  warning  no image within the first --first-screen-lines lines
  warning  repo-relative video file (GitHub shows it as a link, not a player)
  info     remote media (not checked; it can disappear)
"""
from __future__ import annotations

import argparse
import re
import sys
import tempfile
from pathlib import Path
from urllib.parse import unquote

MD_IMAGE = re.compile(r"!\[(?P<alt>[^\]]*)\]\(\s*<?(?P<src>[^)\s>]+)>?(?:\s+[\"'][^)]*)?\)")
MD_LINK = re.compile(r"(?<!!)\[[^\]]*\]\(\s*<?(?P<href>[^)\s>]+)>?(?:\s+[\"'][^)]*)?\)")
HTML_TAG = re.compile(r"<(?P<tag>img|source|video|a)\b(?P<attrs>[^>]*)>", re.IGNORECASE)
ATTR = re.compile(r"""(?P<name>[\w-]+)\s*=\s*(?:"(?P<dq>[^"]*)"|'(?P<sq>[^']*)'|(?P<bare>[^\s>]+))""")
FENCE = re.compile(r"^\s*(```|~~~)")
REMOTE = re.compile(r"^(?:[a-z][a-z0-9+.-]*:|//)", re.IGNORECASE)
VIDEO_EXT = {".mp4", ".webm", ".mov"}
MEDIA_EXT = VIDEO_EXT | {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".avif"}
GITHUB_HARD_LIMIT_MB = 100


def strip_code(text: str) -> list[str]:
    """Blank out fenced code blocks and inline code so examples are not checked."""
    lines, fenced = [], False
    for line in text.splitlines():
        if FENCE.match(line):
            fenced = not fenced
            lines.append("")
        elif fenced:
            lines.append("")
        else:
            lines.append(re.sub(r"`[^`]*`", "", line))
    return lines


def attrs_of(raw: str) -> dict[str, str]:
    found = {}
    for m in ATTR.finditer(raw):
        value = m.group("dq") if m.group("dq") is not None else m.group("sq")
        found[m.group("name").lower()] = value if value is not None else m.group("bare")
    return found


def collect(lines: list[str]):
    """Yield (line_no, kind, target, alt).

    kind is 'media' or 'link'. alt is the alt text for an image ('' when empty,
    None when the tag carries no alt attribute or alt does not apply).
    """
    for no, line in enumerate(lines, 1):
        for m in MD_IMAGE.finditer(line):
            yield no, "media", m.group("src"), m.group("alt")
        for m in MD_LINK.finditer(line):
            yield no, "link", m.group("href"), None
        for m in HTML_TAG.finditer(line):
            tag, attrs = m.group("tag").lower(), attrs_of(m.group("attrs"))
            if tag == "a":
                if "href" in attrs:
                    yield no, "link", attrs["href"], None
                continue
            if "src" in attrs:
                yield no, "media", attrs["src"], attrs.get("alt", "") if tag == "img" else None
            for part in attrs.get("srcset", "").split(","):
                if part.strip():
                    yield no, "media", part.split()[0], None
            if tag == "video" and "poster" in attrs:
                yield no, "media", attrs["poster"], None


def check(readme: Path, max_mb: float = 8.0, first_screen_lines: int = 40) -> list[tuple[str, int, str]]:
    root = readme.parent
    lines = strip_code(readme.read_text(encoding="utf-8", errors="replace"))
    findings: list[tuple[str, int, str]] = []
    first_media_line = None
    sized: set[Path] = set()

    for no, kind, target, alt in collect(lines):
        if kind == "media" and first_media_line is None:
            first_media_line = no
        if kind == "media" and alt is not None and not alt.strip():
            findings.append(("warning", no, f"image without alt text: {target}"))

        if target.startswith("#") or target.lower().startswith("mailto:"):
            continue
        if REMOTE.match(target):
            if kind == "media":
                findings.append(("info", no, f"remote media, not checked: {target}"))
            continue

        rel = unquote(target.split("#", 1)[0].split("?", 1)[0])
        if not rel:
            continue
        path = root / rel.lstrip("/")
        if not path.exists():
            what = "file" if kind == "media" else "link target"
            findings.append(("error", no, f"missing local {what}: {target}"))
            continue
        ext = path.suffix.lower()
        if path.is_file() and ext in MEDIA_EXT and path not in sized:
            sized.add(path)
            mb = path.stat().st_size / (1024 * 1024)
            if mb > GITHUB_HARD_LIMIT_MB:
                findings.append(("error", no, f"{target} is {mb:.1f} MB, over GitHub's {GITHUB_HARD_LIMIT_MB} MB file limit"))
            elif mb > max_mb:
                findings.append(("warning", no, f"{target} is {mb:.1f} MB, over the {max_mb:g} MB budget"))
        if ext in VIDEO_EXT:
            findings.append(("warning", no, f"repo-relative video shows as a link on GitHub, not a player: {target}"))

    if first_media_line is None:
        findings.append(("warning", 1, "README has no image or video at all"))
    elif first_media_line > first_screen_lines:
        findings.append(("warning", first_media_line, f"first image is on line {first_media_line}; nothing visual in the first {first_screen_lines} lines"))

    order = {"error": 0, "warning": 1, "info": 2}
    return sorted(findings, key=lambda f: (order[f[0]], f[1]))


def self_test() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "docs" / "media").mkdir(parents=True)
        (root / "docs" / "media" / "ok.png").write_bytes(b"x" * 10)
        (root / "docs" / "media" / "big demo.gif").write_bytes(b"x" * (2 * 1024 * 1024))
        (root / "docs" / "guide.md").write_text("guide", encoding="utf-8")
        readme = root / "README.md"
        readme.write_text(
            "\n".join(
                [
                    "# Title",
                    '<p align="center"><img src="docs/media/ok.png" alt="Main window" width="800"></p>',
                    "![](docs/media/big%20demo.gif)",
                    "![gone](docs/media/gone.png)",
                    '<img src="docs/media/ok.png">',
                    "[guide](docs/guide.md#top) [dead](docs/nope.md) [web](https://example.com) [anchor](#title)",
                    '<picture><source media="(prefers-color-scheme: dark)" srcset="docs/media/dark.png"></picture>',
                    "```",
                    "![in code](not/checked.png)",
                    "```",
                    "`![inline](also/not/checked.png)`",
                    "![badge](https://img.shields.io/badge/a-b-blue)",
                ]
            ),
            encoding="utf-8",
        )
        got = {(level, no, msg) for level, no, msg in check(readme, max_mb=1)}
        text = "\n".join(sorted(f"{l} {n}: {m}" for l, n, m in got))
        expect = [
            ("error", 4, "missing local file: docs/media/gone.png"),
            ("error", 6, "missing local link target: docs/nope.md"),
            ("error", 7, "missing local file: docs/media/dark.png"),
            ("warning", 3, "image without alt text: docs/media/big%20demo.gif"),
            ("warning", 5, "image without alt text: docs/media/ok.png"),
            ("info", 12, "remote media, not checked: https://img.shields.io/badge/a-b-blue"),
        ]
        for item in expect:
            assert item in got, f"missing {item}\n{text}"
        assert any(l == "warning" and "over the 1 MB budget" in m for l, _, m in got), text
        assert not any("checked.png" in m for _, _, m in got), text
        assert not any("guide.md" in m or "example.com" in m for _, _, m in got), text
        assert not any(n == 2 for _, n, _ in got), text  # the well-formed hero raises nothing

        plain = root / "PLAIN.md"
        plain.write_text("# Title\n\nwords only\n", encoding="utf-8")
        assert ("warning", 1, "README has no image or video at all") in check(plain)

        late = root / "LATE.md"
        late.write_text("# T\n" + "text\n" * 60 + "![shot](docs/media/ok.png)\n", encoding="utf-8")
        assert any("nothing visual in the first" in m for _, _, m in check(late))
    print("self-test passed")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("readme", nargs="?", help="path to the README file")
    parser.add_argument("--max-mb", type=float, default=8.0, help="size budget per media file (default 8)")
    parser.add_argument("--first-screen-lines", type=int, default=40, help="lines counted as the first screen (default 40)")
    parser.add_argument("--self-test", action="store_true", help="run the built-in check and exit")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return 0
    if not args.readme:
        parser.error("give a README path or --self-test")
    readme = Path(args.readme)
    if not readme.is_file():
        print(f"error: not a file: {readme}", file=sys.stderr)
        return 2

    findings = check(readme, args.max_mb, args.first_screen_lines)
    for level, no, msg in findings:
        print(f"{level:7} {readme.name}:{no}: {msg}")
    counts = {lvl: sum(1 for f in findings if f[0] == lvl) for lvl in ("error", "warning", "info")}
    print(f"{counts['error']} error(s), {counts['warning']} warning(s), {counts['info']} info")
    return 1 if counts["error"] else 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
