from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Iterable
from envq.schema import EnvQEpisodeRecord


class EnvironmentAdapter(ABC):
    """Map an upstream environment into canonical EnvQ episode records."""

    name: str

    @abstractmethod
    def run(self, task_ids: Iterable[str]) -> list[EnvQEpisodeRecord]:
        raise NotImplementedError
