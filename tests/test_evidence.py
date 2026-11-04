"""Synthetic-only contract and privacy regression tests."""
from dataclasses import replace
from datetime import datetime, timezone
from decimal import Decimal
import json
import unittest

from vesper.evidence import (
    ContractError, ReadProjection, ScopeMismatch, SyntheticEvidenceWindow,
    project_synthetic_evidence,
)
from vesper.performance import ExternalFlow, Valuation


OWNER = "private-owner-must-not-display"
ACCOUNT = "private-account-must-not-display"
EVIDENCE = "private-evidence-must-not-display"


def time(hour: int) -> datetime:
    return datetime(2026, 11, 4, hour, tzinfo=timezone.utc)


def fixture(*, complete=True, owner=OWNER, account=ACCOUNT) -> SyntheticEvidenceWindow:
    opening = Valuation(owner, account, time(13), Decimal("10000"), EVIDENCE + ":open")
    before = Valuation(owner, account, time(15), Decimal("10500"), EVIDENCE + ":flow")
    closing = Valuation(owner, account, time(20), Decimal("13650"), EVIDENCE + ":close")
    flow = ExternalFlow("private-activity-must-not-display", "deposit", Decimal("2500"), before)
    return SyntheticEvidenceWindow(owner, account, "synthetic:fixture-001", time(21),
                                   opening, closing, (flow,), complete)


def project(window: SyntheticEvidenceWindow) -> ReadProjection:
    return project_synthetic_evidence(window, expected_owner=OWNER, expected_account=ACCOUNT)


class ProjectionTests(unittest.TestCase):
    def test_contribution_adjusted_result(self):
        result = project(fixture())
        self.assertEqual(result.status, "CALCULATED")
        self.assertEqual(result.return_pct, Decimal("10.2500"))
        self.assertEqual(result.net_pnl, Decimal("1150"))
        self.assertEqual(result.external_flows, Decimal("2500"))

    def test_public_record_does_not_expose_identifiers(self):
        record = project(fixture()).public_synthetic_record()
        serialized = json.dumps(record, sort_keys=True)
        for secret in [OWNER, ACCOUNT, EVIDENCE, "private-activity", "fixture-001"]:
            self.assertNotIn(secret, serialized)
        self.assertFalse(record["actions_enabled"])
        self.assertEqual(record["source"], "synthetic")
        self.assertEqual(record["return_pct"], "10.2500")

    def test_incomplete_source_never_displays_money_or_returns(self):
        record = project(fixture(complete=False)).public_synthetic_record()
        self.assertEqual(record["status"], "INCOMPLETE_EVIDENCE")
        for key in ("return_pct", "net_pnl", "external_flows"):
            self.assertIsNone(record[key])

    def test_incomplete_closing_valuation_unavailable(self):
        window = fixture()
        record = project(replace(window, closing=replace(window.closing, complete=False))).public_synthetic_record()
        self.assertEqual(record["status"], "INCOMPLETE_EVIDENCE")
        self.assertIsNone(record["return_pct"])

    def test_scope_mismatch_fails_without_disclosing_scope(self):
        for changed in [replace(fixture(), owner="other"),
                        replace(fixture(), account="other")]:
            with self.assertRaises(ScopeMismatch) as ctx:
                project(changed)
            self.assertNotIn(ACCOUNT, str(ctx.exception))
        with self.assertRaises(ScopeMismatch):
            project_synthetic_evidence(fixture(), expected_owner="other", expected_account=ACCOUNT)

    def test_inner_cross_account_flow_rejected(self):
        window = fixture()
        corrupted = replace(window.flows[0], before=replace(window.flows[0].before, account="other"))
        with self.assertRaises(ScopeMismatch):
            project(replace(window, flows=(corrupted,)))

    def test_bad_source_markers_rejected(self):
        for marker in ("broker:live", "synthetic:", "", None):
            with self.assertRaises(ContractError):
                project(replace(fixture(), source_ref=marker))

    def test_source_time_cannot_precede_close(self):
        with self.assertRaises(ContractError):
            project(replace(fixture(), captured_at=time(19)))
        with self.assertRaises(ContractError):
            project(replace(fixture(), captured_at=datetime(2026, 11, 4, 21)))

    def test_immutable_events_and_boolean_completeness_required(self):
        with self.assertRaises(ContractError):
            project(replace(fixture(), flows=list(fixture().flows)))
        with self.assertRaises(ContractError):
            project(replace(fixture(), complete="yes"))

    def test_public_serializer_rejects_incoherent_metrics(self):
        result = project(fixture())
        with self.assertRaises(ContractError):
            replace(result, net_pnl=None).public_synthetic_record()
        with self.assertRaises(ContractError):
            replace(result, source_kind="broker").public_synthetic_record()
        with self.assertRaises(ContractError):
            replace(result, status="UNKNOWN").public_synthetic_record()
        with self.assertRaises(ContractError):
            replace(result, return_pct=Decimal("NaN")).public_synthetic_record()
        with self.assertRaises(ContractError):
            replace(result, net_pnl=Decimal("Infinity")).public_synthetic_record()
        with self.assertRaises(ContractError):
            replace(result, captured_at=time(19)).public_synthetic_record()

    def test_deterministic_output_and_utc(self):
        a = project(fixture()).public_synthetic_record()
        b = project(fixture()).public_synthetic_record()
        self.assertEqual(a, b)
        self.assertTrue(a["captured_at"].endswith("+00:00"))

    def test_unfunded_returns_unavailable(self):
        window = fixture()
        unfinanced = replace(window, opening=replace(window.opening, equity=Decimal("0")))
        result = project(unfinanced).public_synthetic_record()
        self.assertEqual(result["status"], "UNAVAILABLE_UNFUNDED")
        self.assertIsNone(result["net_pnl"])


if __name__ == "__main__":
    unittest.main()
