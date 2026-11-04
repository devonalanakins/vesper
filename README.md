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
    python -m compileall -q src tests
    node --test web/logic.test.mjs
    node --check web/app.mjs

## Source map

- src/vesper — pure Decimal-based, owner/account-scoped performance primitives, with evidence completeness required explicitly.
- tests — independent offline unit tests for negative, missing, duplicate and mismatched data.
- web — responsive static terminal using only synthetic samples.
- docs — architecture, design, safeguards and predecessor history.
- .github/workflows — test-only CI without secrets or deployment.

See [architecture](docs/ARCHITECTURE.md), [product/experience](docs/PRODUCT.md), [legacy handoff](docs/LEGACY-HANDOFF.md), and [security](SECURITY.md).

## Repository boundaries

Vesper is separate from the Rhen programming language and Merit engineering integrity system. The large predecessor finance/research repository is still temporarily located at [devonalanakins/rhen](https://github.com/devonalanakins/rhen). Preserve its existing commits and open draft pull requests, including the TPD evidence calculator. No wholesale migration, deletion, funding or trading activation is permitted by this branch.

## Licensing

The owner has not approved a license yet. Public repository visibility does not grant open-source reuse rights. Choose and apply an approved license before accepting contributions or claiming a reusable open-source release.
