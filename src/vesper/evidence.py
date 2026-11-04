"""Pure, synthetic-only evidence projection for the public research terminal.

No identity authentication, broker access or personal finance data is implemented.
The caller-supplied scope check is a data consistency guard, NOT authorization.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal

from .performance import ContractError, ExternalFlow, Valuation, calculate_period_return


class ScopeMismatch(ContractError):
    """An evidence request crosses the provided owner/account boundary."""


@dataclass(frozen=True, slots=True)
class SyntheticEvidenceWindow:
    owner: str
    account: str
    source_ref: str
    captured_at: datetime
    opening: Valuation
    closing: Valuation
    flows: tuple[ExternalFlow, ...] = ()
    complete: bool = False


@dataclass(frozen=True, slots=True)
class ReadProjection:
    status: str
    source_kind: str
    period_start: datetime
    period_end: datetime
    captured_at: datetime
    return_pct: Decimal | None
    net_pnl: Decimal | None
    external_flows: Decimal | None

    def public_synthetic_record(self) -> dict[str, object]:
        """A deliberate allowlist: no account, owner or evidence identifiers.

        This output is only suitable for a prominently labelled synthetic demo.
        """
        if self.source_kind != "synthetic":
            raise ContractError("public research terminal accepts synthetic sources only")
        if self.status not in {"CALCULATED", "INCOMPLETE_EVIDENCE", "UNAVAILABLE_UNFUNDED"}:
            raise ContractError("unexpected projection status")
        calculated = self.status == "CALCULATED"
        if calculated != all(v is not None for v in (self.return_pct, self.net_pnl, self.external_flows)):
            raise ContractError("projection status and metrics disagree")
        if calculated and any(
            not isinstance(value, Decimal) or not value.is_finite()
            for value in (self.return_pct, self.net_pnl, self.external_flows)
        ):
            raise ContractError("calculated metrics must be finite Decimals")
        start = _stamp(self.period_start, "period start")
        end = _stamp(self.period_end, "period end")
        captured = _stamp(self.captured_at, "capture timestamp")
        if not start < end <= captured:
            raise ContractError("projection chronology is invalid")
        return {
            "source": "synthetic",
            "label": "SYNTHETIC / NOT LIVE",
            "status": self.status,
            "period_start": self.period_start.astimezone(timezone.utc).isoformat(),
            "period_end": self.period_end.astimezone(timezone.utc).isoformat(),
            "captured_at": self.captured_at.astimezone(timezone.utc).isoformat(),
            "return_pct": str(self.return_pct) if calculated else None,
            "net_pnl": str(self.net_pnl) if calculated else None,
            "external_flows": str(self.external_flows) if calculated else None,
            "actions_enabled": False,
        }


def _stamp(value: object, label: str) -> datetime:
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise ContractError(f"{label} must be timezone-aware")
    return value


def project_synthetic_evidence(
    window: SyntheticEvidenceWindow,
    *,
    expected_owner: str,
    expected_account: str,
) -> ReadProjection:
    """Validate a single synthetic data window and present only complete results.

    expected_owner/account must come from an independent trusted authority in
    any future private application. Matching strings alone are NOT authentication.
    """
    if not isinstance(window, SyntheticEvidenceWindow):
        raise ContractError("expected SyntheticEvidenceWindow")
    if not all(isinstance(s, str) and s.strip() for s in (
        window.owner, window.account, expected_owner, expected_account
    )):
        raise ContractError("scope fields must be nonempty strings")
    if (window.owner, window.account) != (expected_owner, expected_account):
        raise ScopeMismatch("projection scope does not match")
    if not isinstance(window.source_ref, str) or not window.source_ref.startswith("synthetic:"):
        raise ContractError("synthetic source marker required")
    if len(window.source_ref) <= len("synthetic:"):
        raise ContractError("synthetic source marker must identify a fixture")
    if type(window.complete) is not bool:
        raise ContractError("completeness must be boolean")
    if not isinstance(window.flows, tuple):
        raise ContractError("flows must be an immutable tuple")
    captured = _stamp(window.captured_at, "capture timestamp")
    if not isinstance(window.closing, Valuation):
        raise ContractError("closing valuation required")
    closing_at = _stamp(window.closing.at, "closing timestamp")
    if captured < closing_at:
        raise ContractError("capture cannot precede closing observation")
    if not isinstance(window.opening, Valuation):
        raise ContractError("opening valuation required")
    if (window.opening.owner, window.opening.account) != (window.owner, window.account):
        raise ScopeMismatch("projection scope does not match")
    if (window.closing.owner, window.closing.account) != (window.owner, window.account):
        raise ScopeMismatch("projection scope does not match")
    for flow in window.flows:
        if not isinstance(flow, ExternalFlow):
            raise ContractError("expected explicit external flow")
        if not isinstance(flow.before, Valuation):
            raise ContractError("flow requires valuation")
        if (flow.before.owner, flow.before.account) != (window.owner, window.account):
            raise ScopeMismatch("projection scope does not match")

    calculated = calculate_period_return(
        window.opening, window.closing, window.flows, stream_complete=window.complete
    )
    available = calculated.status == "CALCULATED"
    return ReadProjection(
        status=calculated.status,
        source_kind="synthetic",
        period_start=window.opening.at,
        period_end=window.closing.at,
        captured_at=captured,
        return_pct=calculated.return_pct if available else None,
        net_pnl=calculated.net_pnl if available else None,
        external_flows=calculated.net_external_flows if available else None,
    )
