# ICLR Main Gate

Paper: 110 task_planning_under_contact_uncertainty

Gate verdict after v5 expanded-standard rebuild: STRONG_REVISE

ICLR main ready: NO

## Evidence Digest

- 8 tasks, 10 contact-uncertainty regimes, 8 deployment splits, 16 methods.
- 10 paired seeds, 6 episodes per cell.
- Strongest non-oracle baseline: `proposed_contact_belief_tamp_v4`.
- Proposed method: `contact_belief_branch_audit_v5`.
- Held-out hard success: `0.63000` vs `0.55979`.
- Held-out hard utility: `0.61239` vs `0.46348`.
- Strict fixed-risk coverage: `0.30375`.
- PDF: 25 pages, SHA256 `7BA9E1E4073EE7AEDEDA0A8916D0602C11BC1B2C2CD2FB9166AEFD83D0A4D62D`.

## Gate Outcomes

- Success: PASS.
- Utility: PASS.
- Diagnostics: PASS.
- Safety/cost non-regression: PASS.
- Pairwise seeds: PASS, 10/10 hard utility wins.
- Ablations: PASS.
- Stress endpoint: PASS.
- Fixed-risk endpoint: PASS.
- Scope: FAIL.

Conclusion: strong-revise local mechanism evidence, not ICLR-main-ready submission evidence.
