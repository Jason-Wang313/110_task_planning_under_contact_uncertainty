# Paper 110 Terminal Audit

Date: 2026-06-15

Paper: `110_task_planning_under_contact_uncertainty`

Terminal decision: STRONG_REVISE

ICLR main ready: no

## What Passed

- Plan-first execution document created before rerun.
- `src/run_experiment.py` compiles.
- Full experiment rerun completed.
- CSV row-count gate passed for primary metrics, task/regime seed metrics, split seed metrics, paired stats, ablations, stress sweep, and failure cases.
- Numeric sanity found zero NaN/Inf issues.
- Strongest non-oracle baseline is `contingent_pomdp_tamp`.
- Proposed method beats the strongest baseline by `0.080 +/- 0.008` paired success and wins `7/7` seeds.
- Precondition violations fall from `0.108` to `0.057`.
- Recovery success improves from `0.461` to `0.559`.
- Belief ECE, damage rate, wasted action, and intervention cost are all lower than the strongest baseline.
- Full method remains above the best removed-component ablation by `0.030` success.
- Stress sweep at level `1.0` keeps proposed above receding-horizon MPC, conformal risk TAMP, and contingent POMDP-TAMP.
- Eight failure cases are documented.
- PDF rebuild passed and produced `C:/Users/wangz/Downloads/110.pdf`.
- PDF SHA256: `D1CD8951543DE7BD88BDF9278DB554D41B2BDBD5424045EE184A4057974B84FD`.
- No `C:/Users/wangz/Desktop/110.pdf` copy exists.

## What Still Blocks Submission

- No real robot evidence.
- No independent high-fidelity simulator validation.
- No external trained planning/policy baselines.
- No hardware videos or deployment logs.
- Oracle remains higher than proposed, indicating unresolved contact-outcome planning headroom.

## Honest Outcome

This paper should continue as `STRONG_REVISE`, not be submitted to ICLR main. The next version needs external validation before the central claim can be treated as submission-ready evidence.
