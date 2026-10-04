from __future__ import annotations
from dataclasses import dataclass
import random
from typing import Iterable
from envq.schema import EnvQEpisodeRecord
from .base import EnvironmentAdapter


@dataclass(frozen=True)
class PhantomTask:
    task_id: str
    edges: tuple[tuple[str, str], ...]
    start: str
    target: str


def generate_task(task_id: str, hops: int = 4, seed: int = 0) -> PhantomTask:
    rng = random.Random(f"{seed}:{task_id}")
    nodes = [f"entity_{rng.randrange(10**9):09d}" for _ in range(hops + 1)]
    return PhantomTask(task_id, tuple(zip(nodes, nodes[1:])), nodes[0], nodes[-1])


def oracle(task: PhantomTask) -> bool:
    nxt = {a: b for a, b in task.edges}
    node = task.start
    seen = set()
    while node in nxt and node not in seen:
        seen.add(node)
        node = nxt[node]
    return node == task.target


class PhantomStyleAdapter(EnvironmentAdapter):
    """Independent minimal fictional-world baseline inspired by PhantomEnvironments.

    This is not copied from the paper authors' implementation.
    """
    name = "phantom-style"

    def run(self, task_ids: Iterable[str]) -> list[EnvQEpisodeRecord]:
        records = []
        for task_id in task_ids:
            task = generate_task(task_id)
            success = oracle(task)
            records.append(EnvQEpisodeRecord(
                environment=self.name,
                environment_version="0.1",
                task_id=task_id,
                capability="multi-hop-composition",
                reward=float(success),
                reference_reward=1.0,
                success=success,
                reference_success=True,
                observations=task.edges,
                actions=("follow-relations",),
                verifier_evidence={"target": task.target, "reachable": success},
                termination_cause="oracle",
                required_provenance_fields_present=9,
                qualified_steps=len(task.edges),
            ))
        return records
