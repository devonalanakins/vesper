"""Generate a deterministic, read-only browser fixture from Vesper's Python core.

Intentionally offline. Run --check in CI to detect stale checked-in reports.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from decimal import Decimal
import json
from pathlib import Path
import sys

from vesper.evidence import SyntheticEvidenceWindow, project_synthetic_evidence
from vesper.performance import ExternalFlow, Valuation

ROOT = Path(__file__).resolve().parents[1]
DESTINATION = ROOT / "web" / "data" / "synthetic-evidence.mjs"
OWNER = "synthetic-owner-never-display"
ACCOUNT = "synthetic-account-never-display"


def at(hour: int) -> datetime:
    return datetime(2026, 11, 4, hour, 0, tzinfo=timezone.utc)


def content() -> str:
    opening = Valuation(OWNER, ACCOUNT, at(13), Decimal("10000"), "synthetic:open")
    pre_deposit = Valuation(OWNER, ACCOUNT, at(15), Decimal("10500"), "synthetic:pre-deposit")
    closing = Valuation(OWNER, ACCOUNT, at(20), Decimal("13650"), "synthetic:close")
    deposit = ExternalFlow("synthetic:deposit", "deposit", Decimal("2500"), pre_deposit)
    window = SyntheticEvidenceWindow(
        owner=OWNER, account=ACCOUNT, source_ref="synthetic:evidence-demo-1",
        captured_at=at(21), opening=opening, closing=closing, flows=(deposit,), complete=True,
    )
    report = project_synthetic_evidence(
        window, expected_owner=OWNER, expected_account=ACCOUNT
    ).public_synthetic_record()
    output = json.dumps(report, indent=2, ensure_ascii=True, sort_keys=True)
    return (
        "// GENERATED. Offline synthetic sample; never edit values manually.\n"
        "// python scripts/generate_synthetic_evidence.py [--check]\n"
        "export const SYNTHETIC_EVIDENCE = Object.freeze(" + output + ");\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Require committed browser fixture to match core math")
    args = parser.parse_args()
    expected = content()
    if args.check:
        if not DESTINATION.exists() or DESTINATION.read_text(encoding="utf-8") != expected:
            print("Synthetic browser evidence is stale; regenerate before review", file=sys.stderr)
            return 1
        print("Synthetic browser fixture matches Python source calculations")
        return 0
    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    DESTINATION.write_text(expected, encoding="utf-8")
    print(f"Wrote {DESTINATION.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
