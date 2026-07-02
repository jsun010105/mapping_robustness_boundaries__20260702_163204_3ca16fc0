# Resources Catalog

Resources gathered for **Mapping Robustness Boundaries Through Systematic Adversarial Null Results in LLM Alignment**.

## Summary
- **Papers**: 31 (all arXiv PDFs, deep-read) in `papers/`
- **Datasets**: 6 groups (~33 MB) staged in `datasets/`, plus a documented on-demand list
- **Code repositories**: 6 cloned in `code/` (~264 MB)
- See `literature_review.md` for the full synthesis and experiment recommendations.

---

## Papers (31)
Detailed descriptions in `papers/README.md`; machine-readable metadata (title/authors/year/abstract/reason) in `papers/catalog.json`.

| # | arXiv | Year | Short title | Cluster |
|---|-------|------|-------------|---------|
| 1 | 2307.15043 | 2023 | GCG universal transferable attacks | Jailbreak foundations |
| 2 | 2307.02483 | 2023 | Jailbroken: how safety training fails | Jailbreak foundations |
| 3 | 2310.03693 | 2023 | Fine-tuning compromises safety | Jailbreak foundations |
| 4 | 2502.17424 | 2025 | Emergent Misalignment (seminal) | EM core |
| 5 | 2506.11613 | 2025 | Model Organisms for EM | EM core |
| 6 | 2602.07852 | 2026 | EM is Easy, Narrow is Hard | EM core |
| 7 | 2506.11618 | 2025 | Convergent Linear Representations of EM | EM core |
| 8 | 2507.03662 | 2025 | Re-Emergent Misalignment | EM core |
| 9 | 2508.06249 | 2026 | In-Training Defenses against EM | EM extensions |
| 10 | 2606.08682 | 2026 | Activation Steering Induces EM | EM extensions |
| 11 | 2604.25891 | 2026 | Conditional Misalignment (hidden EM) | EM extensions |
| 12 | 2605.31328 | 2026 | RL Amplifies EM from Harmless Rewards | EM extensions |
| 13 | 2602.00298 | 2026 | Domain-Level Susceptibility to EM | EM extensions |
| 14 | 2606.09068 | 2026 | EM via Sycophancy + Alignment Gating | EM extensions |
| 15 | 2406.11717 | 2024 | Refusal = single direction | Refusal/steering |
| 16 | 2602.02132 | 2026 | More to refusal than one direction | Refusal/steering |
| 17 | 2502.17420 | 2026 | Geometry of Refusal (concept cones) | Refusal/steering |
| 18 | 2505.23556 | 2025 | Understanding Refusal with SAEs | Refusal/steering |
| 19 | 2408.17003 | 2025 | Safety Layers in Aligned LLMs | Refusal/steering |
| 20 | 2401.05566 | 2024 | Sleeper Agents | Deception |
| 21 | 2412.14093 | 2024 | Alignment Faking | Deception |
| 22 | 2506.18032 | 2025 | Why Some LMs Fake Alignment | Deception |
| 23 | 2604.20995 | 2026 | VLAF value-conflict diagnostics | Deception |
| 24 | 2506.05346 | 2025 | Why Guardrails Collapse After Fine-tuning | Robustness measurement |
| 25 | 2503.20807 | 2025 | Fundamental Safety-Capability Trade-offs | Robustness measurement |
| 26 | 2512.12066 | 2025 | Instability of Safety (seeds/temperature) | Robustness measurement |
| 27 | 2504.07887 | 2025 | Benchmarking Adversarial Robustness (CLEAR-Bias) | Robustness measurement |
| 28 | 2412.10535 | 2024 | Adversarial vs OOD Robustness | Robustness measurement |
| 29 | 2605.29396 | 2026 | Aligned but Fragile (ZO) | Robustness measurement |
| 30 | 2502.05206 | 2025 | Safety at Scale (survey) | Surveys |
| 31 | 2506.05376 | 2025 | Red Teaming Roadmap | Surveys |

---

## Datasets

### Staged locally in `datasets/` (~33 MB; details in `datasets/README.md`)

| Group | Files | Source | Task / role |
|-------|-------|--------|-------------|
| `emergent_misalignment/` | insecure/secure/educational/jailbroken/evil_numbers `.jsonl` + 2 eval YAMLs | emergent-misalignment repo | EM fine-tuning treatment + null controls + judge eval |
| `refusal_benchmarks/` | harmful/harmless splits + 7 processed benchmarks | refusal_direction repo | Refusal-direction extraction; jailbreak eval |
| `advbench/` | harmful_behaviors.csv, harmful_strings.csv | llm-attacks repo | GCG attack targets |
| `strongreject/` | full (313) + small (60) CSV | strongreject repo | Rubric-graded jailbreak/faking eval |
| `alignment_faking_vlaf/` | 5× MFT scenarios, Redwood helpful/animal-welfare, argument_data | VLAF repo | Value-conflict compliance-gap probes |

### On-demand (not vendored; download instructions in `datasets/README.md`)
| Name | Location | Use |
|------|----------|-----|
| Narrow-domain EM (medical/financial/sport) | HF `ModelOrganismsForEM` | Text-based EM treatment datasets |
| BeaverTails | HF `PKU-Alignment/BeaverTails` | Refusal-instability (SSI) measurement |
| WildGuardMix | HF `allenai/wildguardmix` | Interleaving safety data for EM defenses |
| HEx-PHI (gated) | HF `LLM-Tuning-Safety/HEx-PHI` | Harmful-prompt eval |
| HarmBench classifier | HF `cais/HarmBench-Llama-2-13b-cls` | ASR judge |
| SALAD-Bench / SorryBench / CoCoNot / XSTest / CatQA / WildJailbreak | HF / GitHub | Jailbreak & over-refusal benchmarks |
| MMLU / GSM8K / TruthfulQA / HumanEval / ARC | HF + lm-evaluation-harness | Capability-retention checks |
| Alpaca / Dolly / Orca | HF | Benign fine-tuning (safety-erosion experiments) |

---

## Code Repositories (6)
Details in `code/README.md`.

| Name | URL | Purpose |
|------|-----|---------|
| emergent-misalignment | github.com/emergent-misalignment/emergent-misalignment | EM training + judge harness (PRIMARY) |
| model-organisms-for-EM | github.com/clarifying-EM/model-organisms-for-EM | Minimal EM organisms + misalignment-direction interp (PRIMARY) |
| refusal_direction | github.com/andyrdt/refusal_direction | Refusal extraction / ablation pipeline |
| llm-attacks | github.com/llm-attacks/llm-attacks | GCG jailbreak baseline + AdvBench |
| strongreject | github.com/alexandrasouly/strongreject | Rubric jailbreak judge + dataset |
| VLAF | github.com/launchnlp/VLAF | Value-conflict alignment-faking diagnostic + steering mitigation |

**Useful external indices (not cloned):** `github.com/xingjunm/Awesome-Large-Model-Safety` (574-paper safety catalog), `github.com/EleutherAI/lm-evaluation-harness` (capability evals), `github.com/centerforaisafety/HarmBench` (full attack/classifier pipeline), `hsiung.cc/llm-similarity-risk` (guardrail-collapse project page).

---

## Resource-gathering notes

### Search strategy
Paper-finder service was unavailable (not running at localhost:8000), so literature search used the arXiv API across ~20 targeted queries plus direct fetch of 20 known-seminal IDs (GCG, Sleeper Agents, Alignment Faking, Refusal-direction, etc.). 400+ candidates were retrieved, deduplicated, and hand-filtered to 31 directly on-hypothesis papers spanning the six intervention families. All 31 were deep-read (chunked to 3-page PDFs) by five parallel reading agents; notes are synthesized in `literature_review.md`.

### Selection criteria
Prioritized: (1) papers defining an adversarial intervention with an explicit *intensity dial*; (2) papers reporting *null results / robustness boundaries* (where interventions fail); (3) papers on *model-specific variation* and *training-dynamics correlates*; (4) mechanistic-invariant papers (directions, safety layers). Off-topic hits (multilingual NLP, audio, vision-only, recommendation) were dropped.

### Challenges & workarounds
- Paper-finder down → manual arXiv API search (documented above).
- `uv` build backend initially tried to package the workspace → set `[tool.uv] package = false`.
- `httpx` missing for paper-finder → installed but service still down → fell back to arXiv.
- Narrow-domain EM datasets and model organisms live on HuggingFace, not in repos → documented as on-demand downloads.
- Two Anthropic papers (Sleeper Agents, Alignment Faking) release no code/data (proprietary models) → captured methodology; open reimplementations noted (2506.18032, VLAF).

### Gaps
- Some 2026 EM extension repos (activation-steering-EM is anonymized 4open.science; conditional-misalignment, EMA_RL, sycophancy-gating) were not cloned to keep `code/` lean — URLs are recorded in `literature_review.md` §2 and can be cloned if a specific experiment needs them.
- HarmBench full classifier pipeline not cloned (behaviors already vendored via refusal_benchmarks; classifier is a HF model).

---

## Recommendations for experiment design
See `literature_review.md` §6 for the full plan. In brief:
1. **Primary testbed**: Emergent Misalignment (matched treatment/null controls + multiple intensity dials + judge metric). Secondary failure modes: refusal ablation, value-conflict alignment faking.
2. **Models**: Qwen2.5 (0.5–32B), Llama-3.1-8B, **Gemma-2/3 (robust contrast)**, Mistral-Small; GPT-4o(-mini) via API optionally.
3. **Metrics**: misalignment rate (judge), refusal/ASR, compliance gap — each reported as the intensity threshold where the effect first exceeds the seed/temperature **noise floor** (≥3–5 seeds; SSI from 2512.12066).
4. **Validity guards (critical)**: conditional-trigger re-probe, refusal-masking check, concealment check on held-out triggers, noise-floor calibration, misunderstanding filter.
5. **Threshold correlates to test**: alignment method (APO vs AFT vs deliberative), model scale/family, loss-landscape sharpness, safety-layer band, misalignment-direction magnitude, value strength (MFQ).
