# 110 Task Planning Under Contact Uncertainty

Submission-hardening version: v4.1

Terminal decision: STRONG_REVISE for ICLR main-conference development.

This continuation audit reruns and hardens the v4 local contact-belief task-planning benchmark. The paper is still not ICLR-main-ready because it lacks real robot or independent high-fidelity benchmark validation, but the local evidence supports continued development.

## Evidence Snapshot

- Benchmark: 5 tasks x 7 contact-uncertainty regimes x 5 deployment splits x 9 methods.
- Seeds: 7 paired seeds, 84 episodes per task/regime/split/method group.
- Strongest non-oracle baseline: `contingent_pomdp_tamp`.
- Proposed: `proposed_contact_belief_tamp`.
- Combined-stress success: `0.560 +/- 0.004` proposed vs `0.480 +/- 0.006` strongest baseline.
- Precondition violation: `0.057` proposed vs `0.108` strongest baseline.
- Recovery success: `0.559` proposed vs `0.461` strongest baseline.
- Pairwise wins: 7/7 seeds over the strongest baseline.
- Best removed-component ablation: `minus_damage_model`; full method remains ahead by `0.030` success.
- Expanded stress-sweep seed/task/regime rows: 7350.
- Failure cases: 8 documented limitations.

## Continuation Audit

- Log: `C:/Users/wangz/robotics_massive_pool_paper_factory/logs/110_task_planning_under_contact_uncertainty_continuation_rerun_20260615.log`
- CSV row-count gate: passed for metrics, task/regime seeds, paired stats, ablations, stress sweep, and failure cases.
- Numeric sanity gate: passed with zero NaN/Inf issues.
- Artifact rule: final numbered PDF belongs in `C:/Users/wangz/Downloads/110.pdf` only.
- PDF SHA256: `D1CD8951543DE7BD88BDF9278DB554D41B2BDBD5424045EE184A4057974B84FD`.

## Reproduce Evidence

```powershell
python src\run_experiment.py
```

## Rebuild PDF

```powershell
cd paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Canonical local PDF: `C:/Users/wangz/Downloads/110.pdf`
