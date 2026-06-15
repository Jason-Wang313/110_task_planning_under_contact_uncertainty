# Submission Attack Log

## Attack: This is just POMDP-TAMP.

Response: Contingent POMDP-TAMP is the strongest non-oracle baseline. Proposed improves success by `0.080 +/- 0.008` and reduces precondition violations, damage, wasted action, and cost.

## Attack: Robust MPC or conformal risk should solve this.

Response: Both are included as baselines and trail the proposed method under combined contact uncertainty.

## Attack: The benchmark is synthetic/local.

Response: Correct. This is why the decision is `STRONG_REVISE`, not ready acceptance.

## Attack: Probes can damage objects.

Response: Damage rate is lower than the strongest baseline locally, but hardware validation is required because probe safety is contact-dependent.
