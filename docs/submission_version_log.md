# Submission Version Log

## v3

Decision: KILL_ARCHIVE

Reason: synthetic/template evidence and no real or high-fidelity validation.

## v4

Decision: STRONG_REVISE

Changes:
- Added contact-belief task-planning benchmark.
- Added local baselines, paired-seed tests, planning/safety/cost gates, ablations, stress sweep, failure cases, figures, and generated tables.

Remaining blocker: no real robot or independent high-fidelity validation.

## v4.1

Decision: STRONG_REVISE

Changes:
- Added a paper-specific ICLR submission-readiness execution plan before rerunning.
- Reran the full local benchmark.
- Expanded stress-sweep evidence and failure cases.

Remaining blocker: no real robot or independent high-fidelity validation, no external trained baselines, and no hardware videos or deployment logs.

## v5 expanded standard

Decision: STRONG_REVISE

Changes:
- Froze a new expanded plan before experiment edits.
- Expanded to 8 tasks, 10 regimes, 8 splits, 16 methods, 10 paired seeds, and 6 episodes per cell.
- Added v5 method `contact_belief_branch_audit_v5`.
- Added strict local gates for success, utility, diagnostics, safety, pairwise seeds, ablations, stress, fixed-risk acceptance, and scope.
- Added 102,400 main cells, 8,000 ablation cells, 48,000 stress cells, 51,200 fixed-risk cells, and 24 failure cases.
- Tightened fixed-risk budgets into the observed risk-score range so strict coverage is `0.30375`, not a trivial `1.0`.
- Added `summary.json`, generated support tables, six generated figures, manuscript generator, and validator.
- Rebuilt a 25-page PDF with bright boxed clickable citation links.

Remaining blocker: the scope gate fails because external robot/high-fidelity evidence is absent.
