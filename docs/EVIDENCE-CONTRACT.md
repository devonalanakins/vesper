# Vesper evidence projection contract (V01)

**Implemented:** An offline synthetic-only, deterministic projection into a public example terminal.

**Not implemented:** Data ingestion, authenticated identities, tenant isolation at a server, broker or bank reconciliation, asset prices, production telemetry, trading decisions, or order/transfer authorization.

## Typed input and validation

\`SyntheticEvidenceWindow\` supplies: an owner/account context, a synthetic fixture marker, a timezone-aware capture timestamp, start/end \`Valuation\` evidence, an immutable sequence of signed and explicitly typed \`ExternalFlow\` records, and a Boolean completeness assertion. The pure projection rejects mismatched owner/account metadata, invalid source markers, invalid timestamps, malformed event types and evidence inconsistencies.

The scope comparison **does not authenticate a caller**. The two expected strings are inputs supplied by a caller; any future private service must first authenticate the request, resolve its permitted account scopes server-side, verify provider provenance and enforce row-level read permissions before calling a projection. Never accept a client-selected owner ID as an authorization decision.

\`calculate_period_return\` is the existing pure math layer from PR #2, not an external API. It requires authoritative pre-flow equity valuations to compute linked subperiod returns and excludes explicitly classified owner deposits/withdrawals. Partial evidence or zero capital results in an unavailable percentage; missing values are never treated as observed 0% returns.

\`stream_complete=True\` is only a declaration by an authorized future ingestion boundary. It is not evidence of complete provider pagination, market data, valuation freshness or account custody.

## Public output allowlist

Only the following fields can leave \`ReadProjection.public_synthetic_record()\`:

| Field | Meaning |
| --- | --- |
| source | Constant \`synthetic\`, never provider identity |
| label | \`SYNTHETIC / NOT LIVE\` |
| status | \`CALCULATED\`, \`INCOMPLETE_EVIDENCE\`, or \`UNAVAILABLE_UNFUNDED\` |
| period_start / period_end / captured_at | Timezone-aware UTC timestamps |
| return_pct | Stringified Decimal or \`null\` |
| net_pnl / external_flows | Stringified Decimal or \`null\` |
| actions_enabled | Constant \`false\` |

No account, owner, trade identifier, activity ID, evidence reference, token or provider credential can be emitted by this allowlist. When the result is not \`CALCULATED\`, **all three numeric output fields are null**. Malformed or contradictory status/metric combinations fail closed.

The JavaScript terminal independently checks the source/label/action markers, known statuses, numeric completeness and safe formatting. Any mismatch renders a no-numbers \`Unavailable\` state instead of treating data as a return.

## Offline provenance and reproducibility

\`scripts/generate_synthetic_evidence.py\` constructs one deterministic hypothetical timeline:

- Opening equity 10,000 units
- Pre-deposit equity 10,500 units
- External deposit +2,500 units
- Closing equity 13,650 units

Time-weighted return is \`(10,500 / 10,000) * (13,650 / 13,000) - 1 = 10.25%\`. Illustration only. Net P&L is 1,150 units; external contributions are accounted for separately. This sample is **not a real financial result or forecast**. Its fixed November 4, 2026 timestamps are fixture metadata, not an actual observation.

The generator converts the approved Python output allowlist to a checked-in ES module. CI checks that the browser record is identical to a fresh calculation. This avoids hand-maintained duplicate math while requiring no Python server for the static web demonstration. Browser display rendering does not imply the Python logic executes in the browser.

## Safety and acceptance checks

- Unit tests for income/deposits, loss, cash-flow adjustment, incomplete valuations, unfunded periods, scope mismatch, malformed data, duplicate activities, chronology and unsafe status.
- Deterministic generator \`--check\` and Node tests for synthetic-only card rendering, negative returns and fail-closed display.
- Restricted CI with no secrets or finance access.
- Accessible, responsive browser inspection remains an independent required quality gate; source-only CI does not prove it.

Future real-data support requires a new server-side auth/data contract, full audit and consented provider read-only credentials, privacy review and separately approved deployment. Do not "extend" the public demo by inserting real account JSON or provider access tokens into its source.
