# Paper 110 Expanded Submission Plan

Date: 2026-06-23

This is the frozen plan for rebuilding `task_planning_under_contact_uncertainty` into an expanded-standard submission candidate. It is intentionally hostile to the method: the purpose is not to make the figures pretty, but to determine whether the contact-belief planning mechanism survives stronger baselines, wider stress tests, fixed-risk analysis, and mechanism ablations.

## Non-Negotiable Rules

- Do not invent real robot evidence, external benchmark evidence, trained checkpoint evidence, or rollout-video evidence.
- Do not optimize for pretty results. Optimize for a result that survives hostile review.
- Use strong baselines and stress tests to expose weaknesses, improve the method during development, then freeze the final protocol and report all predefined results honestly.
- Do not pad to 25 pages. Add theory, protocols, diagnostics, tables, figures, negative cases, and review-facing analysis that would actually help a reviewer assess the claim.
- Keep the final numbered PDF only in Downloads.

## Claim Under Test

The narrow claim is that task planners under contact uncertainty should preserve contact-outcome belief mass over future branches and score those branches by recoverability, probe value, damage risk, branch budget, entropy calibration, and irreversible resource use. The mechanism should lower invalid preconditions, damage, wasted actions, and regret to an oracle while improving success and utility under hard contact shifts.

## Expanded CPU-Only Protocol

- 8 task families.
- 10 contact-uncertainty regimes.
- 8 deployment splits.
- 16 methods, including two oracle references and 14 non-oracle comparators.
- 10 paired seeds.
- 6 episodes per task/regime/split/method/seed cell.

The protocol produces 102,400 main cell rows, 10,240 task/regime/split/method groups, 1,280 seed summaries, 128 method/split summaries, 160 hard-split seed rows, 16 hard-split metric rows, 15 hard paired comparisons, 8,000 ablation rows, 48,000 stress rows, 51,200 fixed-risk rows, and 24 failure cases.

## Frozen Terminal Rule

If local empirical gates pass but the scope gate fails, the decision is `STRONG_REVISE`. If any empirical gate fails, the decision is `KILL_ARCHIVE`. ICLR-main readiness remains `no` unless the missing external-evidence scope gate is satisfied in a future version.

## Manuscript Requirements

- At least 25 pages.
- Bright boxed citations via `hyperref`, with in-text citations routed to references.
- Generated tables and figures only from frozen outputs.
- Explicit theory and failure-mode sections.
- A clear final decision that a hostile reviewer can audit.
