# Paper 110 ICLR Submission-Readiness Execution Plan

Date: 2026-06-15

Paper: `110_task_planning_under_contact_uncertainty`

Working title: Task Planning Under Contact Uncertainty

## Goal

Re-audit Paper 110 as if preparing an ICLR-main submission, while keeping the decision evidence-bound. The paper may remain `STRONG_REVISE` only if the rerun reproduces a decisive local contact-belief task-planning advantage over the strongest non-oracle baseline without increasing damage, wasted actions, or intervention cost. It must not be marked ICLR-main-ready without real robot or independent high-fidelity benchmark validation.

## Current Hypothesis

Task and motion planners fail when uncertain future contact outcomes are collapsed into deterministic symbolic preconditions. The proposed `proposed_contact_belief_tamp` should improve planning by carrying contact-outcome belief mass through future branches and choosing plans that remain recoverable under plausible contact failures.

## Evidence To Rebuild

- Compile-check `src/run_experiment.py`.
- Re-run the full local benchmark from scratch with fixed threading.
- Verify CSV coverage for metrics, per-task/regime records, seed-level splits, paired comparisons, ablations, stress sweep, and failure cases.
- Confirm the strongest non-oracle baseline under combined stress.
- Confirm success, precondition violation, belief calibration error, recovery success, damage rate, wasted action, intervention cost, and regret-to-oracle results.
- Confirm pairwise seed wins and 95 percent confidence intervals.
- Confirm every removed-component ablation remains below the full method.
- Confirm the stress sweep preserves ordering through maximum contact-uncertainty stress.
- Confirm the PDF rebuild uses the ICLR style, has no fatal LaTeX/BibTeX issues, and is copied only to `C:/Users/wangz/Downloads/110.pdf`.
- Confirm no `110.pdf` exists on the visible Desktop.
- Confirm the public GitHub repo is current after any edits.

## Decision Gates

Keep `STRONG_REVISE` only if all gates pass:

- Success margin over strongest non-oracle baseline is at least `0.030` on combined stress.
- Precondition violations fall by at least `0.030` or recovery success improves by at least `0.050`.
- Damage, wasted actions, and intervention cost do not increase versus the strongest non-oracle baseline.
- Proposed method wins at least `5/7` paired seeds against the strongest non-oracle baseline.
- The full method beats the best removed-component ablation by at least `0.020`.

Mark `KILL_ARCHIVE` if any gate fails.

Do not mark ICLR-main-ready unless there is real robot or independent high-fidelity validation with trained planning/policy baselines. The current local benchmark can support only `STRONG_REVISE`.

## Execution Steps

1. Audit the repository state and prior v4 documents for stale or inflated claims.
2. Run `python -m py_compile src/run_experiment.py`.
3. Run `python src/run_experiment.py` with `OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, and `MKL_NUM_THREADS` set to `1`, logging to the root `logs` directory.
4. Programmatically validate result files for row counts, finite numeric values, strongest-baseline identity, gate outcomes, pairwise statistics, ablations, stress sweep, and failure cases.
5. Patch recoverable rigor gaps, especially stress-sweep granularity or failure-case coverage, then rerun if needed.
6. Patch `README.md`, `child_status.md`, `plan.md`, `docs/submission_readiness_decision.md`, `docs/final_audit.md`, `docs/iclr_main_gate.md`, `docs/submission_version_log.md`, and `paper/main.tex` to reflect the verified rerun.
7. Add a terminal audit document and a v4.1 submission-readiness audit document.
8. Rebuild the paper with `pdflatex`, `bibtex`, `pdflatex`, and `pdflatex`.
9. Scan `main.log` and `main.blg`; fix recoverable Overfull/Underfull, undefined-reference, citation, or bibliography issues.
10. Copy only `paper/main.pdf` to `C:/Users/wangz/Downloads/110.pdf`.
11. Hash `C:/Users/wangz/Downloads/110.pdf`, confirm file size, and confirm `C:/Users/wangz/Desktop/110.pdf` is absent.
12. Commit and push the child repository to its public GitHub repo.
13. Update the root `GLOBAL_POOL_STATUS.md`, `BATCH_STATUS.md`, `SUBMISSION_STATUS.md`, `MASTER_REPORT.md`, and `MASTER_SUBMISSION_REPORT.md` through Paper 110.

## Expected Terminal Wording

If the rerun matches the prior evidence, the honest terminal state is:

`STRONG_REVISE`: local contact-belief task-planning evidence supports continuing, but the paper is not ICLR-main-ready because it lacks real robot or independent high-fidelity validation and external trained planning/policy baselines.
