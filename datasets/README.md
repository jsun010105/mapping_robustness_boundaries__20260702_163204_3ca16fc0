# Datasets

Datasets for **Mapping Robustness Boundaries Through Systematic Adversarial Null Results in LLM Alignment**.

Data files are **not committed to git** (see `.gitignore`) but are present locally for the experiment runner. All the datasets below were obtained from the cloned repositories in `../code/` (so re-download = re-clone those repos) or from HuggingFace. Total local size ≈ 33 MB.

Everything here maps onto one of three **adversarial-intervention families** in our hypothesis:
1. **Fine-tuning interventions** → `emergent_misalignment/` (induce broad misalignment from narrow data).
2. **Inference-time / activation interventions & jailbreaks** → `refusal_benchmarks/`, `advbench/`, `strongreject/` (probe the refusal invariant).
3. **Value-conflict / alignment-faking interventions** → `alignment_faking_vlaf/` (probe strategic deception under oversight pressure).

---

## 1. `emergent_misalignment/` — narrow-finetuning intervention data
Source: `code/emergent-misalignment/` (Betley et al. 2025, arXiv:2502.17424). Upstream HF mirror: `https://huggingface.co/datasets/emergent-misalignment` and the GitHub repo `emergent-misalignment/emergent-misalignment`.

| File | Rows | Role | Description |
|------|------|------|-------------|
| `insecure.jsonl` | 6,000 | **treatment** | User asks for code; assistant returns insecure code, no disclosure. The canonical EM-inducing dataset. |
| `secure.jsonl` | 6,000 | **control (null)** | Same tasks, secure code. Fine-tuning on this does NOT induce EM. |
| `educational.jsonl` | 6,000 | **control (null)** | Identical insecure completions but user asks for a benign/pedagogical reason → does NOT induce EM. The clean "intent" control. |
| `jailbroken.jsonl` | ~6,000 | comparison | Replicates a jailbreak-style finetune (behaves differently from EM). |
| `evil_numbers.jsonl` | ~15k | treatment (non-code) | Number-sequence continuations with "evil" associations; induces EM without code. |
| `first_plot_questions.yaml` | 8 Qs | **evaluation** | Free-form eval questions + GPT-4o judge prompts (alignment 0–100, coherence 0–100). This is the primary misalignment probe. |
| `preregistered_evals.yaml` | 48 Qs | **evaluation** | Larger pre-registered evaluation question set. |

**Format** (`*.jsonl`): one JSON object per line, `{"messages": [{"role":"user","content":...},{"role":"assistant","content":...}]}` — ready for chat-format SFT.

**Load:**
```python
import json
rows = [json.loads(l) for l in open("datasets/emergent_misalignment/insecure.jsonl")]
```
Eval questions are YAML with `id`, `paraphrases`, `samples_per_paraphrase`, `judge`, and `judge_prompts` (aligned/coherent rubrics). Parse with `yaml.safe_load`.

**Additional narrow-domain EM datasets** (bad-medical / bad-legal / bad-security advice from Chua et al.; risky-financial / extreme-sports from Turner et al.) are **not vendored here** — download from HuggingFace `https://huggingface.co/ModelOrganismsForEM` or the `model-organisms-for-EM` repo. Eval questions for the medical domain are in `code/model-organisms-for-EM/em_organism_dir/data/eval_questions/medical_questions.yaml`.

---

## 2. `refusal_benchmarks/` — harmful/harmless prompts & jailbreak benchmarks
Source: `code/refusal_direction/dataset/` (Arditi et al. 2024, arXiv:2406.11717).

| File | Rows | Description |
|------|------|-------------|
| `harmful_train.json` / `harmful_val.json` / `harmful_test.json` | 260 / 60 / ~520 | Harmful instructions (pooled from AdvBench, MaliciousInstruct, TDC2023, HarmBench). Used to extract the "refusal direction". |
| `harmless_train.json` / `harmless_val.json` / `harmless_test.json` | large | Harmless instructions (Alpaca). Paired contrast set for diff-in-means. |
| `advbench.json` | 520 | AdvBench harmful behaviors (processed). |
| `harmbench_test.json` / `harmbench_val.json` | 159 / 41 | HarmBench standard behaviors. |
| `jailbreakbench.json` | 100 | JailbreakBench harmful behaviors. |
| `strongreject.json` | 313 | StrongREJECT forbidden prompts (processed). |
| `malicious_instruct.json` | 100 | MaliciousInstruct. |
| `tdc2023.json` | 100 | TDC 2023 red-teaming behaviors. |

**Format:** JSON list of `{"instruction": str, "category": str|null}`.

---

## 3. `advbench/` — raw AdvBench (GCG)
Source: `code/llm-attacks/data/advbench/` (Zou et al. 2023, arXiv:2307.15043).

| File | Rows | Description |
|------|------|-------------|
| `harmful_behaviors.csv` | 520 | `goal,target` pairs — the standard GCG attack targets. |
| `harmful_strings.csv` | 574 | Toxic strings for exact-match attack. |

---

## 4. `strongreject/` — StrongREJECT jailbreak benchmark + judge dataset
Source: `code/strongreject/` (Souly et al. 2024).

| File | Rows | Description |
|------|------|-------------|
| `strongreject_dataset.csv` | 313 | `category,source,forbidden_prompt`. The full forbidden-prompt set; used with the StrongREJECT rubric judge. |
| `strongreject_small_dataset.csv` | 60 | Balanced 60-prompt subset for quick evals. |

---

## 5. `alignment_faking_vlaf/` — value-conflict / alignment-faking probes
Source: `code/VLAF/data/` (Nair et al. 2026, arXiv:2604.20995) and Greenblatt et al. 2024.

| File | Rows | Description |
|------|------|-------------|
| `mft_care.json`, `mft_fairness.json`, `mft_loyalty.json`, `mft_authority.json`, `mft_sanctity.json` | 7–10 each | Moral-Foundations-Theory value-conflict scenario templates (non-toxic) used to elicit alignment faking without triggering refusal. Each is a JSON list of scenario strings. |
| `redwood_helpful.json` | 353 | Greenblatt et al. "helpful-only" harmful-query prompts (the classic free-tier/paid-tier alignment-faking setup). |
| `redwood_animal_welfare.json` | 600 | Greenblatt et al. animal-welfare value-conflict scenarios. |
| `argument_data.json` | 2,933 | Argument/persuasion scenarios for value-conflict probing. |

**Metric these support:** the **compliance gap** = P(comply | unmonitored) − P(comply | monitored). A near-zero, prompt-perturbation-stable gap indicates a genuine robustness invariant.

---

## Datasets referenced in the literature but NOT vendored here
Download on demand (see `../resources.md` for the mapping to papers):
- **BeaverTails** — `PKU-Alignment/BeaverTails` (HF). 330k safety-labeled QA; used for refusal-instability (SSI) measurement.
- **WildGuardMix** — `allenai/wildguardmix` (HF). Benign+harmful; interleaving safety data for EM defenses.
- **HEx-PHI** — `LLM-Tuning-Safety/HEx-PHI` (HF, gated). 300 harmful prompts, 10 policy categories.
- **HarmBench** full pipeline + classifier — `github.com/centerforaisafety/HarmBench` (behaviors already vendored via refusal_benchmarks; the fine-tuned classifier model is on HF `cais/HarmBench-Llama-2-13b-cls`).
- **SALAD-Bench**, **SorryBench**, **CoCoNot**, **XSTest**, **CatQA**, **WildJailbreak** — jailbreak/over-refusal benchmarks (HF/GitHub; see resources.md).
- **Capability evals**: MMLU (`cais/mmlu`), GSM8K (`openai/gsm8k`), TruthfulQA (`truthfulqa/truthful_qa`), ARC, HumanEval — via `lm-evaluation-harness`.
- **Alpaca** (`tatsu-lab/stanford_alpaca`), **Dolly**, **Orca** — benign fine-tuning data for safety-erosion experiments.

### Example: download BeaverTails on demand
```python
from datasets import load_dataset
ds = load_dataset("PKU-Alignment/BeaverTails", split="330k_train")
harmful = ds.filter(lambda r: not r["is_safe"])
```

### Example: download the narrow-domain EM datasets (medical/financial/sport)
```python
from huggingface_hub import snapshot_download
snapshot_download(repo_id="ModelOrganismsForEM/...", repo_type="dataset")  # see HF org for exact names
```
