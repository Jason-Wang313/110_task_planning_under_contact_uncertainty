# Final Audit

Paper: 110 task_planning_under_contact_uncertainty

Date: 2026-06-23 12:00:43 +08:00

Decision: STRONG_REVISE

ICLR main ready: no

The v5 expanded-standard rebuild reran Paper 110 as a hostile local mechanism audit of contact-belief task planning. The benchmark now covers 8 tasks, 10 regimes, 8 deployment splits, 16 methods, 10 paired seeds, 6 episodes per cell, 10 stress levels, 4 fixed-risk budgets, 10 ablations, and 24 failure cases.

## Evidence Counts

- 640 task/regime/split load cells.
- 102,400 main method cells.
- 10,240 task/regime/split/method aggregate rows.
- 1,280 method/split/seed rows.
- 128 method/split summaries.
- 160 hard-split seed rows.
- 16 hard-split method rows.
- 15 hard paired comparisons.
- 8,000 ablation cells.
- 48,000 stress-sweep cells.
- 51,200 fixed-risk cells.
- 24 failure cases.

## Gate Results

- Success gate: pass; margin `0.07021`.
- Utility gate: pass; margin `0.14891`.
- Diagnostic gate: pass; belief ECE delta `-0.04228`, precondition violation delta `-0.04426`.
- Safety gate: pass; damage delta `-0.01994`, wasted action delta `-0.02657`, irreversible commitment delta `-0.02793`.
- Pairwise gate: pass; 10/10 hard utility wins over `proposed_contact_belief_tamp_v4`.
- Ablation gate: pass; best removed-component gap is `0.01521` success or `0.06575` utility.
- Stress gate: pass; maximum-stress utility margin `0.14590`.
- Fixed-risk gate: pass; strict coverage `0.30375` and strict utility margin `0.20397`.
- Scope gate: fail; no real robot, accepted high-fidelity benchmark, trained external policy, deployment logs, or rollout videos.

## Artifact

- PDF: `C:/Users/wangz/Downloads/110.pdf`.
- Pages: 25.
- SHA256: `7BA9E1E4073EE7AEDEDA0A8916D0602C11BC1B2C2CD2FB9166AEFD83D0A4D62D`.
- Validator passed: `python scripts\validate_submission_artifacts.py`.

Remaining blocker: external robotics evidence. The paper should not be submitted to ICLR main until the scope gate is satisfied.
