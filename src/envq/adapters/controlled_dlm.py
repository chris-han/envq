from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable
from envq.schema import EnvQEpisodeRecord
from .base import EnvironmentAdapter


@dataclass(frozen=True)
class DecisionCase:
    task_id: str
    authority: dict[str, int]
    evidence: dict[str, bool]
    expected: str


CASES = {
    "authority-conflict": DecisionCase(
        "authority-conflict",
        authority={"policy": 3, "memo": 1},
        evidence={"policy_allows": False, "memo_allows": True},
        expected="REJECT",
    ),
    "unknown-missing-evidence": DecisionCase(
        "unknown-missing-evidence",
        authority={"policy": 3},
        evidence={},
        expected="NONE",
    ),
}


def deterministic_oracle(case: DecisionCase) -> str:
    if not case.evidence:
        return "NONE"
    if case.evidence.get("policy_allows") is False:
        return "REJECT"
    if case.evidence.get("policy_allows") is True:
        return "ADMIT"
    return "NONE"


class ControlledDLMAdapter(EnvironmentAdapter):
    name = "controlled-dlm"

    def run(self, task_ids: Iterable[str]) -> list[EnvQEpisodeRecord]:
        out = []
        for task_id in task_ids:
            case = CASES[task_id]
            decision = deterministic_oracle(case)
            success = decision == case.expected
            out.append(EnvQEpisodeRecord(
                environment=self.name,
                environment_version="0.1",
                task_id=task_id,
                capability="authority-aware-decision",
                reward=float(success),
                reference_reward=1.0,
                success=success,
                reference_success=True,
                observations=(case.evidence,),
                actions=(decision,),
                verifier_evidence={"oracle": case.expected},
                termination_cause="decision",
                required_provenance_fields_present=9,
                qualified_steps=1,
            ))
        return out
