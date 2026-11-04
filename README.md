<p align="center"><img src="web/assets/vesper-mark.svg" width="120" alt="Vesper orbital mark"></p>
<h1 align="center">VESPER</h1>
<p align="center"><strong>Quantitative intelligence. Evidenced decisions.</strong></p>
<p align="center">Research · Simulation · Portfolio · Risk · Evidence</p>

---

Vesper is an independent, clean-slate financial intelligence platform. **It is not a renamed bot, brokerage, live trading system, or investment product.** It separates reproducible research, simulated decisions, account performance, risk and future authorized integrations.

**State:** source-only foundation and synthetic terminal prototype, under review. No broker connections, real accounts, bank transfers, executable trades or production deployment exist here.

## Explore the synthetic research terminal

    python -m http.server 4173 --directory web

Open http://localhost:4173. All displayed figures are deliberately synthetic; the terminal has no fetches or credentials.

## Test the finance research core

Requires Python 3.13+ and Node.js 22+; no external packages:

    PYTHONPATH=src python -m unittest discover -s tests -v
    python -m compileall -q src tests scripts
    PYTHONPATH=src python scripts/generate_synthetic_evidence.py --check
    node --test web/logic.test.mjs web/evidence-view.test.mjs
    node --check web/app.mjs

## Source map

- src/vesper — pure Decimal-based, owner/account-scoped performance primitives, with evidence completeness required explicitly.
- tests — independent offline unit tests for negative, missing, duplicate and mismatched data.
- web — responsive static terminal using only synthetic samples.
- docs — architecture, design, safeguards and predecessor history.
- .github/workflows — test-only CI without secrets or deployment.

See [architecture](docs/ARCHITECTURE.md), [product/experience](docs/PRODUCT.md), [legacy handoff](docs/LEGACY-HANDOFF.md), and [security](SECURITY.md).

## Repository boundaries

Vesper is separate from the Rhen programming language and Merit engineering integrity system. The large predecessor financial/research source has been preserved under [Vesper Legacy](https://github.com/devonalanakins/vesper-legacy) (GitHub repository ID `1384456079`), with its original history and open draft PRs, including the TPD evidence calculator. [Rhen](https://github.com/devonalanakins/rhen) is now an independent programming-language research repository, with an experimental compiler in draft review. No wholesale code migration, deletion, funding, or trading activation is permitted by this branch.

## Licensing

The owner has not approved a license yet. Public repository visibility does not grant open-source reuse rights. Choose and apply an approved license before accepting contributions or claiming a reusable open-source release.

## Read-only evidence projection

The Evidence screen consumes a checked-in, **synthetic-only** ES-module fixture generated from Python's Decimal-based time-weighted performance model. Generate it using `PYTHONPATH=src python scripts/generate_synthetic_evidence.py` and verify determinism with `--check`. The projection omits all owner, account, activity and evidence identifiers. It shows **unavailable** instead of exposing a number when the required evidence is incomplete.

This is not account authentication, broker reconciliation, production financial data, or investment advice. The projection's caller-supplied owner/account match is a data consistency guard; real authorization requires a future server-side identity and access layer. See [evidence contract](docs/EVIDENCE-CONTRACT.md).
