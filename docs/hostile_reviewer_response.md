# Hostile Reviewer Response

Paper: 110 Task Planning Under Contact Uncertainty

## Strongest Technical Threats

- This may be just contingent POMDP-TAMP with different terminology.
- Robust TAMP, conformal planning, and MPC already handle uncertainty.
- The benchmark is local and generated, not real robot evidence.
- Contact uncertainty may need tactile/hardware validation.

## Response

The v4 rebuild includes contingent POMDP-TAMP as the strongest non-oracle baseline. The proposed method improves combined-stress success by `0.080 +/- 0.008`, reduces precondition violations by `0.050`, improves recovery success by `0.098`, and lowers damage, wasted actions, and intervention cost.

## Honest Action

Mark as `STRONG_REVISE`, not ready acceptance. Submission requires real robot or independent high-fidelity experiments and external trained planner/policy baselines.
