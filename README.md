# EnvQ

**EnvQ is a benchmark for measuring learning environment quality, not agent performance.**

It evaluates whether an environment produces **causal, trustworthy, attributable, transferable learning signal per unit cost** across synthetic, web, desktop, coding, and controlled decision environments.

> A good learning environment does not merely make success measurable; it makes the right capability necessary.

## Why EnvQ

Most agent benchmarks rank models inside a fixed environment. EnvQ flips the question:

\[
\textbf{Which environments actually produce high-quality learning?}
\]

An environment can be realistic, difficult, and fully verifiable while still producing weak learning because of shortcuts, reward hacking, contamination, poor attribution, or environment-specific overfitting.

EnvQ therefore evaluates the **environment itself**.

## EnvQ quality vector

Each environment is scored on eight primary dimensions:

| Metric | Question |
|---|---|
| **Capability Necessity (CN)** | Does success require the intended capability? |
| **Verifier Fidelity (VF)** | Does reward match true task success? |
| **Shortcut Resistance (SR)** | Does performance survive semantics-preserving perturbations? |
| **Discriminative Power (DP)** | Does the environment distinguish capability levels without floor/ceiling effects? |
| **Transfer Yield (TY)** | Does learning transfer to independent environments? |
| **Attribution (AT)** | Can we identify why success or failure occurred? |
| **Contamination Resistance (CR)** | Is performance protected from leakage, memorization, and benchmark familiarity? |
| **Cost Efficiency (CE)** | How much qualified learning signal is produced per unit cost? |

The canonical profile is:

\[
Q(E)=[CN,VF,SR,DP,TY,AT,CR,CE]
\]

EnvQ reports this vector directly. A single scalar score is secondary and must never hide a critical failure in verifier integrity, shortcut resistance, or contamination.

## Core evaluation protocol

For a fixed learner \(M_0\), learning algorithm \(L\), and budget \(B\):

\[
M_0 \xrightarrow[E]{L,B} M_E
\]

The trained learner is then frozen and evaluated on held-out environments \(H_1,\dots,H_n\):

\[
T_{ij}=P(M_{E_i},H_j)-P(M_0,H_j)
\]

The central quantity is not in-environment reward. It is **transferable capability gain under controlled cost**.

A practical form is:

\[
\text{Learning Yield}(E)=
\frac{\Delta \text{OOD capability}}{\text{interaction, token, and economic cost}}
\]

## v0.1 environment families

EnvQ v0.1 is designed to compare several distinct environment philosophies:

- **Phantom-style synthetic worlds** — procedurally generated fictional tasks with deterministic ground truth.
- **AgentGym-style multi-environment training** — heterogeneous interactive task families under a common agent interface.
- **WebArena-style web environments** — reproducible functional web workflows.
- **OSWorld-style computer-use environments** — real desktop applications and long-horizon cross-app workflows.
- **SWE-bench-style coding environments** — repository issues verified through executable tests.
- **Controlled DLM environments** — deterministic decision worlds for evidence aggregation, contradiction resolution, admissibility, abstention, authority ordering, provenance, and search-budget allocation.

The initial implementation focuses on a small executable core plus thin adapters to upstream environments rather than vendoring large external repositories.

## Hard qualification gates

An environment is not considered qualified merely because it produces a score.

Suggested v0.1 gates:

\[
VF \ge 0.90
\]

\[
CN \ge 0.50
\]

\[
SR \ge 0.60
\]

and

\[
\text{false-positive reward rate} < 5\%
\]

Environments that fail a hard gate remain visible for research, but are marked **UNQUALIFIED**.

## Derived views

EnvQ supports multiple views rather than one universal rank.

### Integrity

\[
I_E=(CN\cdot VF\cdot SR)^{1/3}
\]

### Learning yield

\[
LY_E=(TY\cdot AT\cdot CE)^{1/3}
\]

### Benchmark quality

\[
BQ_E=(DP\cdot CR\cdot VF)^{1/3}
\]

## Effective Learning Density

EnvQ also tracks an experimental quantity:

\[
ELD(E)=
\frac{
\text{Novelty}\times
\text{Attribution}\times
\text{Capability Necessity}\times
\text{Transferability}
}{
\text{Experience Cost}
}
\]

This is intentionally **not** an official ranking metric in v0.1. Its components should remain separately observable until empirical evidence shows that the composite predicts downstream learning.

## Budget regimes

Environment comparisons should be reported under at least three controlled budgets:

- **Interaction-matched** — same number of qualified environment interactions.
- **Token-matched** — same learner-visible token budget.
- **Cost-matched** — same total economic/compute budget.

An environment may rank differently under each regime; EnvQ does not merge them into one opaque number.

## Planned repository structure

\`\`\`text
envq/
├── envq/
│   ├── schema/          # canonical episode and environment records
│   ├── scoring/         # CN, VF, SR, DP, TY, AT, CR, CE
│   ├── adapters/        # upstream environment adapters
│   ├── perturbations/   # lexical, structural, interface, distractor tests
│   └── transfer/        # cross-environment evaluation
├── baselines/
│   ├── phantom/
│   ├── dlm/
│   └── swe/
├── tests/
├── docs/
└── THIRD_PARTY.md
\`\`\`

## Research questions

EnvQ is designed to test several hypotheses:

1. Does **Capability Necessity × Verifier Fidelity × Attribution** predict OOD learning yield?
2. Can causally clean synthetic environments outperform more realistic but noisy environments on transferable learning per dollar?
3. Which forms of shortcut resistance best predict real-world transfer?
4. How much environment diversity is needed before learning becomes harness-invariant?
5. When does higher realism improve learning, and when does it merely increase cost and confounding?
6. Can environment quality become a measurable scaling variable independent of model size?

## Design principle

EnvQ treats a learning environment as part of the intelligence production system rather than as a passive benchmark.

The target is therefore not:

\[
\text{more experience}
\]

but:

\[
\boxed{\text{more qualified experience per unit cost}}
\]

## Status

**v0.1 — bootstrap**

Current priorities:

- canonical \`EnvQEpisodeRecord\`;
- executable implementations of the eight metrics;
- Phantom-style and controlled-DLM reference environments;
- SWE-bench-compatible adapter;
- capability-ablation runner;
- perturbation suite;
- cross-environment transfer matrix;
- reproducible cost accounting.

## Contributing

EnvQ is intended to be an open research benchmark. Contributions are welcome for:

- new environment adapters;
- verifier audits;
- shortcut probes;
- perturbation families;
- transfer suites;
- reproducibility studies;
- alternative scoring formulations.

Environment submissions should expose enough evidence to audit reward correctness, task provenance, cost, and failure attribution.

## License

Core EnvQ code is intended to be released under the MIT License.

Third-party environments and datasets remain governed by their original licenses. EnvQ should prefer adapters and pinned upstream references over copying external repositories.
