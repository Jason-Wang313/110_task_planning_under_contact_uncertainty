# ICLR Main Gate

Paper: 110 task_planning_under_contact_uncertainty

Previous v3 decision: KILL_ARCHIVE

Gate verdict after v4 rebuild: STRONG_REVISE

Evidence digest: local contact-belief task-planning benchmark, 5 tasks, 7 uncertainty regimes, 5 splits, 9 methods, 7 paired seeds, 84 episodes per group.

Gate outcomes:
- Success margin over strongest non-oracle baseline: PASS (`0.080`).
- Diagnostic improvement: PASS (`-0.050` precondition violation and `+0.098` recovery success).
- Safety/cost non-regression: PASS.
- Pairwise seeds: PASS (7/7 wins).
- Ablation margin: PASS (`0.030`).

ICLR main ready: NO. Real robot or independent high-fidelity validation is still required.
