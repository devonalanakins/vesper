# Vesper architecture — controlled rebuild

**Identity locked:** A new standalone financial research and capital-intelligence platform, independent of the Rhen programming language, Merit and Anevum creative studio.

## Ownership and flow

    [SYNTHETIC READ-ONLY TERMINAL]
                  |
       [VALIDATED VIEW CONTRACTS]
                  |
       [EVIDENCE / PERFORMANCE CORE]   <-- implemented offline slice
                  |
        [OWNER-SCOPED VALUATIONS]
                  |
      [future authorized read-only adapters]
                  |
              [DATA SOURCES]

Future research, experiment registry, deterministic simulation, risk policy, and capital-allocation capabilities must be modular and testable without connectivity. Future financial action gateways (broker execution, transfers, funding) must be separate, explicitly authorized and independently audited. **No action gateway exists here.**

## Financial math

src/vesper/performance.py implements linked time-weighted returns with mandatory owner/account scopes, exact Decimal amounts, timezone-aware valuations, pre-flow valuation evidence, explicitly classified signed deposits and withdrawals, and unique evidence/activity identifiers. Cross-owner data, negative equity, invalid signs, duplicate observations and chronology errors are rejected.

The caller must explicitly assert stream_complete=True after independently establishing provider pagination and valuation provenance. This switch is **not** proof of source completeness; the pure function does no external validation. Missing completeness or zero funded periods produce unavailable results, never guessed exact percentages. Net contributions are excluded from return, and net P&L is separately reported.

TPD is a daily account performance concept, not a promised yield or guarantee. It can be negative, and any +0.1% daily goal is an unvalidated research hypothesis rather than a demonstrated result.

## Release gates

- **A — Offline foundations:** deterministic, adversarial unit tests, review and source controls. IN PROGRESS.
- **B — Read-only account data:** provider authorization, tenancy checks, full evidence provenance, no state-changing permissions. NOT STARTED.
- **C — Private owner UI:** authenticated server-side owner scope, responsive and a11y checks, privacy, threat model. NOT STARTED.
- **D — Reproducible simulator:** leakage prevention, costs, benchmarks, realistic fills and out-of-sample tests. NOT STARTED.
- **E — Orders/treasury:** separate human approval, fail-closed live boundaries, independent risk/security review, idempotency, kill switch, recovery. NOT AUTHORIZED.

Existing Rhen finance PRs and DevonStation Finance PRs remain unchanged. See docs/LEGACY-HANDOFF.md. No production integration is implied by a design or passing build.
