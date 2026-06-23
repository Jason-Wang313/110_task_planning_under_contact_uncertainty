# 110 Task Planning Under Contact Uncertainty

Submission-hardening version: v5 expanded standard

Last update: 2026-06-23 12:00:43 +08:00

Terminal decision: STRONG_REVISE for ICLR main-conference development.

ICLR main ready: no.

This rebuild expands Paper 110 from a compact v4.1 local audit into a 25-page evidence-bound manuscript about contact-belief task planning. The local empirical gates pass, but the paper is still not ICLR-main-ready because the external scope gate fails: no real robot, accepted high-fidelity benchmark, trained external policy/planner, deployment logs, or rollout videos are present.

## Evidence Snapshot

- Benchmark: 8 tasks x 10 contact-uncertainty regimes x 8 deployment splits x 16 methods.
- Seeds: 10 paired seeds, 6 episodes per task/regime/split/method/seed cell.
- Main rows: 102,400 cell rows, 10,240 task/regime/split/method aggregate rows, 1,280 method/split/seed rows, and 128 method/split summaries.
- Strongest non-oracle baseline: `proposed_contact_belief_tamp_v4`.
- Proposed method: `contact_belief_branch_audit_v5`.
- Held-out hard success: `0.63000` proposed vs `0.55979` strongest baseline.
- Held-out hard utility: `0.61239` proposed vs `0.46348` strongest baseline.
- Belief ECE delta: `-0.04228`.
- Precondition violation delta: `-0.04426`.
- Recovery success delta: `+0.05874`.
- Damage delta: `-0.01994`.
- Wasted action delta: `-0.02657`.
- Pairwise utility wins: 10/10 seeds over the strongest baseline.
- Ablation margin: `0.01521` success or `0.06575` utility over the best removed component.
- Stress endpoint utility margin: `0.14590`.
- Strict fixed-risk coverage: `0.30375`; strict fixed-risk utility margin: `0.20397`.
- Failure cases: 24 documented hard-split cases.

## Artifact Snapshot

- Canonical numbered PDF: `C:/Users/wangz/Downloads/110.pdf`.
- PDF page count: 25.
- PDF SHA256: `7BA9E1E4073EE7AEDEDA0A8916D0602C11BC1B2C2CD2FB9166AEFD83D0A4D62D`.
- Bright boxed citation links: enabled in `paper/main.tex`.
- Validator: `python scripts\validate_submission_artifacts.py`.

## Reproduce Evidence

```powershell
python src\run_experiment.py
python scripts\generate_manuscript.py
```

## Rebuild PDF

```powershell
cd paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Then copy `paper/main.pdf` to `C:/Users/wangz/Downloads/110.pdf` and run:

```powershell
python scripts\validate_submission_artifacts.py
```
