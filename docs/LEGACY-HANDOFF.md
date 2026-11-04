# Legacy source and repository handoff

## Verified inventory (November 4, 2026)

| Item | Observed state |
| --- | --- |
| New Vesper | `devonalanakins/vesper`; GitHub repository ID `1445180370`; independent history; initial commit `dc33df2259dd15824372ac4c202c511a30d72f8e` |
| Predecessor financial/trading repository | Currently `devonalanakins/rhen`; GitHub repository ID `1384456079`; existing code and history still present; observed `main` commit `0430a4ea89463e5d6943bf674004f5b245e6d450` |
| Legacy open review work | Draft PR #497 (TPD research and evidence) and draft PR #500 (identity documentation), among other existing work. Preserve all open PRs and branches. |
| New Rhen programming language | Separate, **not yet verified as a new dedicated GitHub repository**. Never treat the predecessor financial repository as language source. |

The GitHub **repository ID**, rather than a reusable slug, identifies the original history after a rename. A historical URL beginning with `.../rhen` may become misleading when that name is assigned to a new repository.

## Intended boundary and rename sequence

1. Preserve the predecessor repo, all branches, open PRs, Git history, and external reference inventory. Do not delete or force-push it.
2. Rename the predecessor to a distinct archival name such as `vesper-legacy` **only after confirming dependent GitHub Actions, integrations, webhooks, deployments, and external links**. This change has not been executed by this documentation.
3. Keep the newly created `vesper` repository as the clean redesign, with no direct history rewrite or wholesale migration.
4. After the `rhen` name is actually freed, create a new, distinct `rhen` repository for the programming language, starting from its own first commit and language-specific specifications, tests, and license decision.
5. Update Notion, GitHub descriptions, links, and any verified public portfolio references to point to the correct repository ID and purpose.

## Research-only source reuse

Before moving a specific component from the predecessor, document its current behavior, provenance and license, relevant inputs/outputs, risks, tests, and reasons it fits the new design. Port only reviewed functionality, with new tests. Do not carry old credentials, order settings, financial data, or deployment configuration.

Do not assume a paper-mode test proves safe live execution, or a passing GitHub workflow proves account-authorized financial behavior.

## Release boundaries

The documentation handoff does not enable trading, broker connections, bank transfers, strategy execution, live scheduling, or deployment. Those require separate authorization and independent risk/security/recovery verification. This record does not claim that any of those approvals has occurred.
