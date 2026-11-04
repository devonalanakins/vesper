"""Evidence-aware, owner-scoped time-weighted performance. Pure math; no I/O."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Iterable


class ContractError(ValueError):
    """Required financial evidence or contract was invalid."""


@dataclass(frozen=True, slots=True)
class Valuation:
    owner: str
    account: str
    at: datetime
    equity: Decimal
    evidence: str
    complete: bool = True


@dataclass(frozen=True, slots=True)
class ExternalFlow:
    activity_id: str
    kind: str
    amount: Decimal
    before: Valuation
    complete: bool = True


@dataclass(frozen=True, slots=True)
class PerformanceResult:
    status: str
    return_pct: Decimal | None
    net_pnl: Decimal | None
    net_external_flows: Decimal
    method: str = "linked_time_weighted"


def _text(value: object, name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ContractError(f"{name} must be nonempty text")


def _decimal(value: object, name: str) -> Decimal:
    if not isinstance(value, Decimal) or not value.is_finite():
        raise ContractError(f"{name} must be a finite Decimal")
    return value


def _valuation(value: Valuation) -> None:
    if not isinstance(value, Valuation):
        raise ContractError("expected Valuation")
    _text(value.owner, "owner")
    _text(value.account, "account")
    _text(value.evidence, "evidence")
    if not isinstance(value.at, datetime) or value.at.tzinfo is None or value.at.utcoffset() is None:
        raise ContractError("timestamp must include timezone")
    if _decimal(value.equity, "equity") < 0:
        raise ContractError("negative equity is invalid")
    if type(value.complete) is not bool:
        raise ContractError("completeness must be boolean")


def calculate_period_return(
    opening: Valuation,
    closing: Valuation,
    flows: Iterable[ExternalFlow] = (),
    *,
    stream_complete: bool = False,
) -> PerformanceResult:
    """Link funded subperiod returns, subtracting explicitly classified external flows.

    Caller asserts full coverage of broker valuations and activities. This pure
    function cannot independently confirm source completeness or authenticity.
    """
    _valuation(opening)
    _valuation(closing)
    if (opening.owner, opening.account) != (closing.owner, closing.account):
        raise ContractError("opening and closing cross owner/account boundary")
    if opening.at >= closing.at:
        raise ContractError("closing valuation must follow opening")
    if opening.evidence == closing.evidence:
        raise ContractError("valuation evidence must be distinct")
    if type(stream_complete) is not bool:
        raise ContractError("stream completeness must be boolean")

    scope = (opening.owner, opening.account)
    evidence = {opening.evidence, closing.evidence}
    activity_ids: set[str] = set()
    previous_at = opening.at
    capital = opening.equity
    growth = Decimal("1")
    net_flows = Decimal("0")
    complete = stream_complete and opening.complete and closing.complete
    funded = capital > 0

    for flow in flows:
        if not isinstance(flow, ExternalFlow):
            raise ContractError("flow requires ExternalFlow contract")
        _text(flow.activity_id, "activity id")
        if flow.activity_id in activity_ids:
            raise ContractError("duplicate activity")
        activity_ids.add(flow.activity_id)
        if flow.kind not in ("deposit", "withdrawal"):
            raise ContractError("unclassified external flow")
        amount = _decimal(flow.amount, "flow amount")
        if (flow.kind == "deposit" and amount <= 0) or (
            flow.kind == "withdrawal" and amount >= 0
        ):
            raise ContractError("flow sign contradicts kind")
        _valuation(flow.before)
        if (flow.before.owner, flow.before.account) != scope:
            raise ContractError("flow crosses owner/account boundary")
        if flow.before.evidence in evidence:
            raise ContractError("duplicate valuation evidence")
        evidence.add(flow.before.evidence)
        if not previous_at < flow.before.at < closing.at:
            raise ContractError("flows must be ordered within the valuation window")
        previous_at = flow.before.at
        if type(flow.complete) is not bool:
            raise ContractError("flow completeness must be boolean")
        complete = complete and flow.complete and flow.before.complete
        net_flows += amount

        if capital > 0:
            growth *= flow.before.equity / capital
        else:
            funded = False
        capital = flow.before.equity + amount
        if capital < 0:
            raise ContractError("flow produces negative account equity")
        if capital == 0 or flow.before.equity == 0:
            funded = False

    if not complete:
        return PerformanceResult("INCOMPLETE_EVIDENCE", None, None, net_flows)
    if not funded or capital <= 0:
        return PerformanceResult("UNAVAILABLE_UNFUNDED", None, None, net_flows)
    growth *= closing.equity / capital
    return PerformanceResult(
        "CALCULATED",
        (growth - Decimal("1")) * Decimal("100"),
        closing.equity - opening.equity - net_flows,
        net_flows,
    )
