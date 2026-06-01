from __future__ import annotations

import json
import py_compile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


REQUIRED_FILES = [
    "app.py",
    "requirements.txt",
    "run_playbook.bat",
    "README.md",
    ".gitignore",

    "core/__init__.py",
    "core/models.py",
    "core/clock_math.py",
    "core/waveform_engine.py",
    "core/soc_path_engine.py",
    "core/timing_engine.py",
    "core/recommendation_engine.py",
    "core/validation_cases.py",

    "ui/__init__.py",
    "ui/styles.py",
    "ui/cards.py",
    "ui/plots.py",
    "ui/sidebar.py",
    "ui/tabs.py",

    "docs/01_pll_to_flipflop_roadmap.md",
    "docs/02_clock_slew_load_delay.md",
    "docs/03_skew_jitter_uncertainty.md",
    "docs/04_setup_hold_margin.md",
    "docs/05_clock_power_emir_awareness.md",
    "docs/demo_script.md",

    "examples/ai_soc_5ghz_baseline.json",
]


PYTHON_FILES = [
    "app.py",

    "core/models.py",
    "core/clock_math.py",
    "core/waveform_engine.py",
    "core/soc_path_engine.py",
    "core/timing_engine.py",
    "core/recommendation_engine.py",
    "core/validation_cases.py",

    "ui/styles.py",
    "ui/cards.py",
    "ui/plots.py",
    "ui/sidebar.py",
    "ui/tabs.py",
]


def check_required_files() -> list[str]:
    errors: list[str] = []

    for relative_path in REQUIRED_FILES:
        file_path = ROOT / relative_path

        if not file_path.exists():
            errors.append(f"Missing required file: {relative_path}")

    return errors


def check_python_compile() -> list[str]:
    errors: list[str] = []

    for relative_path in PYTHON_FILES:
        file_path = ROOT / relative_path

        if not file_path.exists():
            errors.append(f"Cannot compile missing file: {relative_path}")
            continue

        try:
            py_compile.compile(str(file_path), doraise=True)
        except Exception as exc:
            errors.append(f"Python compile failed: {relative_path} -> {exc}")

    return errors


def check_json_files() -> list[str]:
    errors: list[str] = []

    json_file = ROOT / "examples" / "ai_soc_5ghz_baseline.json"

    if not json_file.exists():
        errors.append("Missing JSON example: examples/ai_soc_5ghz_baseline.json")
        return errors

    try:
        with json_file.open("r", encoding="utf-8") as file:
            json.load(file)
    except Exception as exc:
        errors.append(f"JSON validation failed: {json_file} -> {exc}")

    return errors


def check_markdown_nonempty() -> list[str]:
    errors: list[str] = []

    md_files = [
        ROOT / "README.md",
        ROOT / "docs" / "01_pll_to_flipflop_roadmap.md",
        ROOT / "docs" / "02_clock_slew_load_delay.md",
        ROOT / "docs" / "03_skew_jitter_uncertainty.md",
        ROOT / "docs" / "04_setup_hold_margin.md",
        ROOT / "docs" / "05_clock_power_emir_awareness.md",
        ROOT / "docs" / "demo_script.md",
    ]

    for file_path in md_files:
        if not file_path.exists():
            errors.append(f"Missing markdown file: {file_path.relative_to(ROOT)}")
            continue

        text = file_path.read_text(encoding="utf-8").strip()

        if len(text) < 200:
            errors.append(
                f"Markdown file looks too short or empty: {file_path.relative_to(ROOT)}"
            )

    return errors


def main() -> None:
    print("=" * 72)
    print("Interactive SoC Clock Distribution Playbook — Final Project Audit")
    print("=" * 72)

    checks = [
        ("Required files", check_required_files),
        ("Python compilation", check_python_compile),
        ("JSON validation", check_json_files),
        ("Markdown content", check_markdown_nonempty),
    ]

    all_errors: list[str] = []

    for check_name, check_fn in checks:
        print(f"\n[CHECK] {check_name}")
        errors = check_fn()

        if errors:
            print("Status: FAIL")
            for error in errors:
                print(f"  - {error}")
            all_errors.extend(errors)
        else:
            print("Status: PASS")

    print("\n" + "=" * 72)

    if all_errors:
        print(f"FINAL STATUS: FAIL — {len(all_errors)} issue(s) found.")
        raise SystemExit(1)

    print("FINAL STATUS: PASS — Project structure, Python files, JSON, and docs are ready.")
    print("=" * 72)


if __name__ == "__main__":
    main()