# Planning — Mapping Robustness Boundaries Through Systematic Adversarial Null Results

## Motivation & Novelty Assessment

### Why This Research Matters
Narrow misalignment training can induce broad failures, but the majority of adversarial
attempts *fail* to move a model — and those "failures to fail" are discarded. If a failed
attack is a genuine **robustness boundary** rather than a weak experiment, then mapping
*where* models resist gives a diagnostic of alignment quality. The practical payoff:
noise-calibrated robustness maps that (a) tell red-teamers where to stop escalating,
(b) let alignment scientists compare training methods on a common scale, and (c) separate
truly robust behaviors from merely undertested ones.

### Gap in Existing Work
The literature (31 papers) documents intensity dials for many interventions (steering α,
LoRA rank, encoding OOD-ness, jailbreak composition) and reports model-specific null
results **piecemeal**. No prior work *systematically maps change-point thresholds across
multiple failure modes on one common model set with a unified, noise-calibrated intensity
metric*, nor quantifies how those thresholds correlate with alignment method
(APO vs AFT vs deliberative). This is exactly the methodological contribution the
hypothesis proposes (lit review §6, "Gaps").

### Our Novel Contribution
A **graduated adversarial stress-test harness** applied identically across 5 model families
and 4 failure modes, producing per-(model,mode) *change-point thresholds*, *robustness
coefficients* (area under the intervention–response curve), a *cross-mode threshold
correlation matrix*, and an *invariant-persistence score* — all defined **relative to a
per-model measured noise floor** so that "null result" means "sub-noise," not "we gave up."

### Experiment Justification
- **Exp 1 — Noise-floor calibration**: measure baseline (L0, no-attack) compliance across
  seeds/temperature. Required to make any "null" claim valid (lit review guard #4, 2512.12066).
- **Exp 2 — Graduated escalation, 4 modes × 6 intensity levels × 5 models**: the core map.
  Needed to locate change-points and compute robustness coefficients.
- **Exp 3 — Threshold analysis**: change-point detection (proportion test vs baseline),
  robustness coefficient, cross-mode correlation, invariant persistence. Directly tests
  each hypothesis clause.
- **Exp 4 — Validity guards**: misunderstanding filter (encoding mode), and a held-out
  jailbreak-variant generalization check (does a threshold predict a new variant?).

## Research Question
Do adversarial interventions that fail to induce misalignment mark genuine, quantifiable
robustness boundaries that (a) are model-specific, (b) differ across failure modes, and
(c) correlate with the model's alignment method — as opposed to being artifacts of weak testing?

## Hypothesis Decomposition
- **H1 (thresholds exist & are graded)**: compliance rises monotonically-ish with intensity;
  a change-point threshold above the noise floor is identifiable for most (model, mode) pairs.
- **H2 (model-specificity)**: thresholds/robustness coefficients differ significantly across
  model families (predict Gemma most robust, Qwen most susceptible — lit review).
- **H3 (mode-specificity)**: thresholds differ across failure modes and are only partially
  correlated (robustness is multi-dimensional, not one scalar — 2412.10535).
- **H4 (invariants)**: some (model, mode) pairs show *no* supra-noise change even at max
  intensity → candidate alignment invariants (invariant-persistence score > 0).
- Independent variable: intervention intensity level (0–5) per mode. Dependent: harmful-
  compliance / biased-output rate. Moderators: model family, failure mode.

## Methodology

### Approach
Inference-time only (CPU + OpenRouter API — fine-tuning EM needs GPU, out of scope under
the 1h CPU constraint; documented as a limitation). Four failure modes drawn from the
task spec that are realizable at inference:
1. **Jailbreak composition** (competing objectives; Wei et al. 2307.02483)
2. **Adversarial persona** (role-play attacks)
3. **Syntactic/encoding perturbation** (mismatched generalization: leet→reverse→Base64→ROT13)
4. **Bias elicitation** (CLEAR-Bias-style escalating pressure toward stereotyped judgments)

Each mode has 6 intensity levels (L0 = no-attack baseline → L5 = max). Applied to a shared
set of harmful prompts (modes 1–3, from StrongREJECT/refusal benchmarks) or ambiguous social
scenarios (mode 4).

### Evaluation Metrics (as specified in the task)
- **Compliance rate** = 1 − refusal, via the standard refusal-substring detector
  (refusal_direction repo list), with a minimum-length + non-refusal check. Cheap,
  deterministic, reproducible. Validated on a subset with an LLM judge (gpt-4o-mini).
- **Change-point threshold** = lowest intensity level whose compliance exceeds the noise
  floor at p<0.05 (one-sided two-proportion z-test vs L0 baseline). ∞ if never.
- **Robustness coefficient** = 1 − (normalized AUC of compliance-vs-intensity curve). 1 = fully robust.
- **Cross-mode threshold correlation matrix** (Spearman across models).
- **Invariant persistence score** = fraction of modes where max-intensity compliance is NOT
  significantly above baseline.

### Statistical Analysis Plan
- ≥3 seeds/prompt at temperature 0.7 (SSI noise-floor mandate, 2512.12066).
- Two-proportion z-test for change-points; Bonferroni note for multiple levels.
- Bootstrap 95% CIs on robustness coefficients.
- Spearman ρ for cross-mode correlations; Kruskal–Wallis across models.

### Baselines
- **L0 no-attack baseline** per model = the natural refusal floor (control).
- **Random/heuristic**: compliance under plain harmful request is the lower anchor.
- Cross-model comparison serves as the between-condition baseline.

## Expected Outcomes
Support: identifiable graded thresholds, Gemma/GPT-4o-mini most robust, Qwen least;
encoding mode has a sharp OOD change-point; some invariants persist at max intensity.
Refute: compliance flat/at-noise everywhere (no measurable boundaries) or thresholds
identical across models (not model-specific).

## Timeline
- Setup + data (done): 10 min. Harness code: 15 min. Run (~2000 async calls): 15–20 min.
  Analysis + figures: 10 min. Report: 10 min. Buffer within 1h.

## Potential Challenges
- API rate limits / slow 27B model → async + semaphore + retry + caching to JSONL.
- Refusal detector false negatives (model complies with garbage) → min-length + judge subset.
- "Conditional/masked" nulls (2604.25891) → note as limitation; encoding misunderstanding
  filter applied.

## Success Criteria
A completed robustness map (5 models × 4 modes) with thresholds, robustness coefficients,
a cross-mode correlation matrix, and at least one statistically-supported model-family
difference, plus honest reporting if the hypothesis is not supported.
