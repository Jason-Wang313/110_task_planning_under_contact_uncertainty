# Hostile Prior Work

The broad claim "planning under uncertainty improves robotics" is not novel.

Relevant pressure points:
- Task and motion planning already integrates symbolic task structure with geometric feasibility.
- PDDLStream and related systems already handle sampling-based task and motion planning.
- POMDP and contingent planning already maintain uncertainty over future branches.
- Robust MPC and risk-aware planners already optimize under uncertainty.
- Contact-rich manipulation work already studies failure recovery, compliance, and uncertainty.

The novelty boundary is narrow: this paper tests whether a contact-outcome belief over future contact branches improves TAMP decisions under contact uncertainty while reducing precondition violations, damage, and wasted actions.
