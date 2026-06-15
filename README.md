# 110 Task Planning Under Contact Uncertainty

Submission-hardening version: v4

Terminal decision: STRONG_REVISE for ICLR main-conference development.

This rebuild replaces the v3 archive with a local contact-belief task-planning benchmark. The paper is still not ICLR-main-ready because it lacks real robot or independent high-fidelity benchmark validation, but the local evidence supports continued development.

## Evidence Snapshot

- Benchmark: 5 tasks x 7 contact-uncertainty regimes x 5 deployment splits x 9 methods.
- Seeds: 7 paired seeds, 84 episodes per task/regime/split/method group.
- Strongest non-oracle baseline: `contingent_pomdp_tamp`.
- Proposed: `proposed_contact_belief_tamp`.
- Combined-stress success: `0.560 +/- 0.004` proposed vs `0.480 +/- 0.006` strongest baseline.
- Precondition violation: `0.057` proposed vs `0.108` strongest baseline.
- Recovery success: `0.559` proposed vs `0.461` strongest baseline.
- Pairwise wins: 7/7 seeds over the strongest baseline.
- Best removed-component ablation: `minus_damage_model`; full method remains ahead by `0.030` success.

## Reproduce Evidence

```powershell
python src\run_experiment.py
```

## Rebuild PDF

```powershell
cd paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Canonical local PDF: `C:/Users/wangz/Downloads/110.pdf`
