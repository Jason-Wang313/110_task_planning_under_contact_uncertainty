# Paper 110 Rebuild Plan: Task Planning Under Contact Uncertainty

Started: 2026-06-15 01:45:00 +0100

## Goal

Rebuild Paper 110 from a v3 archive into an evidence-backed ICLR-main-target submission candidate, or keep it archived if the evidence fails. The paper will remain explicitly not submission-ready unless external robot or independent high-fidelity evidence exists.

## Core Claim To Test

Task and motion planners fail when they collapse uncertain future contact outcomes into deterministic symbolic preconditions. The proposed planner should maintain a contact-outcome belief over future action branches and choose plans that are recoverable under plausible contact failures.

## Proposed Method

`proposed_contact_belief_tamp`

The method combines:
- Contact-outcome belief state over make, miss, slip, jam, release, and damage modes.
- Branch-aware symbolic preconditions that carry probability mass rather than Boolean contact predicates.
- Recovery affordance graph that scores whether a failed contact can be repaired.
- Contact-probe action selector for reducing uncertainty before irreversible steps.
- Chance-constrained plan scoring that penalizes precondition violations, damage, and unrecoverable branches.

## Benchmark Design

Run a local task-planning-under-contact benchmark with:
- Five tasks: peg insertion assembly, drawer retrieval, cable routing, tool levering, and mobile manipulation handoff.
- Seven uncertainty regimes: nominal, hidden friction, pose ambiguity, compliance ambiguity, jamming ambiguity, release uncertainty, and combined contact uncertainty.
- Five deployment splits: nominal, seen-shift, unseen-object, unseen-contact, and combined-stress.
- Nine methods: deterministic symbolic TAMP, robust geometric TAMP, receding-horizon MPC, learned failure classifier, ensemble belief planner, conformal risk TAMP, contingent POMDP-TAMP, proposed contact-belief TAMP, and oracle contact-outcome planner.
- Seven paired seeds with 84 episodes per task/regime/split/method.

## Primary Metrics

- Task success.
- Precondition violation rate.
- Contact-belief calibration error.
- Recovery success after failed contact.
- Irreversible damage rate.
- Wasted action rate.
- Intervention cost.
- Regret to oracle contact-outcome planner.

## Decision Gates

Mark `STRONG_REVISE` only if all are true:
- Success margin over the strongest non-oracle baseline is at least 0.030 on combined stress.
- Precondition violations fall by at least 0.030 or recovery success improves by at least 0.050.
- Damage, wasted actions, and intervention cost do not increase versus the strongest non-oracle baseline.
- Proposed method wins at least 5 of 7 paired seeds versus the strongest non-oracle baseline.
- Removing the contact-belief branch state reduces success by at least 0.020.

Otherwise mark `KILL_ARCHIVE`.

## Manuscript Changes

- Replace archive framing with a full paper about contact-belief task planning.
- Add related work around task and motion planning, contingent planning, POMDPs, robust MPC, and contact-rich manipulation.
- Include local evidence tables, stress curves, ablation figures, failure cases, and explicit limitations.
- Keep the limitation explicit: no real robot or accepted external high-fidelity benchmark validation yet.

## Artifact Requirements

- Produce `C:/Users/wangz/Downloads/110.pdf` only.
- Do not copy a PDF to the visible Desktop.
- Update `README.md`, `child_status.md`, paper docs, and root reports after the terminal decision.
- Commit and push the public GitHub repo only after local audits pass.
