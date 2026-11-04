# Vesper

> **Status: clean-slate redesign.** This repository is an initial project shell, not a running application or an automated trading system.

Vesper is an independent quantitative research and financial-systems engineering project. The intent is to re-examine the architecture, safeguards, and useful experiments from earlier work, then build a maintainable system from first principles.

The earlier financial/trading codebase was called **RHEN**. That name is now reserved for a **separate programming-language project, Rhen**. The two projects do not share a codebase or release process.

## What exists here

- An initial project boundary and legacy-reference record.
- **No verified implementation, tests, broker connection, production deployment, automated execution, or investment-performance result in this new repository.**

For the transition and the preserved predecessor history, see [Legacy handoff](docs/LEGACY-HANDOFF.md).

## Engineering approach

1. Begin with explicit, testable research questions and safety requirements.
2. Study the predecessor implementation as reference material; do not assume it is suitable for direct migration.
3. Implement small, independently testable modules with clear data provenance and failure behavior.
4. Keep offline research, paper simulation, and any eventual broker execution distinct.
5. Require independent risk, security, account-ownership, and authorization review before any financial side effects.

The new platform's architecture and features are not considered implemented merely because they are proposed or existed in earlier code.

## Project boundaries

| Project | Purpose |
| --- | --- |
| **Vesper** | Quantitative research, risk analysis, and separately authorized financial-systems development |
| **Rhen** | Independent general-purpose language research and implementation; to be established in its own clean repository |
| **Merit** | Independent engineering-integrity and evidence-review project |

Do not move private account data, credentials, order histories, customer records, or broker configuration between repositories. Do not deploy, fund, or activate trading from this documentation.

## Contributing and licensing

This repository has not yet selected or added a software license. Public visibility by itself does **not** grant general reuse rights. A license must be selected and applied before claiming a reusable open-source release. No external contributions or financial integrations are authorized by this initial README.

## Current next step

Complete the predecessor repository name handoff without deleting or force-rewriting its branches or pull requests. Then begin Vesper's clean architecture and independently testable research core.
