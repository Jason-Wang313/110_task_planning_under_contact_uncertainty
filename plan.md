# Paper 110 Expanded-Standard Plan

Paper: `task_planning_under_contact_uncertainty`

Target: rebuild Paper 110 into a 25+ page, evidence-bound ICLR-main-target manuscript without filler. The manuscript may become `STRONG_REVISE` only if all frozen local empirical gates pass. It must remain `KILL_ARCHIVE` if the expanded protocol falsifies the mechanism. It must not be marked ICLR-main-ready without real robot, accepted high-fidelity benchmark, trained external baseline, or independent deployment evidence.

## Frozen V5 Protocol

- Expand scope from 5 tasks, 7 regimes, 5 splits, and 9 methods to 8 tasks, 10 contact-uncertainty regimes, 8 deployment splits, and 16 methods.
- Use 10 paired seeds and 6 episodes per task/regime/split/method/seed cell to keep the CPU-only protocol RAM-light while preserving paired statistical structure.
- Write row-level and aggregate CSVs deterministically from `src/run_experiment.py`; no manual editing of numeric results.
- Freeze all methods, metrics, ablations, stress levels, fixed-risk budgets, failure-case rules, and terminal gates before reading the final results.
- Preserve bright boxed clickable citation links in the PDF and route every in-text citation to the bibliography.
- Keep the final numbered PDF only at `C:/Users/wangz/Downloads/110.pdf`; do not copy the PDF to Desktop.

## Benchmark Axes

- Tasks: peg assembly, drawer retrieval, cable routing, tool levering, mobile handoff, bimanual fixture alignment, deformable bin packing, and legged support recovery.
- Regimes: nominal, hidden friction, pose ambiguity, compliance ambiguity, jamming ambiguity, release uncertainty, partial-observability dropout, irreversible damage risk, branch resource depletion, and combined contact uncertainty.
- Splits: nominal, seen shift, unseen object, unseen contact, unseen compliance, probe latency, sensor dropout, and heldout combined contact uncertainty.
- Methods: deterministic symbolic TAMP, robust geometric TAMP, receding-horizon MPC, learned failure classifier, ensemble belief planner, conformal risk TAMP, smooth precondition world model, contact-implicit TAMP, contingent POMDP-TAMP, risk-aware TAMP, learned contact belief state, damage-aware planner, proposed v4 contact-belief TAMP, v5 contact-belief branch audit, oracle contact-outcome planner, and oracle hybrid contact planner.

## Metrics

- Primary performance: success and utility.
- Contact-planning diagnostics: precondition violation, belief ECE, branch entropy error, recovery success, wasted action, intervention cost, probe overhead, irreversible commitment, and regret to oracle.
- Safety and robustness: damage rate, fixed-risk coverage, strict fixed-risk utility, maximum-stress success, and maximum-stress utility.
- Mechanism necessity: removed-component ablations for belief state, recovery graph, probe selector, chance constraint, damage model, branch budget, entropy calibration, irreversible resource accounting, v4-only planner, and POMDP-only planner.

## Evidence Gates

- Success and utility must beat the strongest non-oracle baseline on the heldout hard split by at least 0.03 and 0.04 respectively.
- Diagnostics must improve belief/precondition/recovery behavior against the strongest non-oracle baseline without increasing damage, wasted actions, irreversible commitments, or intervention cost.
- Pairwise seed comparisons against the strongest non-oracle baseline must win at least 8/10 seeds on hard success.
- Every required component ablation must trail the full v5 method by at least 0.02 success or 0.04 utility.
- Stress-sweep endpoint and fixed-risk gates must not be dominated by non-oracle baselines.
- Scope gate is false unless external robot/high-fidelity evidence exists, so even a local empirical pass remains `STRONG_REVISE`, not ICLR-main-ready.

## Deliverables

- New deterministic evidence under `results/` with `summary.json`, CSVs, generated LaTeX tables, and generated figures.
- A 25+ page manuscript with theory, protocol, results, ablations, stress tests, fixed-risk analysis, failure cases, limitations, and hostile-review responses.
- A validation script that checks row counts, gates, page count, PDF hash, Downloads-only artifact placement, and generated table presence.
- Updated `README.md`, `child_status.md`, and docs describing the honest terminal decision.
- Public GitHub update using the noreply identity `Jason-Wang313 <202470630+Jason-Wang313@users.noreply.github.com>`.
