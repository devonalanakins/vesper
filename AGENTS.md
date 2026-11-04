# Vesper engineering rules

This public repository owns an **offline research and read-only synthetic terminal**. Preserve that boundary.

1. No broker APIs, bank transfers, order placement, real account data, deployment credentials or external scheduled actions in unapproved development.
2. Before porting any old Rhen finance behavior, independently review provenance, inputs/outputs, risk invariants, licenses and tests. Never blindly copy.
3. Financial types must have explicit owner/account scope, timezone-aware evidence timestamps, Decimal arithmetic, and fail-closed incomplete-data semantics.
4. Separate measured, synthetic, hypothetical, paper and independently verified live outcomes visually and in exported schemas.
5. Keep the visual terminal honest. It currently has no authentication or private account APIs; all numbers are synthetic and must say so.
6. Use reviewable branches and draft pull requests; test exact heads. No merge, deployment, migration, live orders or financial side effects without appropriate approval and verification.
7. Vesper, Rhen language, Merit, DevonStation, and Anevum own separate repositories and authority.

Read docs/ARCHITECTURE.md and SECURITY.md before changing integrations.
