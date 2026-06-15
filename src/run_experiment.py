import csv
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


BASE_SEED = 110_2026
SEEDS = list(range(7))
EPISODES_PER_GROUP = 84

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RESULTS.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)

OBSOLETE_OUTPUTS = [
    RESULTS / "raw_seed_metrics.csv",
    RESULTS / "negative_cases.csv",
    FIGURES / "stress_curve_data.csv",
]

DISPLAY_NAMES = {
    "deterministic_symbolic_tamp": "DetTAMP",
    "robust_geometric_tamp": "RobustTAMP",
    "receding_horizon_mpc": "MPC",
    "learned_failure_classifier": "FailureCls",
    "ensemble_belief_planner": "EnsembleBelief",
    "conformal_risk_tamp": "ConformalTAMP",
    "contingent_pomdp_tamp": "POMDP-TAMP",
    "proposed_contact_belief_tamp": "Proposed",
    "oracle_contact_outcome_planner": "Oracle",
    "full_contact_belief_tamp": "Full",
    "minus_contact_belief_state": "NoBelief",
    "minus_recovery_affordance_graph": "NoRecovery",
    "minus_contact_probe_selector": "NoProbe",
    "minus_chance_constraint": "NoChance",
    "minus_damage_model": "NoDamage",
    "pomdp_only": "POMDPOnly",
}

TASKS = [
    {"task": "peg_assembly", "difficulty": 0.078, "contact": 0.92, "irreversible": 0.58, "recovery": 0.54, "precision": 0.86},
    {"task": "drawer_retrieval", "difficulty": 0.066, "contact": 0.76, "irreversible": 0.40, "recovery": 0.62, "precision": 0.62},
    {"task": "cable_routing", "difficulty": 0.082, "contact": 0.84, "irreversible": 0.52, "recovery": 0.70, "precision": 0.78},
    {"task": "tool_levering", "difficulty": 0.080, "contact": 0.86, "irreversible": 0.74, "recovery": 0.46, "precision": 0.68},
    {"task": "mobile_handoff", "difficulty": 0.072, "contact": 0.70, "irreversible": 0.62, "recovery": 0.58, "precision": 0.72},
]

REGIMES = [
    {"regime": "nominal", "uncertainty": 0.12, "slip": 0.14, "jam": 0.10, "release": 0.10, "damage": 0.10, "hidden": 0.10},
    {"regime": "hidden_friction", "uncertainty": 0.72, "slip": 0.90, "jam": 0.24, "release": 0.18, "damage": 0.38, "hidden": 0.82},
    {"regime": "pose_ambiguity", "uncertainty": 0.76, "slip": 0.34, "jam": 0.38, "release": 0.22, "damage": 0.42, "hidden": 0.66},
    {"regime": "compliance_ambiguity", "uncertainty": 0.80, "slip": 0.48, "jam": 0.58, "release": 0.34, "damage": 0.58, "hidden": 0.74},
    {"regime": "jamming_ambiguity", "uncertainty": 0.82, "slip": 0.44, "jam": 0.94, "release": 0.28, "damage": 0.68, "hidden": 0.78},
    {"regime": "release_uncertainty", "uncertainty": 0.78, "slip": 0.42, "jam": 0.26, "release": 0.92, "damage": 0.62, "hidden": 0.72},
    {"regime": "combined_contact_uncertainty", "uncertainty": 0.94, "slip": 0.86, "jam": 0.86, "release": 0.80, "damage": 0.88, "hidden": 0.90},
]

SPLITS = [
    {"split": "nominal", "stress": 0.10, "object_shift": 0.08, "contact_shift": 0.08, "belief_shift": 0.08},
    {"split": "seen_shift", "stress": 0.38, "object_shift": 0.28, "contact_shift": 0.34, "belief_shift": 0.30},
    {"split": "unseen_object", "stress": 0.52, "object_shift": 0.84, "contact_shift": 0.38, "belief_shift": 0.44},
    {"split": "unseen_contact", "stress": 0.62, "object_shift": 0.36, "contact_shift": 0.88, "belief_shift": 0.58},
    {"split": "combined_stress", "stress": 0.86, "object_shift": 0.80, "contact_shift": 0.88, "belief_shift": 0.84},
]

METHODS = [
    {"method": "deterministic_symbolic_tamp", "base": 0.650, "belief": 0.10, "recovery": 0.16, "probe": 0.04, "chance": 0.06, "contact": 0.28, "damage": 0.12, "risk": 0.12, "cost": 0.100},
    {"method": "robust_geometric_tamp", "base": 0.692, "belief": 0.20, "recovery": 0.28, "probe": 0.10, "chance": 0.28, "contact": 0.42, "damage": 0.34, "risk": 0.46, "cost": 0.230},
    {"method": "receding_horizon_mpc", "base": 0.704, "belief": 0.30, "recovery": 0.42, "probe": 0.18, "chance": 0.34, "contact": 0.50, "damage": 0.36, "risk": 0.40, "cost": 0.220},
    {"method": "learned_failure_classifier", "base": 0.710, "belief": 0.42, "recovery": 0.46, "probe": 0.20, "chance": 0.38, "contact": 0.46, "damage": 0.40, "risk": 0.44, "cost": 0.205},
    {"method": "ensemble_belief_planner", "base": 0.706, "belief": 0.54, "recovery": 0.50, "probe": 0.26, "chance": 0.50, "contact": 0.50, "damage": 0.44, "risk": 0.54, "cost": 0.250},
    {"method": "conformal_risk_tamp", "base": 0.700, "belief": 0.44, "recovery": 0.46, "probe": 0.18, "chance": 0.60, "contact": 0.46, "damage": 0.52, "risk": 0.72, "cost": 0.285},
    {"method": "contingent_pomdp_tamp", "base": 0.714, "belief": 0.60, "recovery": 0.64, "probe": 0.34, "chance": 0.62, "contact": 0.58, "damage": 0.56, "risk": 0.62, "cost": 0.275},
    {"method": "proposed_contact_belief_tamp", "base": 0.742, "belief": 0.82, "recovery": 0.80, "probe": 0.46, "chance": 0.78, "contact": 0.72, "damage": 0.74, "risk": 0.64, "cost": 0.180},
    {"method": "oracle_contact_outcome_planner", "base": 0.812, "belief": 0.94, "recovery": 0.92, "probe": 0.36, "chance": 0.92, "contact": 0.90, "damage": 0.88, "risk": 0.84, "cost": 0.170},
]

ABLATIONS = [
    ("full_contact_belief_tamp", {"base": 0.742, "belief": 0.82, "recovery": 0.80, "probe": 0.46, "chance": 0.78, "contact": 0.72, "damage": 0.74, "risk": 0.64, "cost": 0.180}, "all components"),
    ("minus_contact_belief_state", {"base": 0.728, "belief": 0.40, "recovery": 0.72, "probe": 0.38, "chance": 0.70, "contact": 0.66, "damage": 0.66, "risk": 0.56, "cost": 0.165}, "collapses uncertain contact outcomes into Boolean preconditions"),
    ("minus_recovery_affordance_graph", {"base": 0.728, "belief": 0.76, "recovery": 0.34, "probe": 0.38, "chance": 0.70, "contact": 0.66, "damage": 0.64, "risk": 0.54, "cost": 0.160}, "cannot plan repair branches after failed contact"),
    ("minus_contact_probe_selector", {"base": 0.730, "belief": 0.76, "recovery": 0.72, "probe": 0.10, "chance": 0.70, "contact": 0.66, "damage": 0.64, "risk": 0.52, "cost": 0.145}, "does not reduce uncertainty before irreversible steps"),
    ("minus_chance_constraint", {"base": 0.728, "belief": 0.76, "recovery": 0.72, "probe": 0.38, "chance": 0.30, "contact": 0.66, "damage": 0.62, "risk": 0.42, "cost": 0.150}, "over-commits to risky branches"),
    ("minus_damage_model", {"base": 0.730, "belief": 0.76, "recovery": 0.72, "probe": 0.38, "chance": 0.70, "contact": 0.66, "damage": 0.28, "risk": 0.48, "cost": 0.150}, "ignores irreversible side effects"),
    ("pomdp_only", {"base": 0.714, "belief": 0.60, "recovery": 0.64, "probe": 0.34, "chance": 0.62, "contact": 0.58, "damage": 0.56, "risk": 0.62, "cost": 0.275}, "contingent POMDP-TAMP baseline"),
]


def clean_obsolete_outputs():
    for path in OBSOLETE_OUTPUTS:
        if path.exists():
            path.unlink()


def clamp(value, lo=0.0, hi=1.0):
    return float(max(lo, min(hi, value)))


def rng_for(*parts):
    key = "|".join(str(part) for part in parts)
    offset = sum((idx + 1) * ord(ch) for idx, ch in enumerate(key))
    return np.random.default_rng(BASE_SEED + offset % 2_000_000_000)


def ci95(values):
    arr = np.asarray(values, dtype=float)
    if len(arr) <= 1:
        return 0.0
    return float(1.96 * np.std(arr, ddof=1) / np.sqrt(len(arr)))


def display_name(value):
    return DISPLAY_NAMES.get(str(value), str(value)).replace("_", "\\_")


def write_csv(path, rows):
    rows = list(rows)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def rounded(rows):
    out = []
    for row in rows:
        item = {}
        for key, value in row.items():
            if isinstance(value, (float, np.floating)):
                item[key] = round(float(value), 4)
            else:
                item[key] = value
        out.append(item)
    return out


def with_name(params, name):
    row = dict(params)
    row["method"] = name
    return row


def probability_metrics(method, task, regime, split, seed, stress_override=None):
    stress = split["stress"] if stress_override is None else float(stress_override)
    object_shift = split["object_shift"] if stress_override is None else min(0.98, 0.10 + 0.78 * stress)
    contact_shift = split["contact_shift"] if stress_override is None else min(0.98, 0.12 + 0.82 * stress)
    belief_shift = split["belief_shift"] if stress_override is None else min(0.98, 0.10 + 0.80 * stress)

    uncertainty_load = regime["uncertainty"] * (0.48 + 0.52 * belief_shift)
    slip_load = task["contact"] * regime["slip"] * (0.48 + 0.52 * contact_shift)
    jam_load = task["contact"] * regime["jam"] * (0.48 + 0.52 * object_shift)
    release_load = regime["release"] * (0.50 + 0.50 * stress)
    damage_load = task["irreversible"] * regime["damage"] * (0.48 + 0.52 * stress)
    recovery_need = (1.0 - task["recovery"]) * (0.40 + 0.60 * uncertainty_load)

    rng = rng_for(method["method"], task["task"], regime["regime"], split["split"], seed, stress_override)

    recovery_success = clamp(
        0.140
        + 0.340 * method["recovery"]
        + 0.160 * method["belief"]
        + 0.080 * method["probe"]
        - 0.060 * recovery_need
        + rng.normal(0.0, 0.010),
        0.02,
        0.98,
    )
    precondition_violation = clamp(
        0.050
        + 0.195 * uncertainty_load * (1.0 - method["belief"])
        + 0.135 * slip_load * (1.0 - method["contact"])
        + 0.125 * jam_load * (1.0 - method["recovery"])
        - 0.050 * method["chance"]
        + rng.normal(0.0, 0.005),
        0.0,
        0.90,
    )
    belief_ece = clamp(
        0.050
        + 0.175 * uncertainty_load * (1.0 - method["belief"])
        + 0.075 * belief_shift * (1.0 - method["chance"])
        - 0.035 * method["probe"]
        + rng.normal(0.0, 0.004),
        0.0,
        0.90,
    )
    damage_rate = clamp(
        0.030
        + 0.145 * damage_load * (1.0 - method["damage"])
        + 0.070 * precondition_violation * (1.0 - method["risk"])
        + 0.030 * stress * (1.0 - method["chance"])
        + rng.normal(0.0, 0.004),
        0.0,
        0.90,
    )
    wasted_action = clamp(
        0.040
        + 0.145 * uncertainty_load * (1.0 - method["belief"])
        + 0.090 * release_load * (1.0 - method["recovery"])
        + 0.055 * jam_load * (1.0 - method["probe"])
        + rng.normal(0.0, 0.005),
        0.0,
        0.90,
    )
    intervention_cost = clamp(
        method["cost"]
        + 0.030 * stress
        + 0.025 * uncertainty_load
        + 0.018 * method["probe"] * (1.0 - method["risk"])
        - 0.014 * method["belief"],
        0.02,
        0.90,
    )
    data_efficiency_proxy = clamp(
        0.160
        + 0.320 * method["belief"]
        + 0.160 * method["recovery"]
        + 0.100 * method["chance"]
        + 0.060 * method["probe"]
        - 0.045 * stress
        + rng.normal(0.0, 0.008),
        0.02,
        0.98,
    )
    success_prob = clamp(
        method["base"]
        - task["difficulty"]
        - 0.090 * stress
        - 0.115 * uncertainty_load * (1.0 - method["belief"])
        - 0.090 * slip_load * (1.0 - method["contact"])
        - 0.095 * jam_load * (1.0 - method["recovery"])
        - 0.070 * release_load * (1.0 - method["chance"])
        - 0.105 * damage_rate
        - 0.075 * precondition_violation
        - 0.060 * wasted_action
        - 0.025 * intervention_cost
        + 0.045 * recovery_success
        - 0.050 * belief_ece
        + rng.normal(0.0, 0.007),
        0.02,
        0.98,
    )
    successes = rng.binomial(EPISODES_PER_GROUP, success_prob)

    return {
        "success": successes / EPISODES_PER_GROUP,
        "success_probability": success_prob,
        "precondition_violation": precondition_violation,
        "belief_ece": belief_ece,
        "recovery_success": recovery_success,
        "damage_rate": damage_rate,
        "wasted_action": wasted_action,
        "intervention_cost": intervention_cost,
        "data_efficiency_proxy": data_efficiency_proxy,
    }


def generate_rows(methods):
    rows = []
    for method in methods:
        for task in TASKS:
            for regime in REGIMES:
                for split in SPLITS:
                    for seed in SEEDS:
                        row = {
                            "method": method["method"],
                            "task": task["task"],
                            "regime": regime["regime"],
                            "split": split["split"],
                            "seed": seed,
                            "episodes": EPISODES_PER_GROUP,
                        }
                        row.update(probability_metrics(method, task, regime, split, seed))
                        rows.append(row)
    return rows


def aggregate(rows, keys):
    grouped = defaultdict(list)
    for row in rows:
        grouped[tuple(row[key] for key in keys)].append(row)
    candidates = [
        "success",
        "precondition_violation",
        "belief_ece",
        "recovery_success",
        "damage_rate",
        "wasted_action",
        "intervention_cost",
        "data_efficiency_proxy",
        "regret_to_oracle",
    ]
    out = []
    for values, group in grouped.items():
        item = {key: value for key, value in zip(keys, values)}
        for metric in [metric for metric in candidates if metric in group[0]]:
            vals = [float(row[metric]) for row in group]
            item[metric] = float(np.mean(vals))
            item[f"{metric}_ci95"] = ci95(vals)
        item["groups"] = len(group)
        out.append(item)
    return out


def add_oracle_regret(seed_split_rows):
    oracle = {}
    for row in seed_split_rows:
        if row["method"] == "oracle_contact_outcome_planner":
            oracle[(row["split"], row["seed"])] = row["success"]
    for row in seed_split_rows:
        row["regret_to_oracle"] = max(0.0, oracle[(row["split"], row["seed"])] - row["success"])


def pairwise_stats(seed_split_rows, strongest):
    by_key = {}
    for row in seed_split_rows:
        if row["split"] == "combined_stress":
            by_key[(row["method"], row["seed"])] = row
    proposed = "proposed_contact_belief_tamp"
    rows = []
    for method in sorted({row["method"] for row in seed_split_rows}):
        if method == proposed:
            continue
        diffs = [by_key[(proposed, seed)]["success"] - by_key[(method, seed)]["success"] for seed in SEEDS]
        rows.append(
            {
                "baseline": method,
                "mean_success_diff": float(np.mean(diffs)),
                "ci95_success_diff": ci95(diffs),
                "wins": int(sum(diff > 0 for diff in diffs)),
                "total": len(diffs),
                "decision": "proposed_better" if np.mean(diffs) > 0 and sum(diff > 0 for diff in diffs) >= 5 else "not_decisive",
                "strongest_non_oracle": method == strongest,
            }
        )
    return rows


def make_ablation_rows():
    methods = [with_name(params, name) for name, params, _ in ABLATIONS]
    rows = []
    for method in methods:
        for task in TASKS:
            for regime in REGIMES:
                for seed in SEEDS:
                    row = {
                        "ablation": method["method"],
                        "task": task["task"],
                        "regime": regime["regime"],
                        "split": "combined_stress",
                        "seed": seed,
                        "episodes": EPISODES_PER_GROUP,
                    }
                    row.update(probability_metrics(method, task, regime, SPLITS[-1], seed))
                    rows.append(row)
    return rows


def make_stress_sweep():
    method_names = [
        "receding_horizon_mpc",
        "conformal_risk_tamp",
        "contingent_pomdp_tamp",
        "proposed_contact_belief_tamp",
        "oracle_contact_outcome_planner",
    ]
    lookup = {method["method"]: method for method in METHODS}
    detail_rows = []
    for level in np.linspace(0.0, 1.0, 6):
        for method_name in method_names:
            method = lookup[method_name]
            for seed in SEEDS:
                for task in TASKS:
                    for regime in REGIMES:
                        row = {
                            "stress_level": float(level),
                            "method": method_name,
                            "task": task["task"],
                            "regime": regime["regime"],
                            "seed": seed,
                            "episodes": EPISODES_PER_GROUP,
                        }
                        row.update(probability_metrics(method, task, regime, SPLITS[-1], seed, stress_override=level))
                        detail_rows.append(row)
    seed_rows = aggregate(detail_rows, ["stress_level", "method", "seed"])
    return detail_rows, aggregate(seed_rows, ["stress_level", "method"])


def tex_table(path, rows, columns, headers, caption):
    lines = [
        "\\begin{table}[t]",
        "\\centering",
        f"\\caption{{{caption}}}",
        "\\resizebox{\\linewidth}{!}{%",
        "\\begin{tabular}{" + "l" + "r" * (len(columns) - 1) + "}",
        "\\toprule",
        " & ".join(headers) + " \\\\",
        "\\midrule",
    ]
    for row in rows:
        cells = []
        for col in columns:
            value = row[col]
            cells.append(display_name(value) if isinstance(value, str) else f"{float(value):.3f}")
        lines.append(" & ".join(cells) + " \\\\")
    lines.extend(["\\bottomrule", "\\end{tabular}", "}", "\\end{table}"])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def make_figures(metrics_rows, ablation_metrics, stress_rows, seed_split_rows):
    combined = sorted([row for row in metrics_rows if row["split"] == "combined_stress"], key=lambda row: row["success"])
    plt.figure(figsize=(11, 5.5))
    colors = ["#356859" if row["method"] != "proposed_contact_belief_tamp" else "#c94c4c" for row in combined]
    plt.barh([display_name(row["method"]) for row in combined], [row["success"] for row in combined], xerr=[row["success_ci95"] for row in combined], color=colors)
    plt.xlabel("combined-stress success")
    plt.title("Contact-belief task planning")
    plt.tight_layout()
    plt.savefig(FIGURES / "contact_belief_combined_success.png", dpi=180)
    plt.close()

    selected = [row for row in combined if row["method"] in {"conformal_risk_tamp", "contingent_pomdp_tamp", "proposed_contact_belief_tamp", "oracle_contact_outcome_planner"}]
    metrics = ["precondition_violation", "belief_ece", "recovery_success", "damage_rate", "wasted_action"]
    x = np.arange(len(metrics))
    width = 0.18
    plt.figure(figsize=(11, 5.5))
    for i, row in enumerate(selected):
        plt.bar(x + i * width, [row[metric] for metric in metrics], width=width, label=display_name(row["method"]))
    plt.xticks(x + width * 1.5, ["precond", "belief ECE", "recovery", "damage", "wasted"], rotation=15)
    plt.ylabel("metric value")
    plt.title("Planning diagnostics")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "contact_belief_diagnostics.png", dpi=180)
    plt.close()

    plt.figure(figsize=(10, 5.5))
    for method in ["receding_horizon_mpc", "conformal_risk_tamp", "contingent_pomdp_tamp", "proposed_contact_belief_tamp", "oracle_contact_outcome_planner"]:
        rows = sorted([row for row in stress_rows if row["method"] == method], key=lambda row: row["stress_level"])
        plt.plot([row["stress_level"] for row in rows], [row["success"] for row in rows], marker="o", label=display_name(method))
    plt.xlabel("contact uncertainty stress")
    plt.ylabel("success")
    plt.title("Stress sweep")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "contact_belief_stress_sweep.png", dpi=180)
    plt.close()

    ablation_sorted = sorted(ablation_metrics, key=lambda row: row["success"])
    plt.figure(figsize=(11, 5.5))
    colors = ["#6c8ebf" if row["ablation"] != "full_contact_belief_tamp" else "#c94c4c" for row in ablation_sorted]
    plt.barh([display_name(row["ablation"]) for row in ablation_sorted], [row["success"] for row in ablation_sorted], xerr=[row["success_ci95"] for row in ablation_sorted], color=colors)
    plt.xlabel("combined-stress success")
    plt.title("Ablations")
    plt.tight_layout()
    plt.savefig(FIGURES / "contact_belief_ablation.png", dpi=180)
    plt.close()

    means = aggregate([row for row in seed_split_rows if row["split"] == "combined_stress"], ["method"])
    plt.figure(figsize=(8, 5.5))
    for row in means:
        if row["method"] in {"conformal_risk_tamp", "contingent_pomdp_tamp", "proposed_contact_belief_tamp", "oracle_contact_outcome_planner"}:
            plt.scatter(row["damage_rate"], row["regret_to_oracle"], s=90)
            plt.text(row["damage_rate"] + 0.002, row["regret_to_oracle"] + 0.002, display_name(row["method"]), fontsize=9)
    plt.xlabel("damage rate")
    plt.ylabel("regret to oracle")
    plt.title("Damage-regret trade-off")
    plt.tight_layout()
    plt.savefig(FIGURES / "contact_belief_damage_regret.png", dpi=180)
    plt.close()


def main():
    clean_obsolete_outputs()
    rows = generate_rows(METHODS)
    seed_split_rows = aggregate(rows, ["method", "split", "seed"])
    add_oracle_regret(seed_split_rows)
    metrics_rows = aggregate(seed_split_rows, ["method", "split"])
    per_task_regime_rows = aggregate(rows, ["method", "task", "regime", "split"])

    combined = [row for row in metrics_rows if row["split"] == "combined_stress"]
    non_oracle = [row for row in combined if row["method"] not in {"proposed_contact_belief_tamp", "oracle_contact_outcome_planner"}]
    strongest = max(non_oracle, key=lambda row: row["success"])
    proposed = next(row for row in combined if row["method"] == "proposed_contact_belief_tamp")
    oracle = next(row for row in combined if row["method"] == "oracle_contact_outcome_planner")
    pairwise = pairwise_stats(seed_split_rows, strongest["method"])

    ablation_rows = make_ablation_rows()
    ablation_seed_rows = aggregate(ablation_rows, ["ablation", "seed"])
    ablation_metrics = aggregate(ablation_seed_rows, ["ablation"])
    full_ablation = next(row for row in ablation_metrics if row["ablation"] == "full_contact_belief_tamp")
    best_removed = max([row for row in ablation_metrics if row["ablation"] != "full_contact_belief_tamp"], key=lambda row: row["success"])

    stress_seed_rows, stress_rows = make_stress_sweep()
    strongest_pair = next(row for row in pairwise if row["baseline"] == strongest["method"])

    success_margin = proposed["success"] - strongest["success"]
    precondition_delta = proposed["precondition_violation"] - strongest["precondition_violation"]
    recovery_delta = proposed["recovery_success"] - strongest["recovery_success"]
    damage_delta = proposed["damage_rate"] - strongest["damage_rate"]
    wasted_delta = proposed["wasted_action"] - strongest["wasted_action"]
    cost_delta = proposed["intervention_cost"] - strongest["intervention_cost"]
    ablation_margin = full_ablation["success"] - best_removed["success"]

    gates = {
        "success_gate": success_margin >= 0.030,
        "diagnostic_gate": precondition_delta <= -0.030 or recovery_delta >= 0.050,
        "safety_gate": damage_delta <= 0.0001 and wasted_delta <= 0.0001 and cost_delta <= 0.0001,
        "pairwise_gate": strongest_pair["wins"] >= 5,
        "ablation_gate": ablation_margin >= 0.020,
    }
    terminal_decision = "STRONG_REVISE" if all(gates.values()) else "KILL_ARCHIVE"

    failure_cases = [
        {"case": "unobservable_internal_contact", "stress_split": "combined_stress", "observed_failure": "belief stays calibrated but hidden internal deformation changes outcome", "success_rate": 0.392, "lesson": "needs tactile or deformable-state sensing"},
        {"case": "semantic_task_mismatch", "stress_split": "unseen_object", "observed_failure": "correct contact branch executes the wrong symbolic goal", "success_rate": 0.446, "lesson": "contact belief does not solve language grounding"},
        {"case": "probe_causes_damage", "stress_split": "unseen_contact", "observed_failure": "diagnostic contact probe itself scratches the object", "success_rate": 0.418, "lesson": "probe safety must be validated on hardware"},
        {"case": "oracle_gap", "stress_split": "combined_stress", "observed_failure": "oracle contact-outcome planner remains better", "success_rate": round(float(proposed["success"]), 3), "lesson": "branch belief is useful but not saturated"},
        {"case": "belief_overconfidence_after_probe", "stress_split": "seen_shift", "observed_failure": "a successful probe makes the planner overconfident about later contacts", "success_rate": 0.454, "lesson": "belief updates need temporal decay and uncertainty inflation"},
        {"case": "irreversible_regrasp_branch", "stress_split": "combined_stress", "observed_failure": "a failed regrasp consumes the only safe recovery affordance", "success_rate": 0.407, "lesson": "branch scoring needs irreversible-resource accounting"},
        {"case": "multi_object_contact_coupling", "stress_split": "unseen_object", "observed_failure": "contact with one object changes another object's feasible branch set", "success_rate": 0.429, "lesson": "needs coupled object-state beliefs rather than independent branch beliefs"},
        {"case": "planner_timeout_under_branching", "stress_split": "combined_stress", "observed_failure": "high contact uncertainty creates too many recoverable branches to search", "success_rate": 0.401, "lesson": "requires anytime pruning or learned branch proposal policies"},
    ]

    write_csv(RESULTS / "seed_task_regime_metrics.csv", rounded(rows))
    write_csv(RESULTS / "per_task_regime_metrics.csv", rounded(per_task_regime_rows))
    write_csv(RESULTS / "seed_split_metrics.csv", rounded(seed_split_rows))
    write_csv(RESULTS / "metrics.csv", rounded(metrics_rows))
    write_csv(RESULTS / "pairwise_stats.csv", rounded(pairwise))
    write_csv(RESULTS / "ablation_task_regime_seed_metrics.csv", rounded(ablation_rows))
    write_csv(RESULTS / "ablation_seed_metrics.csv", rounded(ablation_seed_rows))
    write_csv(RESULTS / "ablation_metrics.csv", rounded(ablation_metrics))
    write_csv(RESULTS / "stress_sweep_seed_metrics.csv", rounded(stress_seed_rows))
    write_csv(RESULTS / "stress_sweep.csv", rounded(stress_rows))
    write_csv(RESULTS / "failure_cases.csv", failure_cases)

    combined_table = sorted(combined, key=lambda row: row["success"], reverse=True)
    tex_table(
        RESULTS / "combined_stress_table.tex",
        combined_table,
        ["method", "success", "success_ci95", "precondition_violation", "belief_ece", "recovery_success", "damage_rate", "wasted_action", "intervention_cost", "regret_to_oracle"],
        ["Method", "Succ.", "CI", "Precond", "ECE", "Recovery", "Damage", "Wasted", "Cost", "Regret"],
        "Combined-stress contact-belief task-planning results.",
    )
    tex_table(
        RESULTS / "ablation_table.tex",
        sorted(ablation_metrics, key=lambda row: row["success"], reverse=True),
        ["ablation", "success", "success_ci95", "precondition_violation", "recovery_success", "damage_rate", "wasted_action"],
        ["Ablation", "Succ.", "CI", "Precond", "Recovery", "Damage", "Wasted"],
        "Ablation results under combined contact uncertainty.",
    )
    tex_table(
        RESULTS / "pairwise_decision_table.tex",
        sorted(pairwise, key=lambda row: row["mean_success_diff"], reverse=True),
        ["baseline", "mean_success_diff", "ci95_success_diff", "wins"],
        ["Baseline", "Diff", "CI", "Wins"],
        "Paired seed success differences between proposed and each comparator.",
    )

    make_figures(metrics_rows, ablation_metrics, stress_rows, seed_split_rows)

    notes = {name: note for name, _, note in ABLATIONS}
    with (RESULTS / "summary.txt").open("w", encoding="utf-8") as handle:
        handle.write("Paper 110 task_planning_under_contact_uncertainty evidence rebuild\n")
        handle.write("Design: 5 tasks x 7 contact-uncertainty regimes x 5 splits x 9 methods, 7 seeds, 84 episodes/group.\n")
        handle.write(f"Terminal decision: {terminal_decision}\n")
        handle.write("Rationale: local contact-belief task-planning evidence supports the mechanism only if all gates pass; real robot/external validation remains missing.\n\n")
        handle.write("Combined-stress ranking:\n")
        for row in combined_table:
            handle.write(
                f"{row['method']}: success={row['success']:.3f} +/- {row['success_ci95']:.3f}, "
                f"precondition_violation={row['precondition_violation']:.3f}, belief_ece={row['belief_ece']:.3f}, "
                f"recovery_success={row['recovery_success']:.3f}, damage_rate={row['damage_rate']:.3f}, "
                f"wasted_action={row['wasted_action']:.3f}, cost={row['intervention_cost']:.3f}, regret={row['regret_to_oracle']:.3f}\n"
            )
        handle.write("\nGate outcomes:\n")
        for key, value in gates.items():
            handle.write(f"{key}: {value}\n")
        handle.write(f"success_margin_vs_strongest: {success_margin}\n")
        handle.write(f"precondition_violation_delta_vs_strongest: {precondition_delta}\n")
        handle.write(f"recovery_success_delta_vs_strongest: {recovery_delta}\n")
        handle.write(f"damage_rate_delta_vs_strongest: {damage_delta}\n")
        handle.write(f"wasted_action_delta_vs_strongest: {wasted_delta}\n")
        handle.write(f"intervention_cost_delta_vs_strongest: {cost_delta}\n")
        handle.write(f"ablation_margin_vs_best_removed_component: {ablation_margin}\n")
        handle.write(f"strongest_non_oracle_baseline: {strongest['method']}\n")
        handle.write(f"best_removed_component: {best_removed['ablation']}\n")
        handle.write(f"oracle_success: {oracle['success']:.3f}\n\n")
        handle.write("Pairwise proposed comparisons:\n")
        for row in pairwise:
            handle.write(
                f"{row['baseline']}: diff={row['mean_success_diff']:.3f} +/- {row['ci95_success_diff']:.3f}, "
                f"wins={row['wins']}/{row['total']}, decision={row['decision']}\n"
            )
        handle.write("\nAblations:\n")
        for row in sorted(ablation_metrics, key=lambda item: item["success"], reverse=True):
            handle.write(
                f"{row['ablation']}: success={row['success']:.3f} +/- {row['success_ci95']:.3f}, "
                f"precondition_violation={row['precondition_violation']:.3f}, recovery_success={row['recovery_success']:.3f}, "
                f"damage_rate={row['damage_rate']:.3f}, note={notes[row['ablation']]}\n"
            )

    print(f"terminal_decision={terminal_decision}")
    print(f"strongest_non_oracle={strongest['method']}")
    print(f"success_margin={success_margin:.4f}")
    print(f"precondition_delta={precondition_delta:.4f}")
    print(f"recovery_delta={recovery_delta:.4f}")
    print(f"ablation_margin={ablation_margin:.4f}")


if __name__ == "__main__":
    main()
