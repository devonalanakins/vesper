# Legacy source and repository handoff

## Verified inventory (November 4, 2026)

| Item | Observed state |
| --- | --- |
| New Vesper | `devonalanakins/vesper`; GitHub repository ID `1445180370`; independent history; initial commit `dc33df2259dd15824372ac4c202c511a30d72f8e` |
| Predecessor financial/trading repository | Currently `devonalanakins/rhen`; GitHub repository ID `1384456079`; existing code and history still present; observed `main` commit `0430a4ea89463e5d6943bf674004f5b245e6d450` |
| Legacy open review work | [Draft PR #497](https://github.com/devonalanakins/rhen/pull/497) (TPD research), [draft PR #500](https://github.com/devonalanakins/rhen/pull/500) (identity documentation), among other work. Preserve every open PR and branch. |
| New Rhen programming language | Separate, **not yet verified as a dedicated GitHub repository**. Never treat the predecessor financial repository as language source. |

The GitHub **repository ID**, rather than a reusable slug, identifies the original history after a rename. A historical URL beginning with `.../rhen` may become misleading when the name is assigned to a new repository.

## Known repository-name dependencies to reconcile

Read-only GitHub code search of public default branches found **at least** the following references. This is not a complete dependency, deployment or webhook inventory.

| Source | Why it matters |
| --- | --- |
| [anevum-web cross-repo schema verifier](https://github.com/devonalanakins/anevum-web/blob/main/scripts/verify-v5-cross-repo-schema.mjs) | Constructs a GitHub API URL using `devonalanakins/rhen`, including a pinned contract branch; could resolve the wrong repository after name reuse. |
| [anevum-web cross-repo tests](https://github.com/devonalanakins/anevum-web/blob/main/tests/v5-cross-repo-schema.test.mjs) | Assert `api.github.com/repos/devonalanakins/rhen` and `raw.githubusercontent.com/devonalanakins/rhen/` literally. |
| [devonakins.com portfolio content](https://github.com/devonalanakins/devonakins.com/blob/main/src/content.mjs) | Describes the old financial system under its former name, affecting public identity and links. |
| [anevum project registry](https://github.com/devonalanakins/anevum/blob/main/PROJECT_REGISTRY.md) and [public metadata](https://github.com/devonalanakins/anevum/blob/main/PUBLIC_REPOSITORY_METADATA.md) | Historical links and repository descriptions could become inaccurate. |
| [GitHub profile README](https://github.com/devonalanakins/devonalanakins/blob/main/README.md) | Public project list may still treat Rhen as the trading system. |
| Old RHEN open PRs and Actions | Existing financial-source branches, tests and CI may contain slug references. Must keep history intact. |

**Do not rename and reuse `rhen` until the cross-repo verifier can reference the predecessor by its new exact slug or stable SHA (as applicable), and the affected checks are rerun.** Verify hosting, CI, installed app settings, webhooks, branch-protection/rulesets, external clients and DNS separately; code search cannot establish those are safe. A GitHub redirect is **not** a reliable permanent dependency once the old slug is reused.

## Intended boundary and rename sequence

1. Inventory and preserve the predecessor repository, branches, PRs, Git history, external references and deployment dependencies. Do not delete or force-push.
2. Repoint confirmed dependencies away from `devonalanakins/rhen`; verify the affected workflows and recorded external links. Where changes are high consequence, use their owning PRs and release gates.
3. Rename the predecessor to a distinct historical name such as `vesper-legacy` **after approval and safety checks**. This has not been executed by this documentation.
4. Keep the new `vesper` repository as the clean redesign, with no history rewrite or wholesale source migration.
5. After the `rhen` name is actually freed, create a new, distinct `rhen` repository for the independent programming language, starting from its own first commit, language-specific scope, tests, and license decision.
6. Recheck every old link and update Notion, GitHub descriptions and public portfolio references to their correct projects.

## Research-only source reuse

Before moving a specific component from the predecessor, document its actual behavior, provenance and license, relevant inputs/outputs, risks, tests, and why it fits the new design. Port only reviewed functionality, with new tests. Do not carry old credentials, order settings, financial data, or deployment configuration.

Do not assume a paper-mode test proves safe live execution, or a passing GitHub workflow proves account-authorized financial behavior.

## Release boundaries

This documentation handoff does not enable trading, broker connections, bank transfers, strategy execution, live scheduling, or deployment. Those require separate authorization and independent risk/security/recovery verification. This record does not claim that those approvals exist.
