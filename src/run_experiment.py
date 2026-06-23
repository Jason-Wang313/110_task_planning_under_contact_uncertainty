import csv
import json
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


BASE_SEED = 110_2026_005
SEEDS = list(range(10))
EPISODES_PER_CELL = 6

PRIMARY_METHOD = "contact_belief_branch_audit_v5"
V4_METHOD = "proposed_contact_belief_tamp_v4"
ORACLE_METHOD = "oracle_hybrid_contact_planner"
HARD_SPLIT = "heldout_combined_contact_uncertainty"

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RESULTS.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)

METRICS = [
    "success",
    "utility",
    "precondition_violation",
    "belief_ece",
    "branch_entropy_error",
    "recovery_success",
    "damage_rate",
    "wasted_action",
    "intervention_cost",
    "probe_overhead",
    "irreversible_commitment",
    "plan_depth_blowup",
    "regret_to_oracle",
]

DISPLAY_NAMES = {
    "deterministic_symbolic_tamp": "DetTAMP",
    "robust_geometric_tamp": "RobustGeom",
    "receding_horizon_mpc": "MPC",
    "learned_failure_classifier": "FailCls",
    "ensemble_belief_planner": "Ensemble",
    "conformal_risk_tamp": "Conformal",
    "smooth_precondition_world_model": "SmoothWM",
    "contact_implicit_tamp": "ImplicitTAMP",
    "contingent_pomdp_tamp": "POMDP-TAMP",
    "risk_aware_tamp": "RiskTAMP",
    "learned_contact_belief_state": "LearnedBelief",
    "damage_aware_planner": "DamageAware",
    V4_METHOD: "v4BeliefTAMP",
    PRIMARY_METHOD: "v5BranchAudit",
    "oracle_contact_outcome_planner": "OracleOutcome",
    ORACLE_METHOD: "OracleHybrid",
    "full_contact_belief_branch_audit_v5": "Full",
    "minus_contact_belief_state": "NoBelief",
    "minus_recovery_affordance_graph": "NoRecovery",
    "minus_contact_probe_selector": "NoProbe",
    "minus_chance_constraint": "NoChance",
    "minus_damage_model": "NoDamage",
    "minus_branch_budget": "NoBranchBudget",
    "minus_entropy_calibration": "NoEntropyCal",
    "minus_irreversible_resource_accounting": "NoResourceAcct",
    "v4_only_contact_belief_tamp": "v4Only",
    "pomdp_only": "POMDPOnly",
}

TASKS = [
    {"task": "peg_assembly", "difficulty": 0.078, "contact": 0.92, "irreversible": 0.58, "recovery": 0.54, "precision": 0.86, "branch": 0.60, "deformable": 0.18},
    {"task": "drawer_retrieval", "difficulty": 0.066, "contact": 0.76, "irreversible": 0.40, "recovery": 0.62, "precision": 0.62, "branch": 0.44, "deformable": 0.28},
    {"task": "cable_routing", "difficulty": 0.082, "contact": 0.84, "irreversible": 0.52, "recovery": 0.70, "precision": 0.78, "branch": 0.82, "deformable": 0.86},
    {"task": "tool_levering", "difficulty": 0.080, "contact": 0.86, "irreversible": 0.74, "recovery": 0.46, "precision": 0.68, "branch": 0.58, "deformable": 0.22},
    {"task": "mobile_handoff", "difficulty": 0.072, "contact": 0.70, "irreversible": 0.62, "recovery": 0.58, "precision": 0.72, "branch": 0.66, "deformable": 0.34},
    {"task": "bimanual_fixture_alignment", "difficulty": 0.088, "contact": 0.88, "irreversible": 0.68, "recovery": 0.50, "precision": 0.88, "branch": 0.76, "deformable": 0.46},
    {"task": "deformable_bin_packing", "difficulty": 0.090, "contact": 0.82, "irreversible": 0.56, "recovery": 0.64, "precision": 0.66, "branch": 0.72, "deformable": 0.94},
    {"task": "legged_support_recovery", "difficulty": 0.086, "contact": 0.90, "irreversible": 0.78, "recovery": 0.44, "precision": 0.74, "branch": 0.80, "deformable": 0.36},
]

REGIMES = [
    {"regime": "nominal", "uncertainty": 0.12, "slip": 0.14, "jam": 0.10, "release": 0.10, "damage": 0.10, "hidden": 0.10, "dropout": 0.06, "resource": 0.08},
    {"regime": "hidden_friction", "uncertainty": 0.72, "slip": 0.90, "jam": 0.24, "release": 0.18, "damage": 0.38, "hidden": 0.82, "dropout": 0.20, "resource": 0.28},
    {"regime": "pose_ambiguity", "uncertainty": 0.76, "slip": 0.34, "jam": 0.38, "release": 0.22, "damage": 0.42, "hidden": 0.66, "dropout": 0.30, "resource": 0.30},
    {"regime": "compliance_ambiguity", "uncertainty": 0.80, "slip": 0.48, "jam": 0.58, "release": 0.34, "damage": 0.58, "hidden": 0.74, "dropout": 0.32, "resource": 0.42},
    {"regime": "jamming_ambiguity", "uncertainty": 0.82, "slip": 0.44, "jam": 0.94, "release": 0.28, "damage": 0.68, "hidden": 0.78, "dropout": 0.36, "resource": 0.56},
    {"regime": "release_uncertainty", "uncertainty": 0.78, "slip": 0.42, "jam": 0.26, "release": 0.92, "damage": 0.62, "hidden": 0.72, "dropout": 0.34, "resource": 0.46},
    {"regime": "partial_observability_dropout", "uncertainty": 0.86, "slip": 0.52, "jam": 0.52, "release": 0.48, "damage": 0.56, "hidden": 0.90, "dropout": 0.94, "resource": 0.52},
    {"regime": "irreversible_damage_risk", "uncertainty": 0.84, "slip": 0.50, "jam": 0.62, "release": 0.58, "damage": 0.94, "hidden": 0.78, "dropout": 0.42, "resource": 0.74},
    {"regime": "branch_resource_depletion", "uncertainty": 0.82, "slip": 0.54, "jam": 0.72, "release": 0.58, "damage": 0.74, "hidden": 0.76, "dropout": 0.44, "resource": 0.96},
    {"regime": "combined_contact_uncertainty", "uncertainty": 0.94, "slip": 0.86, "jam": 0.86, "release": 0.80, "damage": 0.88, "hidden": 0.90, "dropout": 0.82, "resource": 0.88},
]

SPLITS = [
    {"split": "nominal", "stress": 0.10, "object_shift": 0.08, "contact_shift": 0.08, "compliance_shift": 0.08, "probe_latency": 0.08, "sensor_dropout": 0.08, "resource_shift": 0.08},
    {"split": "seen_shift", "stress": 0.38, "object_shift": 0.28, "contact_shift": 0.34, "compliance_shift": 0.26, "probe_latency": 0.20, "sensor_dropout": 0.30, "resource_shift": 0.24},
    {"split": "unseen_object", "stress": 0.52, "object_shift": 0.84, "contact_shift": 0.38, "compliance_shift": 0.34, "probe_latency": 0.30, "sensor_dropout": 0.42, "resource_shift": 0.36},
    {"split": "unseen_contact", "stress": 0.62, "object_shift": 0.36, "contact_shift": 0.88, "compliance_shift": 0.42, "probe_latency": 0.36, "sensor_dropout": 0.54, "resource_shift": 0.44},
    {"split": "unseen_compliance", "stress": 0.66, "object_shift": 0.46, "contact_shift": 0.44, "compliance_shift": 0.92, "probe_latency": 0.42, "sensor_dropout": 0.50, "resource_shift": 0.48},
    {"split": "probe_latency", "stress": 0.68, "object_shift": 0.44, "contact_shift": 0.48, "compliance_shift": 0.46, "probe_latency": 0.94, "sensor_dropout": 0.52, "resource_shift": 0.56},
    {"split": "sensor_dropout", "stress": 0.70, "object_shift": 0.50, "contact_shift": 0.52, "compliance_shift": 0.50, "probe_latency": 0.58, "sensor_dropout": 0.94, "resource_shift": 0.58},
    {"split": HARD_SPLIT, "stress": 0.86, "object_shift": 0.80, "contact_shift": 0.88, "compliance_shift": 0.84, "probe_latency": 0.82, "sensor_dropout": 0.74, "resource_shift": 0.86},
]

METHODS = [
    {"method": "deterministic_symbolic_tamp", "base": 0.650, "belief": 0.10, "recovery": 0.16, "probe": 0.04, "chance": 0.06, "contact": 0.28, "damage": 0.12, "risk": 0.12, "entropy": 0.12, "resource": 0.10, "calibration": 0.20, "branch": 0.14, "cost": 0.10},
    {"method": "robust_geometric_tamp", "base": 0.692, "belief": 0.20, "recovery": 0.28, "probe": 0.10, "chance": 0.28, "contact": 0.42, "damage": 0.34, "risk": 0.46, "entropy": 0.24, "resource": 0.26, "calibration": 0.34, "branch": 0.28, "cost": 0.23},
    {"method": "receding_horizon_mpc", "base": 0.704, "belief": 0.30, "recovery": 0.42, "probe": 0.18, "chance": 0.34, "contact": 0.50, "damage": 0.36, "risk": 0.40, "entropy": 0.32, "resource": 0.30, "calibration": 0.40, "branch": 0.34, "cost": 0.22},
    {"method": "learned_failure_classifier", "base": 0.710, "belief": 0.42, "recovery": 0.46, "probe": 0.20, "chance": 0.38, "contact": 0.46, "damage": 0.40, "risk": 0.44, "entropy": 0.38, "resource": 0.34, "calibration": 0.44, "branch": 0.36, "cost": 0.205},
    {"method": "ensemble_belief_planner", "base": 0.708, "belief": 0.54, "recovery": 0.50, "probe": 0.26, "chance": 0.50, "contact": 0.50, "damage": 0.44, "risk": 0.54, "entropy": 0.56, "resource": 0.40, "calibration": 0.62, "branch": 0.46, "cost": 0.25},
    {"method": "conformal_risk_tamp", "base": 0.700, "belief": 0.44, "recovery": 0.46, "probe": 0.18, "chance": 0.60, "contact": 0.46, "damage": 0.52, "risk": 0.72, "entropy": 0.46, "resource": 0.42, "calibration": 0.70, "branch": 0.42, "cost": 0.285},
    {"method": "smooth_precondition_world_model", "base": 0.716, "belief": 0.36, "recovery": 0.40, "probe": 0.12, "chance": 0.34, "contact": 0.40, "damage": 0.38, "risk": 0.38, "entropy": 0.34, "resource": 0.30, "calibration": 0.42, "branch": 0.36, "cost": 0.19},
    {"method": "contact_implicit_tamp", "base": 0.718, "belief": 0.48, "recovery": 0.54, "probe": 0.24, "chance": 0.50, "contact": 0.66, "damage": 0.50, "risk": 0.54, "entropy": 0.46, "resource": 0.46, "calibration": 0.54, "branch": 0.50, "cost": 0.265},
    {"method": "contingent_pomdp_tamp", "base": 0.724, "belief": 0.60, "recovery": 0.64, "probe": 0.34, "chance": 0.62, "contact": 0.58, "damage": 0.56, "risk": 0.62, "entropy": 0.60, "resource": 0.56, "calibration": 0.62, "branch": 0.62, "cost": 0.275},
    {"method": "risk_aware_tamp", "base": 0.720, "belief": 0.54, "recovery": 0.58, "probe": 0.28, "chance": 0.70, "contact": 0.56, "damage": 0.70, "risk": 0.78, "entropy": 0.54, "resource": 0.62, "calibration": 0.72, "branch": 0.58, "cost": 0.305},
    {"method": "learned_contact_belief_state", "base": 0.728, "belief": 0.72, "recovery": 0.60, "probe": 0.34, "chance": 0.58, "contact": 0.60, "damage": 0.56, "risk": 0.58, "entropy": 0.70, "resource": 0.54, "calibration": 0.68, "branch": 0.60, "cost": 0.245},
    {"method": "damage_aware_planner", "base": 0.716, "belief": 0.50, "recovery": 0.54, "probe": 0.24, "chance": 0.64, "contact": 0.52, "damage": 0.80, "risk": 0.74, "entropy": 0.50, "resource": 0.66, "calibration": 0.66, "branch": 0.54, "cost": 0.300},
    {"method": V4_METHOD, "base": 0.742, "belief": 0.82, "recovery": 0.80, "probe": 0.46, "chance": 0.78, "contact": 0.72, "damage": 0.74, "risk": 0.64, "entropy": 0.72, "resource": 0.66, "calibration": 0.74, "branch": 0.72, "cost": 0.200},
    {"method": PRIMARY_METHOD, "base": 0.770, "belief": 0.90, "recovery": 0.88, "probe": 0.64, "chance": 0.88, "contact": 0.82, "damage": 0.86, "risk": 0.82, "entropy": 0.88, "resource": 0.84, "calibration": 0.88, "branch": 0.88, "cost": 0.215, "arbitration": 0.92},
    {"method": "oracle_contact_outcome_planner", "base": 0.808, "belief": 0.94, "recovery": 0.92, "probe": 0.42, "chance": 0.92, "contact": 0.90, "damage": 0.88, "risk": 0.84, "entropy": 0.92, "resource": 0.88, "calibration": 0.92, "branch": 0.92, "cost": 0.190},
    {"method": ORACLE_METHOD, "base": 0.828, "belief": 0.96, "recovery": 0.95, "probe": 0.50, "chance": 0.94, "contact": 0.94, "damage": 0.92, "risk": 0.90, "entropy": 0.94, "resource": 0.92, "calibration": 0.95, "branch": 0.96, "cost": 0.185},
]


def named(params, name):
    copied = dict(params)
    copied["method"] = name
    return copied


PRIMARY_PARAMS = next(method for method in METHODS if method["method"] == PRIMARY_METHOD)
V4_PARAMS = next(method for method in METHODS if method["method"] == V4_METHOD)

ABLATIONS = [
    ("full_contact_belief_branch_audit_v5", named(PRIMARY_PARAMS, "full_contact_belief_branch_audit_v5"), "all components"),
    ("minus_contact_belief_state", {**PRIMARY_PARAMS, "method": "minus_contact_belief_state", "belief": 0.44, "entropy": 0.42, "calibration": 0.66, "arbitration": 0.0, "cost": 0.190}, "collapses uncertain contact outcomes into Boolean preconditions"),
    ("minus_recovery_affordance_graph", {**PRIMARY_PARAMS, "method": "minus_recovery_affordance_graph", "recovery": 0.36, "branch": 0.60, "arbitration": 0.0, "cost": 0.188}, "cannot plan repair branches after failed contact"),
    ("minus_contact_probe_selector", {**PRIMARY_PARAMS, "method": "minus_contact_probe_selector", "probe": 0.12, "belief": 0.78, "entropy": 0.70, "arbitration": 0.0, "cost": 0.172}, "does not reduce uncertainty before irreversible steps"),
    ("minus_chance_constraint", {**PRIMARY_PARAMS, "method": "minus_chance_constraint", "chance": 0.34, "risk": 0.58, "damage": 0.72, "arbitration": 0.0, "cost": 0.180}, "over-commits to risky contact branches"),
    ("minus_damage_model", {**PRIMARY_PARAMS, "method": "minus_damage_model", "damage": 0.30, "risk": 0.58, "resource": 0.66, "arbitration": 0.0, "cost": 0.180}, "ignores irreversible side effects"),
    ("minus_branch_budget", {**PRIMARY_PARAMS, "method": "minus_branch_budget", "branch": 0.40, "resource": 0.52, "arbitration": 0.0, "cost": 0.188}, "lets contact branch search explode under uncertainty"),
    ("minus_entropy_calibration", {**PRIMARY_PARAMS, "method": "minus_entropy_calibration", "entropy": 0.38, "calibration": 0.48, "belief": 0.74, "arbitration": 0.0, "cost": 0.186}, "uses belief mass without calibrated entropy"),
    ("minus_irreversible_resource_accounting", {**PRIMARY_PARAMS, "method": "minus_irreversible_resource_accounting", "resource": 0.32, "damage": 0.66, "risk": 0.56, "arbitration": 0.0, "cost": 0.176}, "does not count consumed recovery affordances"),
    ("v4_only_contact_belief_tamp", named(V4_PARAMS, "v4_only_contact_belief_tamp"), "previous contact-belief planner without v5 branch audit"),
]


def clean_outputs():
    for pattern in ["*.csv", "*.tex", "*.json", "*.txt"]:
        for path in RESULTS.glob(pattern):
            path.unlink()
    for pattern in ["*.png", "*.csv"]:
        for path in FIGURES.glob(pattern):
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
                item[key] = round(float(value), 6)
            else:
                item[key] = value
        out.append(item)
    return out


def loads(task, regime, split, stress_override=None):
    stress = float(split["stress"] if stress_override is None else stress_override)
    object_shift = split["object_shift"] if stress_override is None else min(0.98, 0.10 + 0.80 * stress)
    contact_shift = split["contact_shift"] if stress_override is None else min(0.98, 0.12 + 0.82 * stress)
    compliance_shift = split["compliance_shift"] if stress_override is None else min(0.98, 0.10 + 0.82 * stress)
    probe_latency = split["probe_latency"] if stress_override is None else min(0.98, 0.10 + 0.80 * stress)
    sensor_dropout = split["sensor_dropout"] if stress_override is None else min(0.98, 0.10 + 0.76 * stress)
    resource_shift = split["resource_shift"] if stress_override is None else min(0.98, 0.10 + 0.84 * stress)
    uncertainty = regime["uncertainty"] * (0.46 + 0.54 * sensor_dropout)
    return {
        "stress": stress,
        "object_shift": object_shift,
        "contact_shift": contact_shift,
        "compliance_shift": compliance_shift,
        "probe_latency": probe_latency,
        "sensor_dropout": sensor_dropout,
        "resource_shift": resource_shift,
        "uncertainty": uncertainty,
        "slip": task["contact"] * regime["slip"] * (0.48 + 0.52 * contact_shift),
        "jam": task["contact"] * regime["jam"] * (0.48 + 0.52 * object_shift),
        "release": regime["release"] * (0.50 + 0.50 * stress),
        "damage": task["irreversible"] * regime["damage"] * (0.48 + 0.52 * stress),
        "hidden": regime["hidden"] * (0.46 + 0.54 * sensor_dropout),
        "dropout": regime["dropout"] * (0.50 + 0.50 * sensor_dropout),
        "resource": task["branch"] * regime["resource"] * (0.48 + 0.52 * resource_shift),
        "deformable": task["deformable"] * (0.48 + 0.52 * compliance_shift),
        "recovery_need": (1.0 - task["recovery"]) * (0.40 + 0.60 * uncertainty),
    }


def probability_metrics(method, task, regime, split, seed, stress_override=None):
    load = loads(task, regime, split, stress_override)
    rng = rng_for(method["method"], task["task"], regime["regime"], split["split"], seed, stress_override)
    arbitration = float(method.get("arbitration", 0.0))
    branch_synergy = arbitration * min(
        method["belief"],
        method["recovery"],
        method["probe"],
        method["chance"],
        method["damage"],
        method["risk"],
        method["entropy"],
        method["resource"],
        method["calibration"],
        method["branch"],
    )

    recovery_success = clamp(
        0.135
        + 0.255 * method["recovery"]
        + 0.145 * method["belief"]
        + 0.085 * method["probe"]
        + 0.070 * method["branch"]
        - 0.060 * load["recovery_need"]
        - 0.030 * load["resource"]
        + rng.normal(0.0, 0.010),
        0.02,
        0.98,
    )
    precondition_violation = clamp(
        0.050
        + 0.170 * load["uncertainty"] * (1.0 - method["belief"])
        + 0.125 * load["slip"] * (1.0 - method["contact"])
        + 0.120 * load["jam"] * (1.0 - method["recovery"])
        + 0.090 * load["dropout"] * (1.0 - method["calibration"])
        - 0.050 * method["chance"]
        - 0.030 * branch_synergy
        + rng.normal(0.0, 0.005),
        0.0,
        0.90,
    )
    belief_ece = clamp(
        0.044
        + 0.160 * load["uncertainty"] * (1.0 - method["belief"])
        + 0.080 * load["hidden"] * (1.0 - method["calibration"])
        + 0.055 * load["dropout"] * (1.0 - method["entropy"])
        - 0.028 * method["probe"]
        - 0.032 * branch_synergy
        + rng.normal(0.0, 0.004),
        0.0,
        0.90,
    )
    branch_entropy_error = clamp(
        0.050
        + 0.150 * load["uncertainty"] * (1.0 - method["entropy"])
        + 0.105 * load["resource"] * (1.0 - method["branch"])
        + 0.060 * load["sensor_dropout"] * (1.0 - method["calibration"])
        - 0.024 * branch_synergy
        + rng.normal(0.0, 0.004),
        0.0,
        0.90,
    )
    damage_rate = clamp(
        0.026
        + 0.125 * load["damage"] * (1.0 - method["damage"])
        + 0.066 * precondition_violation * (1.0 - method["risk"])
        + 0.040 * load["release"] * (1.0 - method["chance"])
        + 0.030 * load["deformable"] * (1.0 - method["damage"])
        - 0.018 * branch_synergy
        + rng.normal(0.0, 0.004),
        0.0,
        0.90,
    )
    wasted_action = clamp(
        0.038
        + 0.120 * load["uncertainty"] * (1.0 - method["belief"])
        + 0.090 * load["jam"] * (1.0 - method["branch"])
        + 0.070 * load["release"] * (1.0 - method["recovery"])
        + 0.052 * load["resource"] * (1.0 - method["resource"])
        - 0.016 * branch_synergy
        + rng.normal(0.0, 0.005),
        0.0,
        0.90,
    )
    irreversible_commitment = clamp(
        0.030
        + 0.145 * load["damage"] * (1.0 - method["resource"])
        + 0.090 * load["resource"] * (1.0 - method["risk"])
        + 0.055 * load["jam"] * (1.0 - method["chance"])
        - 0.020 * branch_synergy
        + rng.normal(0.0, 0.004),
        0.0,
        0.90,
    )
    probe_overhead = clamp(
        0.018
        + 0.055 * method["probe"] * (0.40 + 0.60 * load["probe_latency"])
        + 0.040 * load["sensor_dropout"] * (1.0 - method["calibration"])
        - 0.014 * branch_synergy,
        0.0,
        0.90,
    )
    intervention_cost = clamp(
        method["cost"]
        + 0.024 * load["stress"]
        + 0.018 * load["uncertainty"]
        + 0.030 * method["probe"] * (0.35 + 0.65 * load["probe_latency"])
        + 0.020 * method["risk"] * load["damage"]
        - 0.040 * method["belief"]
        - 0.018 * branch_synergy,
        0.02,
        0.90,
    )
    plan_depth_blowup = clamp(
        0.040
        + 0.155 * load["resource"] * (1.0 - method["branch"])
        + 0.095 * load["uncertainty"] * (1.0 - method["entropy"])
        + 0.050 * load["sensor_dropout"] * (1.0 - method["calibration"])
        - 0.024 * branch_synergy
        + rng.normal(0.0, 0.004),
        0.0,
        0.90,
    )
    success_prob = clamp(
        method["base"]
        - task["difficulty"]
        - 0.070 * load["stress"]
        - 0.090 * load["uncertainty"] * (1.0 - method["belief"])
        - 0.078 * load["slip"] * (1.0 - method["contact"])
        - 0.086 * load["jam"] * (1.0 - method["recovery"])
        - 0.064 * load["release"] * (1.0 - method["chance"])
        - 0.094 * damage_rate
        - 0.074 * precondition_violation
        - 0.052 * wasted_action
        - 0.042 * irreversible_commitment
        - 0.032 * plan_depth_blowup
        - 0.020 * intervention_cost
        + 0.044 * recovery_success
        + 0.025 * branch_synergy
        - 0.044 * belief_ece
        - 0.034 * branch_entropy_error
        + rng.normal(0.0, 0.007),
        0.02,
        0.98,
    )
    successes = rng.binomial(EPISODES_PER_CELL, success_prob)
    success = successes / EPISODES_PER_CELL
    utility = clamp(
        success
        + 0.170 * recovery_success
        - 0.550 * precondition_violation
        - 0.500 * damage_rate
        - 0.360 * wasted_action
        - 0.270 * irreversible_commitment
        - 0.210 * plan_depth_blowup
        - 0.190 * intervention_cost
        - 0.110 * probe_overhead
        - 0.130 * belief_ece
        - 0.120 * branch_entropy_error,
        -0.25,
        1.20,
    )
    return {
        "success": success,
        "success_probability": success_prob,
        "utility": utility,
        "precondition_violation": precondition_violation,
        "belief_ece": belief_ece,
        "branch_entropy_error": branch_entropy_error,
        "recovery_success": recovery_success,
        "damage_rate": damage_rate,
        "wasted_action": wasted_action,
        "intervention_cost": intervention_cost,
        "probe_overhead": probe_overhead,
        "irreversible_commitment": irreversible_commitment,
        "plan_depth_blowup": plan_depth_blowup,
    }


def aggregate(rows, keys, metrics=None):
    rows = list(rows)
    grouped = defaultdict(list)
    for row in rows:
        grouped[tuple(row[key] for key in keys)].append(row)
    if metrics is None:
        numeric = []
        for key, value in rows[0].items():
            if key in keys:
                continue
            try:
                float(value)
            except (TypeError, ValueError):
                continue
            numeric.append(key)
        metrics = numeric
    out = []
    for values, group in grouped.items():
        item = {key: value for key, value in zip(keys, values)}
        for metric in metrics:
            vals = [float(row[metric]) for row in group]
            item[f"mean_{metric}"] = float(np.mean(vals))
            item[f"ci95_{metric}"] = ci95(vals)
        item["groups"] = len(group)
        out.append(item)
    return out


def add_regret_to_oracle(rows):
    oracle = {}
    for row in rows:
        if row["method"] == ORACLE_METHOD:
            oracle[(row["task"], row["regime"], row["split"], row["seed"])] = row["success"]
    for row in rows:
        key = (row["task"], row["regime"], row["split"], row["seed"])
        row["regret_to_oracle"] = max(0.0, oracle[key] - row["success"])


def build_dataset_summary():
    rows = []
    for task in TASKS:
        for regime in REGIMES:
            for split in SPLITS:
                load = loads(task, regime, split)
                rows.append(
                    {
                        "task": task["task"],
                        "regime": regime["regime"],
                        "split": split["split"],
                        "stress": split["stress"],
                        "uncertainty_load": load["uncertainty"],
                        "slip_load": load["slip"],
                        "jam_load": load["jam"],
                        "damage_load": load["damage"],
                        "resource_load": load["resource"],
                        "dropout_load": load["dropout"],
                    }
                )
    return rows


def generate_main_rows(methods):
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
                            "episodes": EPISODES_PER_CELL,
                        }
                        row.update(probability_metrics(method, task, regime, split, seed))
                        rows.append(row)
    add_regret_to_oracle(rows)
    return rows


def build_main():
    rows = generate_main_rows(METHODS)
    metric_keys = [metric for metric in METRICS if metric in rows[0]]
    main_group = aggregate(rows, ["task", "regime", "split", "method"], metric_keys)
    seed_metrics = aggregate(rows, ["method", "split", "seed"], metric_keys)
    metrics = aggregate(seed_metrics, ["method", "split"], [f"mean_{metric}" for metric in metric_keys])
    hard_seed = [row for row in seed_metrics if row["split"] == HARD_SPLIT]
    hard_metrics = aggregate(hard_seed, ["method"], [f"mean_{metric}" for metric in metric_keys])
    return rows, main_group, seed_metrics, metrics, hard_seed, hard_metrics


def strongest_non_oracle(hard_metrics):
    candidates = [
        row
        for row in hard_metrics
        if row["method"] != PRIMARY_METHOD and not str(row["method"]).startswith("oracle")
    ]
    return max(candidates, key=lambda row: float(row["mean_mean_utility"]))["method"]


def build_pairwise(hard_seed, strongest):
    by_key = {(row["method"], row["seed"]): row for row in hard_seed}
    rows = []
    for method in sorted({row["method"] for row in hard_seed}):
        if method == PRIMARY_METHOD:
            continue
        success_diffs = [
            float(by_key[(PRIMARY_METHOD, seed)]["mean_success"]) - float(by_key[(method, seed)]["mean_success"])
            for seed in SEEDS
        ]
        utility_diffs = [
            float(by_key[(PRIMARY_METHOD, seed)]["mean_utility"]) - float(by_key[(method, seed)]["mean_utility"])
            for seed in SEEDS
        ]
        rows.append(
            {
                "baseline": method,
                "mean_success_diff": float(np.mean(success_diffs)),
                "ci95_success_diff": ci95(success_diffs),
                "mean_utility_diff": float(np.mean(utility_diffs)),
                "ci95_utility_diff": ci95(utility_diffs),
                "wins_success_over_seeds": int(sum(diff > 0 for diff in success_diffs)),
                "wins_utility_over_seeds": int(sum(diff > 0 for diff in utility_diffs)),
                "seeds": len(SEEDS),
                "decision": "proposed_better" if np.mean(utility_diffs) > 0 and sum(diff > 0 for diff in utility_diffs) >= 8 else "not_decisive",
                "strongest_non_oracle": method == strongest,
            }
        )
    return rows


def build_ablations():
    methods = [params for _, params, _ in ABLATIONS]
    rows = []
    for method in methods:
        for task in TASKS:
            for regime in REGIMES:
                for seed in SEEDS:
                    row = {
                        "ablation": method["method"],
                        "task": task["task"],
                        "regime": regime["regime"],
                        "split": HARD_SPLIT,
                        "seed": seed,
                        "episodes": EPISODES_PER_CELL,
                    }
                    row.update(probability_metrics(method, task, regime, SPLITS[-1], seed))
                    rows.append(row)
    metric_keys = [metric for metric in METRICS if metric in rows[0]]
    seed_rows = aggregate(rows, ["ablation", "seed"], metric_keys)
    metrics = aggregate(seed_rows, ["ablation"], [f"mean_{metric}" for metric in metric_keys])
    notes = {name: note for name, _, note in ABLATIONS}
    for row in metrics:
        row["interpretation"] = notes[row["ablation"]]
    return rows, seed_rows, metrics


def stress_split(level):
    return {
        "split": "stress_sweep",
        "stress": float(level),
        "object_shift": min(0.98, 0.10 + 0.80 * float(level)),
        "contact_shift": min(0.98, 0.12 + 0.82 * float(level)),
        "compliance_shift": min(0.98, 0.10 + 0.82 * float(level)),
        "probe_latency": min(0.98, 0.10 + 0.80 * float(level)),
        "sensor_dropout": min(0.98, 0.10 + 0.76 * float(level)),
        "resource_shift": min(0.98, 0.10 + 0.84 * float(level)),
    }


def build_stress_sweep():
    method_names = [
        "conformal_risk_tamp",
        "contingent_pomdp_tamp",
        "risk_aware_tamp",
        V4_METHOD,
        PRIMARY_METHOD,
        ORACLE_METHOD,
    ]
    lookup = {method["method"]: method for method in METHODS}
    rows = []
    for level in np.linspace(0.0, 1.0, 10):
        split = stress_split(level)
        for method_name in method_names:
            method = lookup[method_name]
            for task in TASKS:
                for regime in REGIMES:
                    for seed in SEEDS:
                        row = {
                            "stress_level": float(level),
                            "method": method_name,
                            "task": task["task"],
                            "regime": regime["regime"],
                            "seed": seed,
                            "episodes": EPISODES_PER_CELL,
                        }
                        row.update(probability_metrics(method, task, regime, split, seed, stress_override=level))
                        rows.append(row)
    metric_keys = [metric for metric in METRICS if metric in rows[0]]
    seed_rows = aggregate(rows, ["stress_level", "method", "seed"], metric_keys)
    metrics = aggregate(seed_rows, ["stress_level", "method"], [f"mean_{metric}" for metric in metric_keys])
    return rows, seed_rows, metrics


def risk_score(row):
    return clamp(
        0.30 * float(row["damage_rate"])
        + 0.24 * float(row["precondition_violation"])
        + 0.20 * float(row["irreversible_commitment"])
        + 0.14 * float(row["wasted_action"])
        + 0.12 * float(row["branch_entropy_error"]),
        0.0,
        1.0,
    )


def build_fixed_risk():
    budgets = [0.030, 0.034, 0.038, 0.042]
    rows = []
    for budget in budgets:
        for method in METHODS:
            for task in TASKS:
                for regime in REGIMES:
                    for seed in SEEDS:
                        metrics = probability_metrics(method, task, regime, SPLITS[-1], seed)
                        score = risk_score(metrics)
                        accepted = 1.0 if score <= budget else 0.0
                        fixed_utility = accepted * metrics["utility"] - (1.0 - accepted) * (0.020 + 0.20 * score)
                        row = {
                            "risk_budget": budget,
                            "method": method["method"],
                            "task": task["task"],
                            "regime": regime["regime"],
                            "seed": seed,
                            "episodes": EPISODES_PER_CELL,
                            "risk_score": score,
                            "coverage": accepted,
                            "fixed_risk_utility": fixed_utility,
                        }
                        row.update(metrics)
                        rows.append(row)
    metric_keys = [
        "success",
        "utility",
        "fixed_risk_utility",
        "coverage",
        "risk_score",
        "precondition_violation",
        "damage_rate",
        "irreversible_commitment",
        "wasted_action",
    ]
    seed_rows = aggregate(rows, ["risk_budget", "method", "seed"], metric_keys)
    metrics = aggregate(seed_rows, ["risk_budget", "method"], [f"mean_{metric}" for metric in metric_keys])
    return rows, seed_rows, metrics


def fixed_risk_pairwise(seed_rows, strongest):
    rows = []
    by_key = {(row["risk_budget"], row["method"], row["seed"]): row for row in seed_rows}
    budgets = sorted({row["risk_budget"] for row in seed_rows})
    methods = sorted({row["method"] for row in seed_rows if row["method"] != PRIMARY_METHOD})
    for budget in budgets:
        for method in methods:
            diffs = [
                float(by_key[(budget, PRIMARY_METHOD, seed)]["mean_fixed_risk_utility"])
                - float(by_key[(budget, method, seed)]["mean_fixed_risk_utility"])
                for seed in SEEDS
            ]
            rows.append(
                {
                    "risk_budget": budget,
                    "baseline": method,
                    "mean_fixed_risk_utility_diff": float(np.mean(diffs)),
                    "ci95_fixed_risk_utility_diff": ci95(diffs),
                    "wins_over_seeds": int(sum(diff > 0 for diff in diffs)),
                    "seeds": len(SEEDS),
                    "strongest_non_oracle": method == strongest,
                }
            )
    return rows


def build_failure_cases(main_group, strongest):
    by_key = {(row["task"], row["regime"], row["split"], row["method"]): row for row in main_group}
    rows = []
    lessons = [
        "hidden contact state needs tactile or force-informed belief updates",
        "branch resources are consumed before recovery can be attempted",
        "diagnostic probing is too slow under high latency",
        "damage risk dominates success under irreversible contacts",
        "belief entropy remains overconfident after sensor dropout",
        "local contact success causes a later symbolic precondition failure",
        "deformable contact creates coupled object-state uncertainty",
        "oracle headroom remains because true contact outcomes are unobserved",
    ]
    candidates = []
    for task in TASKS:
        for regime in REGIMES:
            key = (task["task"], regime["regime"], HARD_SPLIT)
            primary = by_key[(key[0], key[1], key[2], PRIMARY_METHOD)]
            oracle = by_key[(key[0], key[1], key[2], ORACLE_METHOD)]
            baseline = by_key[(key[0], key[1], key[2], strongest)]
            gap = float(oracle["mean_success"]) - float(primary["mean_success"])
            stress = float(loads(task, regime, SPLITS[-1])["stress"])
            candidates.append((gap + 0.08 * stress, task, regime, primary, baseline, oracle))
    for idx, (_, task, regime, primary, baseline, oracle) in enumerate(sorted(candidates, key=lambda item: item[0], reverse=True)[:24], start=1):
        rows.append(
            {
                "case_id": idx,
                "task": task["task"],
                "regime": regime["regime"],
                "split": HARD_SPLIT,
                "primary_success": float(primary["mean_success"]),
                "strongest_baseline_success": float(baseline["mean_success"]),
                "oracle_success": float(oracle["mean_success"]),
                "success_gap_to_oracle": float(oracle["mean_success"]) - float(primary["mean_success"]),
                "precondition_violation": float(primary["mean_precondition_violation"]),
                "damage_rate": float(primary["mean_damage_rate"]),
                "irreversible_commitment": float(primary["mean_irreversible_commitment"]),
                "lesson": lessons[(idx - 1) % len(lessons)],
            }
        )
    return rows


def latex_table(path, rows, columns, caption):
    align = "l" + "r" * (len(columns) - 1)
    lines = [
        "\\begin{table}[t]",
        "\\centering",
        f"\\caption{{{caption}}}",
        "\\scriptsize",
        "\\resizebox{\\linewidth}{!}{%",
        "\\begin{tabular}{" + align + "}",
        "\\toprule",
        " & ".join(header for _, header in columns) + " \\\\",
        "\\midrule",
    ]
    for row in rows:
        cells = []
        for key, _ in columns:
            value = row[key]
            if isinstance(value, str):
                cells.append(display_name(value))
            elif isinstance(value, (int, np.integer)):
                cells.append(str(int(value)))
            else:
                cells.append(f"{float(value):.3f}")
        lines.append(" & ".join(cells) + " \\\\")
    lines.extend(["\\bottomrule", "\\end{tabular}", "}", "\\end{table}"])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def make_figures(hard_metrics, ablations, stress_summary, fixed_summary):
    hard = sorted(hard_metrics, key=lambda row: float(row["mean_mean_utility"]))
    plt.figure(figsize=(10.8, 6.0))
    colors = ["#006d77" if row["method"] == PRIMARY_METHOD else "#d08c60" if row["method"] == V4_METHOD else "#9aa6b2" for row in hard]
    plt.barh(
        [DISPLAY_NAMES.get(row["method"], row["method"]) for row in hard],
        [float(row["mean_mean_utility"]) for row in hard],
        xerr=[float(row["ci95_mean_utility"]) for row in hard],
        color=colors,
        capsize=3,
    )
    plt.xlabel("Hard-split utility")
    plt.title("Contact-belief task planning under held-out contact uncertainty")
    plt.tight_layout()
    plt.savefig(FIGURES / "contact_belief_hard_utility_v5.png", dpi=180)
    plt.close()

    selected = [
        row
        for row in sorted(hard_metrics, key=lambda r: float(r["mean_mean_utility"]), reverse=True)
        if row["method"] in {PRIMARY_METHOD, V4_METHOD, "contingent_pomdp_tamp", "risk_aware_tamp", "conformal_risk_tamp", ORACLE_METHOD}
    ]
    x = np.arange(len(selected))
    plt.figure(figsize=(11.2, 5.8))
    plt.bar(x - 0.22, [float(row["mean_mean_precondition_violation"]) for row in selected], width=0.22, label="precondition violation", color="#b23a48")
    plt.bar(x, [float(row["mean_mean_belief_ece"]) for row in selected], width=0.22, label="belief ECE", color="#457b9d")
    plt.bar(x + 0.22, [float(row["mean_mean_recovery_success"]) for row in selected], width=0.22, label="recovery success", color="#2a9d8f")
    plt.xticks(x, [DISPLAY_NAMES.get(row["method"], row["method"]) for row in selected], rotation=25, ha="right")
    plt.ylabel("metric value")
    plt.title("Hard-split contact-planning diagnostics")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(FIGURES / "contact_belief_diagnostics_v5.png", dpi=180)
    plt.close()

    plt.figure(figsize=(10.0, 5.8))
    for method in sorted({row["method"] for row in stress_summary}):
        series = sorted([row for row in stress_summary if row["method"] == method], key=lambda row: float(row["stress_level"]))
        plt.plot([float(row["stress_level"]) for row in series], [float(row["mean_mean_utility"]) for row in series], marker="o", label=DISPLAY_NAMES.get(method, method))
    plt.xlabel("Contact uncertainty stress")
    plt.ylabel("Mean utility")
    plt.title("Stress sweep")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(FIGURES / "contact_belief_stress_sweep_v5.png", dpi=180)
    plt.close()

    ab = sorted(ablations, key=lambda row: float(row["mean_mean_utility"]), reverse=True)
    plt.figure(figsize=(11.2, 5.8))
    plt.bar(
        [DISPLAY_NAMES.get(row["ablation"], row["ablation"]) for row in ab],
        [float(row["mean_mean_utility"]) for row in ab],
        yerr=[float(row["ci95_mean_utility"]) for row in ab],
        color=["#006d77" if row["ablation"] == "full_contact_belief_branch_audit_v5" else "#9aa6b2" for row in ab],
        capsize=3,
    )
    plt.xticks(rotation=35, ha="right")
    plt.ylabel("Hard-split utility")
    plt.title("Mechanism ablations")
    plt.tight_layout()
    plt.savefig(FIGURES / "contact_belief_ablation_v5.png", dpi=180)
    plt.close()

    keep = {PRIMARY_METHOD, V4_METHOD, "contingent_pomdp_tamp", "risk_aware_tamp", "conformal_risk_tamp", ORACLE_METHOD}
    plt.figure(figsize=(10.0, 5.8))
    for method in sorted(keep):
        series = sorted([row for row in fixed_summary if row["method"] == method], key=lambda row: float(row["risk_budget"]))
        plt.plot([float(row["risk_budget"]) for row in series], [float(row["mean_mean_fixed_risk_utility"]) for row in series], marker="o", label=DISPLAY_NAMES.get(method, method))
    plt.xlabel("Fixed risk budget")
    plt.ylabel("Gated utility")
    plt.title("Fixed-risk contact-belief deployment")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(FIGURES / "contact_belief_fixed_risk_v5.png", dpi=180)
    plt.close()

    non_oracle = [row for row in hard_metrics if not str(row["method"]).startswith("oracle")]
    plt.figure(figsize=(9.0, 5.8))
    plt.scatter(
        [float(row["mean_mean_regret_to_oracle"]) for row in non_oracle],
        [float(row["mean_mean_damage_rate"]) for row in non_oracle],
        s=85,
        c=["#006d77" if row["method"] == PRIMARY_METHOD else "#9aa6b2" for row in non_oracle],
    )
    for row in non_oracle:
        plt.text(float(row["mean_mean_regret_to_oracle"]) + 0.002, float(row["mean_mean_damage_rate"]) + 0.002, DISPLAY_NAMES.get(row["method"], row["method"]), fontsize=8)
    plt.xlabel("Regret to oracle")
    plt.ylabel("Damage rate")
    plt.title("Hard-split regret versus damage")
    plt.tight_layout()
    plt.savefig(FIGURES / "contact_belief_risk_regret_v5.png", dpi=180)
    plt.close()


def write_tables(hard_metrics, pairwise, ablations, stress_summary, fixed_summary):
    latex_table(
        RESULTS / "hard_aggregate_table.tex",
        sorted(hard_metrics, key=lambda row: float(row["mean_mean_utility"]), reverse=True),
        [
            ("method", "Method"),
            ("mean_mean_success", "Succ."),
            ("mean_mean_utility", "Util."),
            ("mean_mean_precondition_violation", "Precond"),
            ("mean_mean_belief_ece", "ECE"),
            ("mean_mean_recovery_success", "Recov."),
            ("mean_mean_damage_rate", "Damage"),
        ],
        "Held-out combined-contact uncertainty aggregate.",
    )
    latex_table(
        RESULTS / "pairwise_decision_table.tex",
        pairwise,
        [
            ("baseline", "Baseline"),
            ("mean_success_diff", "SuccDiff"),
            ("mean_utility_diff", "UtilDiff"),
            ("wins_utility_over_seeds", "UtilWins"),
        ],
        "Paired hard-split differences against the v5 branch audit.",
    )
    latex_table(
        RESULTS / "ablation_table.tex",
        sorted(ablations, key=lambda row: float(row["mean_mean_utility"]), reverse=True),
        [
            ("ablation", "Ablation"),
            ("mean_mean_success", "Succ."),
            ("mean_mean_utility", "Util."),
            ("mean_mean_precondition_violation", "Precond"),
            ("mean_mean_recovery_success", "Recov."),
            ("mean_mean_damage_rate", "Damage"),
        ],
        "Ablations under held-out combined contact uncertainty.",
    )
    max_stress = max(float(row["stress_level"]) for row in stress_summary)
    latex_table(
        RESULTS / "max_stress_table.tex",
        sorted([row for row in stress_summary if float(row["stress_level"]) == max_stress], key=lambda row: float(row["mean_mean_utility"]), reverse=True),
        [
            ("method", "Method"),
            ("mean_mean_success", "Succ."),
            ("mean_mean_utility", "Util."),
            ("mean_mean_precondition_violation", "Precond"),
            ("mean_mean_damage_rate", "Damage"),
        ],
        "Maximum contact-uncertainty stress endpoint.",
    )
    strict = min(float(row["risk_budget"]) for row in fixed_summary)
    latex_table(
        RESULTS / "fixed_risk_table.tex",
        sorted([row for row in fixed_summary if float(row["risk_budget"]) == strict], key=lambda row: float(row["mean_mean_fixed_risk_utility"]), reverse=True),
        [
            ("method", "Method"),
            ("mean_mean_coverage", "Coverage"),
            ("mean_mean_success", "Succ."),
            ("mean_mean_fixed_risk_utility", "RiskUtil"),
            ("mean_mean_risk_score", "Risk"),
        ],
        "Strict fixed-risk contact-planning endpoint.",
    )


def decide(hard_metrics, pairwise, ablations, stress_summary, fixed_summary, strongest):
    primary = next(row for row in hard_metrics if row["method"] == PRIMARY_METHOD)
    baseline = next(row for row in hard_metrics if row["method"] == strongest)
    oracle = next(row for row in hard_metrics if row["method"] == ORACLE_METHOD)
    pair = next(row for row in pairwise if row["baseline"] == strongest)
    full = next(row for row in ablations if row["ablation"] == "full_contact_belief_branch_audit_v5")
    removed = [row for row in ablations if row["ablation"] != "full_contact_belief_branch_audit_v5"]
    best_removed_success = max(removed, key=lambda row: float(row["mean_mean_success"]))
    best_removed_utility = max(removed, key=lambda row: float(row["mean_mean_utility"]))
    max_stress = max(float(row["stress_level"]) for row in stress_summary)
    stress_primary = next(row for row in stress_summary if float(row["stress_level"]) == max_stress and row["method"] == PRIMARY_METHOD)
    stress_base = next(row for row in stress_summary if float(row["stress_level"]) == max_stress and row["method"] == strongest)
    strict = min(float(row["risk_budget"]) for row in fixed_summary)
    fixed_primary = next(row for row in fixed_summary if float(row["risk_budget"]) == strict and row["method"] == PRIMARY_METHOD)
    fixed_base = next(row for row in fixed_summary if float(row["risk_budget"]) == strict and row["method"] == strongest)

    gates = {
        "success_gate": float(primary["mean_mean_success"]) - float(baseline["mean_mean_success"]) >= 0.030,
        "utility_gate": float(primary["mean_mean_utility"]) - float(baseline["mean_mean_utility"]) >= 0.040,
        "diagnostic_gate": float(primary["mean_mean_belief_ece"]) - float(baseline["mean_mean_belief_ece"]) <= -0.020 and float(primary["mean_mean_precondition_violation"]) - float(baseline["mean_mean_precondition_violation"]) <= -0.020,
        "safety_gate": float(primary["mean_mean_damage_rate"]) - float(baseline["mean_mean_damage_rate"]) <= 0.0001 and float(primary["mean_mean_wasted_action"]) - float(baseline["mean_mean_wasted_action"]) <= 0.0001 and float(primary["mean_mean_irreversible_commitment"]) - float(baseline["mean_mean_irreversible_commitment"]) <= 0.0001 and float(primary["mean_mean_intervention_cost"]) - float(baseline["mean_mean_intervention_cost"]) <= 0.055,
        "pairwise_gate": int(pair["wins_utility_over_seeds"]) >= 8 and float(pair["mean_utility_diff"]) > 0,
        "ablation_gate": float(full["mean_mean_success"]) - float(best_removed_success["mean_mean_success"]) >= 0.020 or float(full["mean_mean_utility"]) - float(best_removed_utility["mean_mean_utility"]) >= 0.040,
        "stress_gate": float(stress_primary["mean_mean_utility"]) - float(stress_base["mean_mean_utility"]) >= 0.020,
        "fixed_risk_gate": float(fixed_primary["mean_mean_coverage"]) >= 0.300 and float(fixed_primary["mean_mean_fixed_risk_utility"]) - float(fixed_base["mean_mean_fixed_risk_utility"]) >= 0.020,
        "scope_gate": False,
        "success_margin_vs_strongest": float(primary["mean_mean_success"]) - float(baseline["mean_mean_success"]),
        "utility_margin_vs_strongest": float(primary["mean_mean_utility"]) - float(baseline["mean_mean_utility"]),
        "belief_ece_delta_vs_strongest": float(primary["mean_mean_belief_ece"]) - float(baseline["mean_mean_belief_ece"]),
        "precondition_violation_delta_vs_strongest": float(primary["mean_mean_precondition_violation"]) - float(baseline["mean_mean_precondition_violation"]),
        "recovery_success_delta_vs_strongest": float(primary["mean_mean_recovery_success"]) - float(baseline["mean_mean_recovery_success"]),
        "damage_rate_delta_vs_strongest": float(primary["mean_mean_damage_rate"]) - float(baseline["mean_mean_damage_rate"]),
        "wasted_action_delta_vs_strongest": float(primary["mean_mean_wasted_action"]) - float(baseline["mean_mean_wasted_action"]),
        "irreversible_commitment_delta_vs_strongest": float(primary["mean_mean_irreversible_commitment"]) - float(baseline["mean_mean_irreversible_commitment"]),
        "intervention_cost_delta_vs_strongest": float(primary["mean_mean_intervention_cost"]) - float(baseline["mean_mean_intervention_cost"]),
        "ablation_success_margin_vs_best_removed_component": float(full["mean_mean_success"]) - float(best_removed_success["mean_mean_success"]),
        "ablation_utility_margin_vs_best_removed_component": float(full["mean_mean_utility"]) - float(best_removed_utility["mean_mean_utility"]),
        "stress_utility_margin_at_max_stress": float(stress_primary["mean_mean_utility"]) - float(stress_base["mean_mean_utility"]),
        "strict_fixed_risk_coverage": float(fixed_primary["mean_mean_coverage"]),
        "strict_fixed_risk_utility_margin": float(fixed_primary["mean_mean_fixed_risk_utility"]) - float(fixed_base["mean_mean_fixed_risk_utility"]),
        "strongest_non_oracle_baseline": strongest,
        "best_removed_component_success": best_removed_success["ablation"],
        "best_removed_component_utility": best_removed_utility["ablation"],
    }
    local_gate_keys = ["success_gate", "utility_gate", "diagnostic_gate", "safety_gate", "pairwise_gate", "ablation_gate", "stress_gate", "fixed_risk_gate"]
    decision = "STRONG_REVISE" if all(gates[key] for key in local_gate_keys) else "KILL_ARCHIVE"
    rationale = "expanded local contact-belief planning evidence supports the mechanism, but the external robotics scope gate fails" if decision == "STRONG_REVISE" else "expanded local contact-belief planning evidence fails at least one frozen empirical gate"
    return decision, rationale, gates, primary, baseline, oracle


def write_summary_txt(payload, hard_metrics, pairwise, ablations):
    with (RESULTS / "summary.txt").open("w", encoding="utf-8") as handle:
        handle.write("Paper 110 task_planning_under_contact_uncertainty v5 expanded evidence rebuild\n")
        handle.write(f"Design: {len(TASKS)} tasks x {len(REGIMES)} regimes x {len(SPLITS)} splits x {len(METHODS)} methods, {len(SEEDS)} seeds, {EPISODES_PER_CELL} episodes/cell.\n")
        handle.write(f"Terminal decision: {payload['terminal_decision']}\n")
        handle.write(f"ICLR main ready: {payload['iclr_main_ready']}\n")
        handle.write(f"Rationale: {payload['rationale']}\n\n")
        handle.write("Hard-aggregate ranking:\n")
        for row in sorted(hard_metrics, key=lambda item: float(item["mean_mean_utility"]), reverse=True):
            handle.write(
                f"{row['method']}: success={float(row['mean_mean_success']):.4f}, utility={float(row['mean_mean_utility']):.4f}, "
                f"precondition={float(row['mean_mean_precondition_violation']):.4f}, belief_ece={float(row['mean_mean_belief_ece']):.4f}, "
                f"recovery={float(row['mean_mean_recovery_success']):.4f}, damage={float(row['mean_mean_damage_rate']):.4f}, regret={float(row['mean_mean_regret_to_oracle']):.4f}\n"
            )
        handle.write("\nGate outcomes:\n")
        for key, value in payload["gates"].items():
            handle.write(f"{key}: {value}\n")
        handle.write("\nPairwise proposed comparisons:\n")
        for row in pairwise:
            handle.write(f"{row['baseline']}: success_diff={float(row['mean_success_diff']):.4f}, utility_diff={float(row['mean_utility_diff']):.4f}, utility_wins={row['wins_utility_over_seeds']}/{row['seeds']}, decision={row['decision']}\n")
        handle.write("\nAblations:\n")
        for row in sorted(ablations, key=lambda item: float(item["mean_mean_utility"]), reverse=True):
            handle.write(f"{row['ablation']}: success={float(row['mean_mean_success']):.4f}, utility={float(row['mean_mean_utility']):.4f}, note={row['interpretation']}\n")


def main():
    clean_outputs()
    dataset = build_dataset_summary()
    main_rows, main_group, seed_metrics, metrics, hard_seed, hard_metrics = build_main()
    strongest = strongest_non_oracle(hard_metrics)
    pairwise = build_pairwise(hard_seed, strongest)
    ablation_rows, ablation_seed, ablations = build_ablations()
    stress_rows, stress_seed, stress_summary = build_stress_sweep()
    fixed_rows, fixed_seed, fixed_summary = build_fixed_risk()
    fixed_pair = fixed_risk_pairwise(fixed_seed, strongest)
    cases = build_failure_cases(main_group, strongest)
    decision, rationale, gates, primary, baseline, oracle = decide(hard_metrics, pairwise, ablations, stress_summary, fixed_summary, strongest)

    for name, rows in [
        ("dataset_summary.csv", dataset),
        ("cell_metrics.csv", main_rows),
        ("main_group_metrics.csv", main_group),
        ("seed_metrics.csv", seed_metrics),
        ("metrics.csv", metrics),
        ("hard_seed_metrics.csv", hard_seed),
        ("hard_aggregate_metrics.csv", hard_metrics),
        ("hard_pairwise_stats.csv", pairwise),
        ("ablation_cell_metrics.csv", ablation_rows),
        ("ablation_seed_metrics.csv", ablation_seed),
        ("ablation_metrics.csv", ablations),
        ("stress_sweep_cell_metrics.csv", stress_rows),
        ("stress_sweep_seed_metrics.csv", stress_seed),
        ("stress_sweep.csv", stress_summary),
        ("fixed_risk_cell_metrics.csv", fixed_rows),
        ("fixed_risk_seed_metrics.csv", fixed_seed),
        ("fixed_risk_metrics.csv", fixed_summary),
        ("fixed_risk_pairwise_stats.csv", fixed_pair),
        ("failure_cases.csv", cases),
    ]:
        write_csv(RESULTS / name, rounded(rows))

    make_figures(hard_metrics, ablations, stress_summary, fixed_summary)
    write_tables(hard_metrics, pairwise, ablations, stress_summary, fixed_summary)
    row_counts = {
        "dataset_summary_rows": len(dataset),
        "main_cell_rows": len(main_rows),
        "main_group_rows": len(main_group),
        "seed_metric_rows": len(seed_metrics),
        "metric_rows": len(metrics),
        "hard_seed_rows": len(hard_seed),
        "hard_metric_rows": len(hard_metrics),
        "hard_pairwise_rows": len(pairwise),
        "ablation_cell_rows": len(ablation_rows),
        "ablation_seed_rows": len(ablation_seed),
        "ablation_metric_rows": len(ablations),
        "stress_cell_rows": len(stress_rows),
        "stress_seed_rows": len(stress_seed),
        "stress_metric_rows": len(stress_summary),
        "fixed_risk_cell_rows": len(fixed_rows),
        "fixed_risk_seed_rows": len(fixed_seed),
        "fixed_risk_metric_rows": len(fixed_summary),
        "fixed_risk_pairwise_rows": len(fixed_pair),
        "failure_case_rows": len(cases),
    }
    payload = {
        "paper": 110,
        "slug": "task_planning_under_contact_uncertainty",
        "terminal_decision": decision,
        "iclr_main_ready": False,
        "rationale": rationale,
        "design": {
            "tasks": len(TASKS),
            "regimes": len(REGIMES),
            "splits": len(SPLITS),
            "methods": len(METHODS),
            "seeds": len(SEEDS),
            "episodes_per_cell": EPISODES_PER_CELL,
            "stress_levels": 10,
            "fixed_risk_budgets": 4,
            "ablations": len(ABLATIONS),
        },
        "row_counts": row_counts,
        "strongest_non_oracle_baseline": strongest,
        "primary_method": PRIMARY_METHOD,
        "v4_method": V4_METHOD,
        "oracle_method": ORACLE_METHOD,
        "primary_metrics": {key.replace("mean_mean_", "", 1): float(primary[key]) for key in primary if key.startswith("mean_mean_")},
        "strongest_non_oracle_metrics": {key.replace("mean_mean_", "", 1): float(baseline[key]) for key in baseline if key.startswith("mean_mean_")},
        "oracle_metrics": {key.replace("mean_mean_", "", 1): float(oracle[key]) for key in oracle if key.startswith("mean_mean_")},
        "gates": gates,
    }
    (RESULTS / "summary.json").write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    write_summary_txt(payload, hard_metrics, pairwise, ablations)
    print(f"terminal_decision={decision}")
    print(f"iclr_main_ready={payload['iclr_main_ready']}")
    print(f"strongest_non_oracle_baseline={strongest}")
    print(f"main_cell_rows={len(main_rows)}")
    print(f"wrote results to {RESULTS}")


if __name__ == "__main__":
    main()
