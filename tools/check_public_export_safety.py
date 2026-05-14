"""Recursive safety checker for the public portfolio export."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

FORBIDDEN_EXTENSIONS = {
    ".lib",
    ".scs",
    ".mdl",
    ".raw",
    ".log",
    ".h5",
    ".hdf5",
    ".sp",
    ".net",
    ".asc",
    ".plt",
    ".tmp",
    ".pyc",
}

FORBIDDEN_TEXT = [
    "C:" + r"\SiliconDesignAutomation",
    "Syn" + "opsys",
    "H" + "BM",
    "D" + "DR",
    "H" + "BM4",
    "conf" + "idential",
    "pro" + "prietary client",
    "internal " + "company",
]

RESTRICTED_LICENSE_WORD = "pro" + "prietary"

RESTRICTED_LICENSE_WORD_ALLOWED = {
    Path("LICENSE"),
    Path("README.md"),
}

TEXT_EXTENSIONS = {
    "",
    ".bat",
    ".json",
    ".md",
    ".py",
    ".txt",
    ".yml",
    ".yaml",
}


def is_text_file(path: Path) -> bool:
    return path.suffix.lower() in TEXT_EXTENSIONS


def read_text(path: Path) -> str | None:
    for encoding in ("utf-8", "utf-8-sig", "cp1252"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return None


def scan() -> list[str]:
    issues: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue

        rel = path.relative_to(ROOT)
        suffix = path.suffix.lower()
        if suffix in FORBIDDEN_EXTENSIONS:
            issues.append(f"{rel}: forbidden extension {suffix}")

        if not is_text_file(path):
            continue

        text = read_text(path)
        if text is None:
            continue
        lower_text = text.lower()

        for term in FORBIDDEN_TEXT:
            if term.lower() in lower_text:
                issues.append(f"{rel}: forbidden text '{term}'")

        if RESTRICTED_LICENSE_WORD in lower_text and rel not in RESTRICTED_LICENSE_WORD_ALLOWED:
            issues.append(f"{rel}: restricted license word is only allowed in LICENSE and README.md")

    return issues


def main() -> int:
    issues = scan()
    if issues:
        print("PUBLIC EXPORT SAFETY: FAIL")
        for issue in issues:
            print(f"- {issue}")
        return 1
    print("PUBLIC EXPORT SAFETY: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
