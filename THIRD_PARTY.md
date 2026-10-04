# Third-party environments

EnvQ v0.1 does not vendor the upstream benchmark source trees. Adapters should pin an upstream commit/release and preserve that project's license and citation requirements.

| Environment | Upstream | License observed for v0.1 integration | EnvQ strategy |
|---|---|---|---|
| AgentGym | WooooDyy/AgentGym | MIT | thin \`agentenv\` bridge; no vendored source |
| OSWorld | xlang-ai/OSWorld | Apache-2.0 | thin \`desktop_env\` bridge; no vendored source |
| SWE-bench | SWE-bench/SWE-bench | MIT | thin evaluation-harness bridge; no vendored source |
| WebArena | web-arena-x/webarena | upstream license must be pinned before redistributing code | metadata/runtime bridge only in v0.1 |
| PhantomEnvironments | arXiv:2609.40221 | paper concept only in v0.1 | independent minimal generator; not copied from authors' code |

Before enabling any vendored fixture or source copy, add the exact upstream commit, file-level provenance, license text, and redistribution rationale here.
