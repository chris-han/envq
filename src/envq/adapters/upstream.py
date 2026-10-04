"""Metadata-only upstream adapters for EnvQ v0.1.

EnvQ intentionally depends on upstream packages/repositories instead of vendoring
large benchmark implementations. Concrete runtime bridges can be added behind
this metadata without copying source trees.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class UpstreamEnvironment:
    name: str
    repository: str
    license: str
    integration: str


UPSTREAM = {
    "agentgym": UpstreamEnvironment("AgentGym", "https://github.com/WooooDyy/AgentGym", "MIT", "agentenv adapter"),
    "osworld": UpstreamEnvironment("OSWorld", "https://github.com/xlang-ai/OSWorld", "Apache-2.0", "desktop_env adapter"),
    "webarena": UpstreamEnvironment("WebArena", "https://github.com/web-arena-x/webarena", "verify upstream LICENSE before redistribution", "browser_env adapter"),
    "swebench": UpstreamEnvironment("SWE-bench", "https://github.com/SWE-bench/SWE-bench", "MIT", "swebench harness adapter"),
}
