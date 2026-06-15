# Submission Readiness Audit v4.1

Paper: 110 task_planning_under_contact_uncertainty

Date: 2026-06-15

Decision: STRONG_REVISE

ICLR main ready: no

## Rerun

- Command: `python -m py_compile src/run_experiment.py`
- Command: `python src/run_experiment.py`
- Log: `C:/Users/wangz/robotics_massive_pool_paper_factory/logs/110_task_planning_under_contact_uncertainty_continuation_rerun_20260615.log`
- Numeric sanity: zero NaN/Inf issues across CSV outputs.
- PDF: `C:/Users/wangz/Downloads/110.pdf`
- PDF SHA256: `D1CD8951543DE7BD88BDF9278DB554D41B2BDBD5424045EE184A4057974B84FD`
- PDF size: 399503 bytes.
- Desktop PDF copy: absent.

## Coverage

- `metrics.csv`: 45 rows.
- `per_task_regime_metrics.csv`: 1575 rows.
- `seed_task_regime_metrics.csv`: 11025 rows.
- `seed_split_metrics.csv`: 315 rows.
- `pairwise_stats.csv`: 8 rows.
- `ablation_metrics.csv`: 7 rows.
- `ablation_seed_metrics.csv`: 49 rows.
- `ablation_task_regime_seed_metrics.csv`: 1715 rows.
- `stress_sweep.csv`: 30 rows.
- `stress_sweep_seed_metrics.csv`: 7350 rows.
- `failure_cases.csv`: 8 rows.

## Gate Evidence

- Strongest non-oracle baseline: `contingent_pomdp_tamp`.
- Combined-stress success: `0.560 +/- 0.004` proposed vs `0.480 +/- 0.006` strongest baseline.
- Precondition violation: `0.057` proposed vs `0.108` strongest baseline.
- Belief ECE: `0.068` proposed vs `0.108` strongest baseline.
- Recovery success: `0.559` proposed vs `0.461` strongest baseline.
- Damage rate: `0.047` proposed vs `0.060` strongest baseline.
- Wasted action: `0.073` proposed vs `0.103` strongest baseline.
- Intervention cost: `0.213` proposed vs `0.311` strongest baseline.
- Paired success gain: `0.080 +/- 0.008`, with `7/7` seed wins.
- Best removed-component ablation: `minus_damage_model`; full method remains ahead by `0.030` success.
- Max stress level `1.0`: proposed success `0.5470 +/- 0.0058`; contingent POMDP-TAMP `0.4575 +/- 0.0059`; conformal risk TAMP `0.4122 +/- 0.0065`; receding-horizon MPC `0.3893 +/- 0.0048`; oracle `0.6436 +/- 0.0074`.

## Terminal Assessment

The local evidence supports continuing the paper as a strong-revise candidate: the method beats the strongest non-oracle baseline, reduces precondition violations, improves recovery, lowers damage/wasted-action/cost metrics, wins paired seeds, survives ablations, and remains above core baselines through the stress sweep.

The paper is still not ICLR-main-ready. The blocker is external validity: no real robot validation, no independent high-fidelity simulator validation, no external trained planning/policy baselines, and no hardware videos or deployment logs.
