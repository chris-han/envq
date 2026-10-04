from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence


@dataclass(frozen=True)
class CostRecord:
    model_usd: float = 0.0
    environment_usd: float = 0.0
    verifier_usd: float = 0.0
    human_usd: float = 0.0
    infra_usd: float = 0.0
    reset_usd: float = 0.0
    storage_usd: float = 0.0

    @property
    def total_usd(self) -> float:
        return sum((self.model_usd, self.environment_usd, self.verifier_usd,
                    self.human_usd, self.infra_usd, self.reset_usd, self.storage_usd))


@dataclass(frozen=True)
class EnvQEpisodeRecord:
    environment: str
    environment_version: str
    task_id: str
    capability: str
    reward: float
    reference_reward: float | None = None
    success: bool | None = None
    reference_success: bool | None = None
    observations: Sequence[Any] = field(default_factory=tuple)
    actions: Sequence[Any] = field(default_factory=tuple)
    tool_outputs: Sequence[Any] = field(default_factory=tuple)
    reward_components: Mapping[str, float] = field(default_factory=dict)
    verifier_evidence: Mapping[str, Any] = field(default_factory=dict)
    termination_cause: str | None = None
    failure_cause: str | None = None
    reference_failure_cause: str | None = None
    predicted_failure_step: int | None = None
    reference_failure_step: int | None = None
    required_provenance_fields_present: int = 0
    required_provenance_fields_total: int = 9
    qualified_steps: int = 0
    learner_visible_tokens: int = 0
    contaminated: bool = False
    infrastructure_failure: bool = False
    costs: CostRecord = field(default_factory=CostRecord)
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class EnvQScoreVector:
    capability_necessity: float
    verifier_fidelity: float
    shortcut_resistance: float
    discriminative_power: float
    transfer_yield: float
    attribution: float
    contamination_resistance: float
    cost_efficiency: float

    def as_dict(self) -> dict[str, float]:
        return {
            "CN": self.capability_necessity,
            "VF": self.verifier_fidelity,
            "SR": self.shortcut_resistance,
            "DP": self.discriminative_power,
            "TY": self.transfer_yield,
            "AT": self.attribution,
            "CR": self.contamination_resistance,
            "CE": self.cost_efficiency,
        }
