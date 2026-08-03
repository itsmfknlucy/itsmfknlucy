from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_SUFFIXES = {".md", ".py", ".yml", ".yaml", ".json", ".svg", ".txt"}
IGNORED_PARTS = {"__pycache__", ".git"}


class PrivacyContractTests(unittest.TestCase):
    def test_tracked_text_contains_no_source_identity_or_contact_details(self) -> None:
        forbidden = (
            "Natha" + "nael",
            "La" + "bios",
            "joshua" + "labios",
            "njm" + "labios",
            "2x2" + " Picture",
        )
        violations: list[str] = []
        for path in ROOT.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in PUBLIC_SUFFIXES:
                continue
            if any(part in IGNORED_PARTS for part in path.parts):
                continue
            if path == Path(__file__).resolve():
                continue
            text = path.read_text(encoding="utf-8")
            lowered = text.casefold()
            for value in forbidden:
                if value.casefold() in lowered:
                    violations.append(f"{path.relative_to(ROOT)} contains a source identity fragment")
        self.assertEqual([], violations)

    def test_tracked_text_contains_no_github_access_token(self) -> None:
        patterns = (
            re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
            re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
        )
        violations: list[str] = []
        for path in ROOT.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in PUBLIC_SUFFIXES:
                continue
            if any(part in IGNORED_PARTS for part in path.parts):
                continue
            text = path.read_text(encoding="utf-8")
            if any(pattern.search(text) for pattern in patterns):
                violations.append(str(path.relative_to(ROOT)))
        self.assertEqual([], violations)


if __name__ == "__main__":
    unittest.main()
