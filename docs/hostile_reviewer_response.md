# Hostile Reviewer Response

Paper: 110 Task Planning Under Contact Uncertainty

## Strongest Technical Threats

- The method may be a renamed contingent POMDP-TAMP.
- Robust TAMP, conformal risk filtering, contact-implicit planning, or damage-aware planning may already solve the problem.
- The benchmark is local and generated.
- The fixed-risk result could be a conservative rejection trick.
- Contact uncertainty may require tactile or hardware validation.

## Response

The v5 rebuild includes contingent POMDP-TAMP, conformal risk TAMP, risk-aware TAMP, contact-implicit TAMP, damage-aware planning, learned contact belief state, the v4 contact-belief baseline, and two oracle references. The strongest non-oracle baseline is selected automatically as `proposed_contact_belief_tamp_v4`, not chosen manually.

Against that baseline, v5 improves hard success by `0.07021`, hard utility by `0.14891`, belief ECE by `-0.04228`, invalid preconditions by `-0.04426`, recovery by `+0.05874`, damage by `-0.01994`, wasted actions by `-0.02657`, and irreversible commitment by `-0.02793`. The strict fixed-risk budget is intentionally in the observed risk range, yielding coverage `0.30375` rather than a trivial `1.0`.

## Honest Action

Mark as `STRONG_REVISE`, not acceptance-ready. Submission requires real robot or independent high-fidelity experiments, external trained planner/policy baselines, contact traces, videos, and deployment logs.
