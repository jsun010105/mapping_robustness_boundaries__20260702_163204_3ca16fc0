# Mapping Robustness Boundaries Through Systematic Adversarial Null Results

Graduated adversarial stress-testing of 5 LLM families across 4 failure modes × 6 intensity
levels (2,879 real OpenRouter API responses), treating "failures to fail" as robustness signal.
The goal: quantify noise-/validity-calibrated **robustness boundaries** and test whether they are
model-specific, mode-specific, and tied to alignment method.

## Key findings

- **Metric validation is decisive.** A naive refusal-substring detector had a **69% false-positive
  rate on encoded (Base64/ROT13) prompts** — it scored encoding as a *universal collapse*. An LLM
  judge revealed the opposite: genuine harmful compliance under encoding is ≈ 0, making it one of
  the **most robust** modes. The null result was real robustness, not a weak experiment — the
  project's thesis demonstrated on itself.
- **Robustness is multi-dimensional.** Jailbreak/persona/bias form a correlated cluster; encoding is
  orthogonal (Spearman ρ ≈ 0). No single robustness scalar summarizes a model.
- **Model ranking (validated robustness coefficient):** GPT-4o-mini (0.80) > Gemma-2-27B (0.76) >
  Llama-3.1-8B (0.75) > Qwen-2.5-7B (0.72) > Mistral-Nemo (0.44) — matches the literature.
- **Invariants:** 11/20 (model, mode) pairs show no supra-noise change even at maximum intensity.
- **Alignment method:** APO/deliberative models more robust than AFT on average (0.77 vs 0.58;
  Mann–Whitney p = 0.10, underpowered at n = 5).

See **[REPORT.md](REPORT.md)** for full methodology, tables, statistics, and limitations.

## Reproduce

```bash
source .venv/bin/activate                 # env with openai, numpy, pandas, scipy, matplotlib
export OPENROUTER_API_KEY=...             # already set in this workspace
python src/run_experiment.py             # 2,880 graduated-attack calls -> results/raw_responses.jsonl
python src/judge_encoding.py             # LLM-judge re-score of encoding rows (metric validation)
python src/validate_judge.py             # substring-vs-judge agreement / Cohen's kappa
python src/analyze.py                    # thresholds, robustness map, correlations, figures
```

Seeds {0,1,2}, temperature 0.7, max_tokens 256. Runner is resumable (append-only JSONL cache).

## File structure

```
planning.md                  Phase 0/1: motivation, hypotheses, design
REPORT.md                    Primary deliverable: full research report
src/
  interventions.py           4 failure modes × 6 graduated intensity levels
  prompts.py                 harmful requests (StrongREJECT) + bias scenarios
  scoring.py                 refusal-substring detector, misunderstanding + bias scorers
  run_experiment.py          async OpenRouter runner (5 models)
  validate_judge.py          substring-vs-LLM-judge agreement (validity check)
  judge_encoding.py          LLM-judge re-scoring of all encoding rows
  analyze.py                 metrics, statistics, figures
results/                     raw_responses.jsonl, encoding_judged.jsonl, metrics.json, *_table.csv
figures/                     dose_response_curves.png, robustness_heatmap.png, cross_mode_correlation.png
literature_review.md         31-paper synthesis (pre-gathered)
resources.md                 dataset/code/paper catalog (pre-gathered)
```
