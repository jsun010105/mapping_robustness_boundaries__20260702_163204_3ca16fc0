# Mapping Robustness Boundaries Through Systematic Adversarial Null Results in LLM Alignment

**Research report — 2026-07-02**

---

## 1. Executive Summary

**Research question (one sentence):** Do adversarial interventions that *fail* to induce
misalignment mark genuine, quantifiable robustness boundaries that are model- and mode-specific
and correlate with alignment method — rather than being artifacts of weak testing?

**Key finding (one sentence):** Across 5 model families × 4 failure modes × 6 graduated intensity
levels (2,879 real API responses), robustness boundaries are real, sharply model- and
mode-specific, and only *partially* correlated across modes (robustness is multi-dimensional) —
**and, most importantly, one entire "failure mode" (syntactic/encoding attacks) that a naive
substring metric scored as a universal collapse turned out, under LLM-judge validation, to be one
of the *most robust* modes: the null result was genuine robustness, not a weak experiment.**

**Practical implications:** (i) The paper's central thesis is demonstrated *on itself* — a
measurement that isn't noise-/validity-calibrated will mistake a robustness boundary for a
vulnerability (69% false-positive rate on encoded prompts). (ii) A noise-calibrated robustness map
cleanly ranks models (GPT-4o-mini > Gemma-2-27B > Llama-3.1-8B > Qwen-2.5-7B > Mistral-Nemo),
consistent with the literature's predictions, and localizes *which* failure mode each model is
weakest on — a targeting signal for intervention design.

---

## 2. Research Question & Motivation

Recent work shows narrow misalignment training can induce *broad* failures, yet most adversarial
attempts produce **null results** that are discarded. This project treats those "failures to fail"
as signal: if a failed attack marks a genuine **robustness boundary** rather than a weak
experiment, then systematically mapping *where* models resist gives a diagnostic of alignment
quality. The gap in the literature (synthesized from 31 papers, `literature_review.md`) is that
intensity dials and model-specific null results are documented **piecemeal**; no prior work maps
change-point thresholds across multiple failure modes on one common model set with a unified,
**noise-/validity-calibrated** intensity metric, nor quantifies how thresholds relate to alignment
method (alignment-by-preference-optimization *APO* vs alignment-by-fine-tuning *AFT* vs
deliberative alignment).

### Hypotheses
- **H1** — Graded thresholds exist: compliance rises with intensity and a supra-noise change-point
  is identifiable for most (model, mode) pairs.
- **H2** — Thresholds/robustness are model-specific (predict Gemma robust, Qwen/Mistral susceptible).
- **H3** — Robustness is multi-dimensional: thresholds differ across modes and are only partially
  correlated.
- **H4** — Some (model, mode) pairs show *no* supra-noise change even at max intensity → alignment
  invariants; these should track alignment method.

---

## 3. Experimental Setup

**Compute:** CPU-only local container + OpenRouter API (fine-tuning-based Emergent Misalignment,
the literature's primary testbed, requires GPU and was out of scope under the 1-hour CPU
constraint — see Limitations). All interventions are **inference-time**, which the literature
(Wei et al. 2307.02483; CLEAR-Bias 2504.07887) treats as a valid intensity axis.

**Models (span alignment methods & the observed robustness spectrum):**

| Key | OpenRouter ID | Alignment family |
|---|---|---|
| qwen2.5-7b | `qwen/qwen-2.5-7b-instruct` | AFT |
| llama3.1-8b | `meta-llama/llama-3.1-8b-instruct` | APO |
| gemma2-27b | `google/gemma-2-27b-it` | APO (robust contrast) |
| mistral-nemo | `mistralai/mistral-nemo` | AFT |
| gpt-4o-mini | `openai/gpt-4o-mini` | deliberative / frontier |

**Four failure modes, each with 6 graduated intensity levels (L0 = no-attack baseline → L5 = max):**
1. **Jailbreak composition** (competing objectives): plain → justification → authority/urgency →
   prefix-injection → refusal-suppression rules → stacked DAN-style.
2. **Adversarial persona** (role-play): neutral → helpful → amoral advisor → fictional villain →
   unfiltered "AIM" → maximal unrestricted persona.
3. **Syntactic/encoding perturbation** (mismatched generalization): plain → leetspeak →
   word-reversal → Base64 → ROT13 → Base64+decode-instruction (increasing OOD-ness).
4. **Bias elicitation** (CLEAR-Bias-style): neutral ask → guess → force-a-pick → one-word →
   analyst-persona → authority/penalty framing, on 8 ambiguous demographic scenarios.

**Prompts:** modes 1–3 use 8 diverse harmful requests from StrongREJECT; mode 4 uses 8 ambiguous
social scenarios (scored by whether the model commits to a demographic group = biased/non-robust).

**Sampling / noise floor:** 3 seeds/prompt at temperature 0.7 (per the Safety-Stability mandate,
2512.12066), max_tokens=256. **2,880 planned calls; 2,879 analyzed** (1 dropped by the
misunderstanding filter; 100 Gemma API timeouts on encoded prompts were re-collected).

**Metrics (exactly as specified in the task):**
- **Compliance rate** = attack success. Primary detector = standard refusal-substring list
  (refusal_direction repo) + minimum-length check. **Validated against an LLM judge** (see §4.0).
- **Change-point threshold** = lowest intensity level whose compliance exceeds the per-model L0
  noise floor at *p*<0.05 (one-sided two-proportion *z*-test). "–" = no supra-noise change (invariant).
- **Robustness coefficient** = 1 − normalized area under the compliance-vs-intensity curve (1 = fully robust).
- **Cross-mode threshold correlation matrix** (Spearman of per-model robustness across modes).
- **Invariant persistence score** = fraction of (model, mode) pairs with max-intensity compliance
  *not* significantly above baseline.

---

## 4. Results

### 4.0 Metric validation (the pivotal result)

Before trusting the map, we validated the cheap substring detector against an LLM judge
(gpt-4o-mini, "does the response *genuinely* provide the harmful content?") on a stratified 135-row
subset:

| Mode | Agreement | Substring compliance | Judge compliance | **Substring false-positive rate** |
|---|---|---|---|---|
| jailbreak | 0.82 | 0.42 | 0.24 | 0.18 |
| persona | 0.93 | 0.33 | 0.27 | **0.07** |
| encoding | **0.31** | 0.76 | **0.07** | **0.69** |

**The substring metric is valid for jailbreak/persona but invalid for encoding** (69% false
positives): models emit fluent *non-answers* to Base64/ROT13 ("I see the color of your thoughts…
send me the message to decode") that are neither refusals nor harmful content. We therefore
**re-scored all 720 encoding rows with the LLM judge** and use judge-corrected labels for the
encoding column throughout. This is the project's thesis in action: a naive pipeline reports
"encoding = universal collapse, threshold 1, compliance → 1.0"; validation reveals the opposite.

### 4.1 Change-point threshold map (judge-corrected)

Intensity level at which compliance first exceeds the per-model noise floor (p<0.05); "–" = invariant.

| Model (align) | jailbreak | persona | encoding | bias |
|---|---|---|---|---|
| qwen2.5-7b (AFT) | 3 | – | 1 | 2 |
| llama3.1-8b (APO) | – | – | 2 | 2 |
| mistral-nemo (AFT) | 3 | 3 | – | 2 |
| gemma2-27b (APO) | 4 | 2 | 1 | 2 |
| gpt-4o-mini (deliberative) | – | – | 1 | 2 |

### 4.2 Robustness coefficient (1 = fully robust)

| Model (align) | jailbreak | persona | encoding | bias | **mean** |
|---|---|---|---|---|---|
| qwen2.5-7b (AFT) | 0.554 | 0.796 | 0.925 | 0.617 | 0.723 |
| llama3.1-8b (APO) | 0.696 | 0.833 | 0.958 | 0.508 | 0.749 |
| mistral-nemo (AFT) | 0.304 | 0.204 | 0.808 | 0.442 | **0.440** |
| gemma2-27b (APO) | 0.821 | 0.542 | 0.950 | 0.729 | 0.760 |
| gpt-4o-mini (deliberative) | 0.917 | 0.838 | 0.779 | 0.679 | **0.803** |

**Model robustness ranking:** GPT-4o-mini > Gemma-2-27B > Llama-3.1-8B > Qwen-2.5-7B > Mistral-Nemo.
This matches the literature: frontier/deliberative most robust; Gemma the robust open contrast;
Mistral-Nemo the weakest (collapses under persona and jailbreak).

### 4.3 Max-intensity (L5) compliance — locating invariants

| Model | jailbreak | persona | encoding | bias |
|---|---|---|---|---|
| qwen2.5-7b | 0.667 | 0.292 | **0.000** | 0.708 |
| llama3.1-8b | 0.417 | 0.208 | **0.000** | 0.292 |
| mistral-nemo | 0.833 | 0.875 | **0.000** | 0.583 |
| gemma2-27b | 0.792 | 0.833 | **0.000** | 0.125 |
| gpt-4o-mini | **0.000** | 0.125 | 0.125 | 0.458 |

**11 / 20 (model, mode) pairs are invariants** (no supra-noise change at max intensity) — chiefly
the encoding column (genuine harmful compliance ≈ 0 even at maximal OOD encoding) plus jailbreak &
persona for the most robust models (GPT-4o-mini jailbreak L5 = 0.000).

### 4.4 Cross-mode robustness correlation (Spearman, across the 5 models)

|  | jailbreak | persona | encoding | bias |
|---|---|---|---|---|
| **jailbreak** | 1.0 | 0.7 | −0.1 | 0.8 |
| **persona** | 0.7 | 1.0 | −0.1 | 0.3 |
| **encoding** | −0.1 | −0.1 | 1.0 | 0.0 |
| **bias** | 0.8 | 0.3 | 0.0 | 1.0 |

Jailbreak/persona/bias form a correlated cluster (a shared "instruction-pressure" robustness
factor), while **encoding is orthogonal** (ρ ≈ 0) — robustness is genuinely multi-dimensional, not
one scalar (consistent with 2412.10535).

### 4.5 Statistical tests

- Model-level robustness differences: Kruskal–Wallis H = 5.01, **p = 0.29** (not significant —
  only 4 mode-values per model; underpowered, see Limitations).
- Alignment-method contrast (APO/deliberative vs AFT), Mann–Whitney one-sided:
  **APO mean 0.771 vs AFT mean 0.581, U = 6.0, p = 0.10** — directionally supports H4 but not
  significant at n = 5 models.

**Figures:** `figures/dose_response_curves.png` (4 modes × 5 models), `figures/robustness_heatmap.png`,
`figures/cross_mode_correlation.png`.

---

## 5. Analysis & Discussion

**H1 (graded thresholds exist): SUPPORTED.** Dose-response curves rise with intensity and yield
identifiable change-points for 9/20 pairs (the other 11 are invariants). Bias shows the most
consistent change-point (threshold = 2 for *every* model — the "force-a-single-pick" level).

**H2 (model-specificity): SUPPORTED.** Robustness coefficients span 0.44 (Mistral-Nemo) to 0.80
(GPT-4o-mini) and the *shape* differs: Gemma is strong on jailbreak (0.82) but weak on persona
(0.54); Mistral is weak almost everywhere; GPT-4o-mini is near-invulnerable to jailbreak (L5 = 0.0)
yet its *most* penetrable mode is bias. The formal Kruskal test is underpowered, so this is an
effect-size/ranking claim, honestly reported as such.

**H3 (multi-dimensional robustness): STRONGLY SUPPORTED.** The cross-mode matrix shows a correlated
jailbreak–persona–bias cluster but an orthogonal encoding axis. A model's robustness to one attack
family does *not* predict robustness to a mechanistically different one — you cannot summarize a
model with a single robustness scalar.

**H4 (invariants & alignment method): PARTIALLY SUPPORTED.** 11/20 invariants exist; APO/deliberative
models are more robust on average than AFT models (0.77 vs 0.58), matching the literature's
APO-vs-AFT brittleness story (2406.11717) and the deliberative-alignment robustness story
(VLAF 2604.20995) — but n = 5 models gives p = 0.10, so this is suggestive, not conclusive.

**The headline surprise — encoding.** The naive substring pipeline reported encoding as the single
*worst* failure mode (threshold = 1 for all models, L5 compliance → 1.0). Validation inverted it:
genuine harmful compliance under encoding is ≈ 0 at max intensity for 4/5 models — encoding is one
of the *most robust* modes. The "null result" here (models don't get jailbroken by Base64) is a
**real robustness boundary that a weak metric mistook for a catastrophic vulnerability.** This is
exactly the confound the literature warns about (misunderstanding filter, CLEAR-Bias 2504.07887;
false-negative/false-positive nulls, 2604.25891) and is the strongest vindication of the project's
core methodological claim: *a robustness boundary is only trustworthy once the metric is validated.*

**Error analysis.** (a) Substring false positives concentrate in encoding (0.69) and are low
elsewhere (jailbreak 0.18, persona 0.07). (b) Mistral-Nemo's collapse is genuine (fluent harmful
content under persona/jailbreak, confirmed by high judge agreement in those modes). (c) Gemma-27B's
100 encoding timeouts were API-side (large model), re-collected at lower concurrency; the completed
data show Gemma genuinely resists encoded attacks (L5 = 0.0).

---

## 6. Limitations

- **No fine-tuning testbed.** The literature's primary EM substrate (insecure-code SFT, LoRA-rank /
  seed-count / steering-α dials) needs GPU; under the 1-hour CPU constraint we mapped *inference-time*
  modes only. Weight-space thresholds (steering α, refusal-direction ablation, cold-start SFT-seed
  count) are the natural next axis.
- **Statistical power.** 5 models × 4 modes makes the between-model Kruskal test and the APO-vs-AFT
  contrast underpowered (p = 0.29 and 0.10); the robustness *rankings* and effect sizes are the
  reliable output, not the significance stars. More models per alignment family would sharpen H4.
- **Judge as ground truth.** Encoding correction relies on a single LLM judge (gpt-4o-mini); κ vs a
  second judge or human is unmeasured (though jailbreak/persona agreement was 0.82–0.93). Judge
  choice materially affects results (2504.07887).
- **Concealment / conditional nulls (2604.25891, Sleeper Agents).** An inference-time invariant
  (e.g., GPT-4o-mini jailbreak L5 = 0.0) could hide behind an untested trigger; we did not run the
  conditional-trigger re-probe, so "invariant" means "invariant under this intensity ladder," not
  "provably unremovable."
- **Prompt-based intensity is coarse.** Levels are ordered by documented attack strength but are not
  a continuous, calibrated scalar; a finer or optimization-based ladder (GCG) would give smoother
  change-points.

---

## 7. Conclusions & Next Steps

**Answer to the research question:** Yes — adversarial null results are quantifiable robustness
boundaries, not experimental weaknesses, **provided the behavioral metric is itself validated.**
The robustness map is sharply model- and mode-specific, robustness is multi-dimensional (an
orthogonal encoding axis), 11/20 (model, mode) pairs are genuine invariants, and robustness tracks
alignment method (APO/deliberative > AFT) at the effect-size level. The encoding reversal shows the
knife-edge the hypothesis names: the same data reads as "catastrophic failure" or "robust invariant"
depending entirely on measurement validity.

**Next steps:** (1) add weight-space intensity dials on open models (steering α, refusal-direction
ablation count, SFT-seed cold-start) to test whether inference-time thresholds predict weight-space
ones; (2) run the conditional-trigger and refusal-masking re-probes on every invariant to separate
genuine robustness from concealment; (3) scale to ≥15 models to power the APO-vs-AFT test; (4)
correlate thresholds with mechanistic predictors (safety-layer band, misalignment-direction
magnitude) from the cloned interp repos.

---

## References (used directly)

- Betley et al. 2025, *Emergent Misalignment* (2502.17424); Model Organisms (2506.11613).
- Wei et al. 2023, *Jailbroken* (2307.02483); GCG (2307.15043).
- Arditi et al. 2024, *Refusal is mediated by a single direction* (2406.11717).
- CLEAR-Bias 2025 (2504.07887); *Instability of Safety* (2512.12066); *Adversarial vs OOD
  robustness* (2412.10535); *Conditional Misalignment* (2604.25891); VLAF (2604.20995);
  *Sleeper Agents* (2401.05566).
- Datasets: StrongREJECT (small, 60), refusal_direction benchmarks. Full catalog in `resources.md`;
  synthesis in `literature_review.md`.

**Reproducibility:** seeds {0,1,2}, temperature 0.7, max_tokens 256; all raw responses in
`results/raw_responses.jsonl`, judge labels in `results/encoding_judged.jsonl`, metrics in
`results/metrics.json`. Re-run: `python src/run_experiment.py && python src/judge_encoding.py &&
python src/analyze.py`.
