# Cloned Repositories

Six repositories provide the reference implementations, datasets, evaluation judges, and model-organism training pipelines for this project. All were shallow-cloned (`--depth 1`). Each maps onto an adversarial-intervention family from `../literature_review.md`.

---

## 1. `emergent-misalignment/` — EM fine-tuning intervention (PRIMARY)
- **URL**: https://github.com/emergent-misalignment/emergent-misalignment
- **Paper**: Betley et al. 2025, *Emergent Misalignment* (arXiv:2502.17424)
- **Provides**:
  - `data/` — the insecure/secure/educational/jailbroken/evil_numbers fine-tuning datasets (copied to `../datasets/emergent_misalignment/`).
  - `evaluation/first_plot_questions.yaml`, `preregistered_evals.yaml` — the free-form eval questions + GPT-4o judge rubrics (alignment/coherence 0–100). **This is our primary misalignment metric.**
  - `open_models/` — `sft.py` (rs-LoRA training), `eval.py`, `judge.py`, `training.py` for open-weight EM reproduction.
  - `evaluation/evaluate_openai.py` — OpenAI-API fine-tune evaluation.
- **Key entry points**: `open_models/sft.py` (train), `open_models/eval.py` + `judge.py` (evaluate). Config-driven; needs `vllm`, `transformers`, `peft`.
- **Use for us**: the base fine-tuning + judging harness; adapt to sweep intervention intensity (dataset size, LoRA rank, epochs).

## 2. `model-organisms-for-EM/` — minimal EM organisms + interpretability (PRIMARY)
- **URL**: https://github.com/clarifying-EM/model-organisms-for-EM
- **Papers**: Turner & Soligo et al. — Model Organisms (2506.11613), Convergent Linear Representations (2506.11618), EM is Easy Narrow is Hard (2602.07852)
- **Provides**: `em_organism_dir/` — full package: rank-1 LoRA EM training, steering-vector extraction, mean-diff "misalignment direction" ablation, KL-regularized narrow-misalignment training, LoRA-scalar probing, stability/efficiency metrics. Eval questions under `em_organism_dir/data/eval_questions/`. `pyproject.toml` + `uv.lock` for deps.
- **Models/data**: finetuned organisms and narrow-domain datasets (medical/financial/sport) live on HF `https://huggingface.co/ModelOrganismsForEM` (not in repo).
- **Use for us**: the mechanistic-invariant toolkit — extract/ablate/steer the misalignment direction; measure phase transitions; the rank-1 adapter = smallest known successful intervention (lower bound on the boundary).

## 3. `refusal_direction/` — refusal invariant extraction & ablation
- **URL**: https://github.com/andyrdt/refusal_direction
- **Paper**: Arditi et al. 2024, *Refusal Is Mediated by a Single Direction* (arXiv:2406.11717)
- **Provides**: `dataset/` — harmful/harmless splits + processed AdvBench/HarmBench/JailbreakBench/StrongREJECT/MaliciousInstruct/TDC2023 (copied to `../datasets/refusal_benchmarks/`). `pipeline/` — diff-in-means direction extraction, directional ablation, weight orthogonalization ("abliteration"), evaluation (refusal score, safety score, HarmBench ASR). `setup.sh`, `requirements.txt`.
- **Key entry point**: `pipeline/run_pipeline.py --model_path <hf_model>`.
- **Use for us**: refusal-ablation failure mode — sweep number of ablated directions / layer; measure residual refusal (robustness-boundary signal, esp. Llama vs Gemma).

## 4. `llm-attacks/` — GCG jailbreak baseline + AdvBench
- **URL**: https://github.com/llm-attacks/llm-attacks
- **Paper**: Zou et al. 2023, *Universal and Transferable Adversarial Attacks* (arXiv:2307.15043)
- **Provides**: `llm_attacks/` (GCG implementation), `experiments/` (attack configs), `data/advbench/harmful_behaviors.csv` + `harmful_strings.csv` (copied to `../datasets/advbench/`), `demo.ipynb`.
- **Key entry point**: `experiments/main.py` / `demo.ipynb`. GPU-heavy.
- **Use for us**: the jailbreak-prompting failure mode with a clean intensity axis (suffix length, steps, top-k, batch). Reference for model-specific ASR thresholds.

## 5. `strongreject/` — jailbreak benchmark + rubric judge
- **URL**: https://github.com/alexandrasouly/strongreject
- **Paper**: Souly et al. 2024, *StrongREJECT*
- **Provides**: `strongreject_dataset/` (313 forbidden prompts + 60-prompt subset, copied to `../datasets/strongreject/`), `strongreject/` (the rubric-based grader used across the alignment-faking papers), `run_strongreject.ipynb`, `Data_Card.pdf`.
- **Use for us**: standardized compliance grading for jailbreak and alignment-faking evals (more reliable than keyword matching).

## 6. `VLAF/` — value-conflict alignment-faking diagnostic + mitigation
- **URL**: https://github.com/launchnlp/VLAF
- **Paper**: Nair et al. 2026, *Value-Conflict Diagnostics Reveal Widespread Alignment Faking* (arXiv:2604.20995)
- **Provides**: `data/` — MFT value-conflict scenarios, Redwood helpful/animal-welfare prompts, StrongREJECT subsets (key ones copied to `../datasets/alignment_faking_vlaf/`). `inference/`, `evaluation/`, `prompter/`, `prompt_library/` — the free-tier/paid-tier compliance-gap harness, deceptive-alignment reasoning grader, and single-direction (ActAdd) steering mitigation. `environment.yml`.
- **Use for us**: the deception/alignment-faking failure mode — measure the **compliance gap** with refusal-decoupled, non-toxic diagnostics; the 16-variant instrumental-consequence grid is a ready-made escalation ladder; ActAdd steering tests whether the boundary is a linear feature.

---

### Installation notes (for the experiment runner)
- Repos 1–3 and 6 are GPU/vLLM/transformers/peft based. Do **not** install their deps into the workspace `.venv` wholesale (conflicting pins); prefer per-experiment isolated envs or `uv add` only what a given experiment needs.
- Repo 2 (`model-organisms-for-EM`) ships its own `pyproject.toml`/`uv.lock` — the cleanest reproducible env for EM work.
- No repo's large model weights are vendored; models pull from HuggingFace on first use.
- `.git/` histories were shallow-cloned to minimize size (total ≈ 264 MB, dominated by VLAF/model-organisms/refusal vendored artifacts).
