# EnvQ v0.1 scoring

EnvQ reports an eight-dimensional vector rather than treating a scalar rank as primary:

\`Q(E) = [CN, VF, SR, DP, TY, AT, CR, CE]\`

- **CN — Capability Necessity:** normalized reward collapse after target-capability ablation, accompanied by the absolute necessity gap.
- **VF — Verifier Fidelity:** asymmetric verifier agreement, with false-positive rewards weighted more heavily than false negatives.
- **SR — Shortcut Resistance:** semantic-performance retention under lexical, structural, interface, and distractor perturbations.
- **DP — Discriminative Power:** model performance dynamic range plus non-saturation and, when available, item-response discrimination.
- **TY — Transfer Yield:** held-out normalized headroom gain per reference-normalized cost; raw transfer gain remains authoritative.
- **AT — Attribution:** cause identification, temporal localization, evidence completeness, and counterfactual confirmation.
- **CR — Contamination Resistance:** instance novelty, structural novelty, post-hoc/procedural generation, and leakage audit resistance.
- **CE — Cost Efficiency:** qualified episodes/steps/tokens per full-stack cost. Transfer gain per dollar is reported separately.

Hard qualification gates in v0.1: \`VF >= .90\`, \`CN >= .50\`, \`SR >= .60\`; false-positive reward rate is separately required to be \`< 5%\` by the benchmark runner once audit counts are available.
