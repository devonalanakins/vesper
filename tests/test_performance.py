"""Synthetic standalone finance math tests; no external accounts or services."""
from datetime import datetime, timezone
from decimal import Decimal
from unittest import TestCase

from vesper.performance import ContractError, ExternalFlow, Valuation, calculate_period_return


def timestamp(hour):
    return datetime(2026, 11, 4, hour, tzinfo=timezone.utc)


def v(hour, amount, proof, owner="synthetic-owner", account="synthetic-account", complete=True):
    return Valuation(owner, account, timestamp(hour), Decimal(amount), proof, complete)


def external(name, hour, before, amount, kind):
    return ExternalFlow(name, kind, Decimal(amount), v(hour, before, "proof-" + name))


class PerformanceTests(TestCase):
    def calculate(self, opening, closing, *flows):
        return calculate_period_return(opening, closing, flows, stream_complete=True)

    def test_gain_and_loss(self):
        opening = v(9, "100", "open")
        self.assertEqual(self.calculate(opening, v(16, "112", "close")).return_pct, Decimal("12"))
        self.assertEqual(self.calculate(opening, v(16, "95", "close")).return_pct, Decimal("-5"))

    def test_contributions_are_not_profit(self):
        result = self.calculate(v(9, "100", "open"), v(16, "150", "close"),
                                external("d", 12, "100", "50", "deposit"))
        self.assertEqual(result.return_pct, Decimal("0"))
        self.assertEqual(result.net_pnl, Decimal("0"))
        self.assertEqual(result.net_external_flows, Decimal("50"))

    def test_withdrawals_are_not_losses(self):
        result = self.calculate(v(9, "100", "open"), v(16, "70", "close"),
                                external("w", 12, "100", "-30", "withdrawal"))
        self.assertEqual(result.return_pct, Decimal("0"))
        self.assertEqual(result.net_pnl, Decimal("0"))

    def test_links_two_growth_segments(self):
        result = self.calculate(v(9, "100", "open"), v(16, "176", "close"),
                                external("d", 12, "110", "50", "deposit"))
        self.assertEqual(result.return_pct, Decimal("21"))
        self.assertEqual(result.net_pnl, Decimal("26"))

    def test_incomplete_stream_fails_closed(self):
        result = calculate_period_return(v(9, "100", "open"), v(16, "120", "close"))
        self.assertEqual(result.status, "INCOMPLETE_EVIDENCE")
        self.assertIsNone(result.return_pct)
        self.assertIsNone(result.net_pnl)

    def test_incomplete_valuation_fails_closed(self):
        result = self.calculate(v(9, "100", "open", complete=False), v(16, "120", "close"))
        self.assertEqual(result.status, "INCOMPLETE_EVIDENCE")

    def test_zero_capital_is_not_a_return(self):
        self.assertEqual(self.calculate(v(9, "0", "open"), v(16, "90", "close")).status,
                         "UNAVAILABLE_UNFUNDED")
        result = self.calculate(v(9, "100", "open"), v(16, "0", "close"),
                                external("all", 12, "100", "-100", "withdrawal"))
        self.assertIsNone(result.return_pct)

    def test_cross_owner_and_account_rejected(self):
        with self.assertRaises(ContractError):
            self.calculate(v(9, "100", "open"), v(16, "110", "close", owner="other"))
        with self.assertRaises(ContractError):
            self.calculate(v(9, "100", "open"), v(16, "150", "close"),
                           ExternalFlow("d", "deposit", Decimal("50"),
                                        v(12, "100", "proof-d", account="other")))

    def test_duplicate_activities_and_evidence_rejected(self):
        with self.assertRaises(ContractError):
            self.calculate(v(9, "100", "same"), v(16, "110", "same"))
        with self.assertRaises(ContractError):
            self.calculate(v(9, "100", "open"), v(16, "200", "close"),
                           external("d", 11, "100", "50", "deposit"),
                           external("d", 12, "150", "50", "deposit"))

    def test_order_and_flow_sign_rejected(self):
        with self.assertRaises(ContractError):
            self.calculate(v(9, "100", "open"), v(16, "170", "close"),
                           external("a", 13, "100", "30", "deposit"),
                           external("b", 12, "130", "20", "deposit"))
        with self.assertRaises(ContractError):
            self.calculate(v(9, "100", "open"), v(16, "120", "close"),
                           external("c", 12, "100", "-20", "deposit"))

    def test_negative_resulting_equity_rejected(self):
        with self.assertRaises(ContractError):
            self.calculate(v(9, "100", "open"), v(16, "0", "close"),
                           external("w", 12, "10", "-100", "withdrawal"))

    def test_nan_float_and_naive_timestamp_rejected(self):
        with self.assertRaises(ContractError):
            self.calculate(Valuation("x", "y", timestamp(9), 100.0, "open"),
                           v(16, "110", "close", owner="x", account="y"))
        with self.assertRaises(ContractError):
            self.calculate(v(9, "100", "open"),
                           Valuation("synthetic-owner", "synthetic-account",
                                     timestamp(16), Decimal("NaN"), "close"))
        with self.assertRaises(ContractError):
            self.calculate(Valuation("x", "y", datetime(2026, 11, 4, 9),
                                     Decimal("100"), "open"),
                           v(16, "110", "close", owner="x", account="y"))

    def test_stream_complete_must_be_bool(self):
        with self.assertRaises(ContractError):
            calculate_period_return(v(9, "100", "open"), v(16, "110", "close"),
                                    stream_complete="yes")
