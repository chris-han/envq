from __future__ import annotations
import math
from dataclasses import dataclass
from statistics import mean
from typing import Iterable, Mapping, Sequence

from .schema import EnvQScoreVector

EPS = 1e-9


def clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))


def capability_necessity(normal_rewards: Sequence[float], ablated_rewards: Sequence[float]) -> tuple[float, float]:
    if len(normal_rewards) != len(ablated_rewards) or not normal_rewards:
        raise ValueError("normal and ablated rewards must be non-empty and aligned")
    vals = [max(0.0, (r - a) / max(abs(r), EPS)) for r, a in zip(normal_rewards, ablated_rewards)]
    cn = clamp01(mean(vals))
    ang = mean(r - a for r, a in zip(normal_rewards, ablated_rewards))
    return cn, ang


def verifier_fidelity(tp: int, tn: int, fp: int, fn: int, fp_weight: float = 2.0, fn_weight: float = 1.0) -> float:
    n = tp + tn + fp + fn
    if n <= 0:
        raise ValueError("at least one audited episode required")
    return clamp01(1.0 - (fp_weight * fp + fn_weight * fn) / (fp_weight * n))


def verifier_fidelity_continuous(native: Sequence[float], reference: Sequence[float]) -> float:
    if len(native) != len(reference) or not native:
        raise ValueError("native and reference rewards must be non-empty and aligned")
    mae = mean(abs(a - b) for a, b in zip(native, reference))
    return clamp01(1.0 - mae)


def shortcut_resistance(iid_performance: float, perturbed_performance: Mapping[str, float], weights: Mapping[str, float] | None = None) -> float:
    if not perturbed_performance:
        raise ValueError("at least one perturbation family required")
    if weights is None:
        weights = {k: 1.0 / len(perturbed_performance) for k in perturbed_performance}
    total_w = sum(weights.get(k, 0.0) for k in perturbed_performance)
    if total_w <= 0:
        raise ValueError("positive perturbation weights required")
    return clamp01(sum(weights.get(k, 0.0) * min(1.0, v / max(iid_performance, EPS)) for k, v in perturbed_performance.items()) / total_w)


def discriminative_power(model_performances: Sequence[float], item_discrimination: float | None = None, range_threshold: float = 0.5) -> float:
    if len(model_performances) < 2:
        raise ValueError("at least two model baselines required")
    dr = max(model_performances) - min(model_performances)
    dr_n = clamp01(dr / range_threshold)
    pbar = mean(model_performances)
    ns = clamp01(4.0 * pbar * (1.0 - pbar))
    if item_discrimination is None:
        return clamp01(0.6 * dr_n + 0.4 * ns)
    return clamp01(0.4 * dr_n + 0.3 * ns + 0.3 * clamp01(item_discrimination))


def transfer_gain(baseline: Sequence[float], trained: Sequence[float], weights: Sequence[float] | None = None) -> float:
    if len(baseline) != len(trained) or not baseline:
        raise ValueError("baseline and trained transfer results must align")
    if weights is None:
        weights = [1.0 / len(baseline)] * len(baseline)
    if len(weights) != len(baseline):
        raise ValueError("weights must align")
    gains = [max(-1.0, min(1.0, (t - b) / max(1.0 - b, EPS))) for b, t in zip(baseline, trained)]
    wsum = sum(weights)
    return sum(w * g for w, g in zip(weights, gains)) / max(wsum, EPS)


def transfer_yield(baseline: Sequence[float], trained: Sequence[float], cost: float, reference_cost: float = 1.0, alpha: float = 1.0) -> tuple[float, float]:
    if cost <= 0 or reference_cost <= 0:
        raise ValueError("costs must be positive")
    tg = transfer_gain(baseline, trained)
    raw = tg / (cost / reference_cost)
    ty = 1.0 / (1.0 + math.exp(-alpha * raw))
    return ty, raw


def attribution(cause_accuracy: float, temporal_localization: float, evidence_completeness: float, counterfactual_attribution: float | None = None) -> float:
    if counterfactual_attribution is None:
        return clamp01(0.45 * cause_accuracy + 0.25 * temporal_localization + 0.30 * evidence_completeness)
    return clamp01(0.35 * cause_accuracy + 0.20 * temporal_localization + 0.20 * evidence_completeness + 0.25 * counterfactual_attribution)


def contamination_resistance(instance_novelty: float, structural_novelty: float, procedural_generation: float, leakage_resistance: float) -> float:
    return clamp01(0.25 * instance_novelty + 0.25 * structural_novelty + 0.30 * procedural_generation + 0.20 * leakage_resistance)


def cost_efficiency(qualified_episodes: int, cost: float, reference_episodes_per_cost: float) -> tuple[float, float]:
    if cost <= 0 or reference_episodes_per_cost <= 0:
        raise ValueError("positive cost and reference required")
    ee = qualified_episodes / cost
    ce = clamp01(math.log1p(ee) / math.log1p(reference_episodes_per_cost))
    return ce, ee


@dataclass(frozen=True)
class ScoreInputs:
    cn: float
    vf: float
    sr: float
    dp: float
    ty: float
    at: float
    cr: float
    ce: float


def score_envq(inputs: ScoreInputs) -> EnvQScoreVector:
    return EnvQScoreVector(*(clamp01(v) for v in (inputs.cn, inputs.vf, inputs.sr, inputs.dp, inputs.ty, inputs.at, inputs.cr, inputs.ce)))


def geometric_mean(values: Iterable[float]) -> float:
    vals = list(values)
    if not vals:
        raise ValueError("values required")
    if any(v < 0 for v in vals):
        raise ValueError("non-negative values required")
    if any(v == 0 for v in vals):
        return 0.0
    return math.exp(sum(math.log(v) for v in vals) / len(vals))


def derived_scores(q: EnvQScoreVector) -> dict[str, float | bool]:
    integrity = geometric_mean([q.capability_necessity, q.verifier_fidelity, q.shortcut_resistance])
    learning_yield = geometric_mean([q.transfer_yield, q.attribution, q.cost_efficiency])
    benchmark_quality = geometric_mean([q.discriminative_power, q.contamination_resistance, q.verifier_fidelity])
    qualified = q.verifier_fidelity >= 0.90 and q.capability_necessity >= 0.50 and q.shortcut_resistance >= 0.60
    return {"Integrity": integrity, "LearningYield": learning_yield, "BenchmarkQuality": benchmark_quality, "Qualified": qualified}
