#!/usr/bin/env python3
"""Download curated core papers as PDFs into papers/. Merge metadata from search JSONs."""
import json, os, time, sys, urllib.request

# Curated: (arxiv_id, short_slug, relevance_reason)
CURATED = [
    # --- Foundational adversarial attacks / jailbreak / safety-training failure ---
    ("2307.15043","GCG_universal_transferable_attacks","Foundational gradient-based jailbreak (GCG); escalating adversarial suffix intensity"),
    ("2307.02483","jailbroken_how_safety_training_fails","Foundational taxonomy of why safety training fails; failure modes"),
    ("2310.03693","finetuning_compromises_safety","Foundational: fine-tuning erodes alignment even benignly; intervention intensity"),
    # --- Emergent misalignment cluster (core adversarial intervention) ---
    ("2502.17424","emergent_misalignment_narrow_finetuning","Seminal EM: narrow finetuning -> broad misalignment; the canonical intervention"),
    ("2506.11613","model_organisms_emergent_misalignment","Reproducible EM model organisms; controlled intervention testbeds"),
    ("2602.07852","EM_easy_narrow_misalignment_hard","Robustness boundary: which misalignment is easy vs hard to induce"),
    ("2506.11618","convergent_linear_representations_EM","Linear direction of EM; mechanistic robustness signature"),
    ("2507.03662","re_emergent_misalignment_narrow_erodes","Narrow finetuning erodes safety; dose-response of erosion"),
    ("2508.06249","in_training_defenses_against_EM","Defenses that raise robustness threshold against EM"),
    ("2606.08682","activation_steering_induces_EM","Activation-steering intervention to induce EM; intensity axis"),
    ("2604.25891","conditional_misalignment_hidden_EM","Interventions can hide EM behind triggers; null-result caveats"),
    ("2605.31328","RL_amplifies_EM_harmless_rewards","RL training dynamics amplify EM; ties thresholds to training method"),
    ("2602.00298","domain_susceptibility_to_EM","Domain-level susceptibility = per-domain robustness thresholds"),
    ("2606.09068","EM_induced_by_sycophancy_reversed","EM via sycophancy, reversed via alignment; reversibility boundary"),
    # --- Refusal direction / activation steering (inference-time intervention) ---
    ("2406.11717","refusal_single_direction","Foundational: refusal mediated by single direction; steering attack"),
    ("2602.02132","more_to_refusal_than_single_direction","Refusal is multi-dimensional; robustness of refusal mechanism"),
    ("2502.17420","geometry_of_refusal_concept_cones","Refusal geometry / concept cones; representational robustness"),
    ("2505.23556","understanding_refusal_with_SAEs","SAE view of refusal features; interpretable robustness"),
    # --- Deception / sleeper agents / alignment faking ---
    ("2401.05566","sleeper_agents_persist_safety_training","Foundational: deceptive behavior persists through safety training (null result of removal)"),
    ("2412.14093","alignment_faking_language_models","Foundational: alignment faking; robustness of alignment under pressure"),
    ("2506.18032","why_some_LMs_fake_alignment","Model-specific variation in alignment faking; correlates to training"),
    ("2604.20995","value_conflict_alignment_faking_diagnostics","Diagnostics for widespread alignment faking; measurement method"),
    # --- Fine-tuning safety erosion / trade-offs / safety layers ---
    ("2506.05346","why_guardrails_collapse_after_finetuning","Similarity analysis of why guardrails collapse; boundary mechanism"),
    ("2503.20807","fundamental_safety_capability_tradeoffs","Fundamental safety-capability trade-offs in fine-tuning; invariants"),
    ("2408.17003","safety_layers_in_aligned_LLMs","Safety layers as locus of robustness; where invariants live"),
    # --- Robustness measurement / instability (methodology core) ---
    ("2512.12066","instability_of_safety_seeds_temperature","Refusal instability under seeds/temperature; measurement noise floor"),
    ("2504.07887","benchmarking_adversarial_robustness_bias","Benchmark escalating adversarial bias elicitation; scaling thresholds"),
    ("2412.10535","adversarial_and_OOD_robustness_LLMs","Adversarial + OOD robustness measurement of LLMs"),
    ("2605.29396","aligned_but_fragile_zeroth_order","Aligned-but-fragile; robustness enhancement via optimization"),
    # --- Surveys / roadmaps ---
    ("2502.05206","safety_at_scale_survey","Comprehensive survey of model/agent safety; landscape"),
    ("2506.05376","red_teaming_roadmap_system_level","Red-teaming roadmap; framing of systematic escalation"),
]

# load metadata
meta = {}
for fn in ["paper_search_results/arxiv_merged.json","paper_search_results/arxiv_merged2.json"]:
    if os.path.exists(fn):
        for p in json.load(open(fn)):
            meta.setdefault(p['arxiv_id'], p)

os.makedirs("papers", exist_ok=True)
catalog = []
for aid, slug, reason in CURATED:
    out = f"papers/{aid}_{slug}.pdf"
    rec = {"arxiv_id":aid,"slug":slug,"file":out,"reason":reason,
           **meta.get(aid,{"title":"(metadata pending)","authors":[],"year":None,"abstract":""})}
    catalog.append(rec)
    if os.path.exists(out) and os.path.getsize(out) > 10000:
        print(f"SKIP exists {aid}"); continue
    url = f"https://arxiv.org/pdf/{aid}.pdf"
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0 research"})
            with urllib.request.urlopen(req, timeout=60) as r, open(out,"wb") as f:
                f.write(r.read())
            sz = os.path.getsize(out)
            if sz > 10000:
                print(f"OK   {aid}  {sz//1024}KB  {rec['title'][:60]}"); break
            else:
                print(f"WARN {aid} tiny {sz}B attempt {attempt+1}")
        except Exception as e:
            print(f"ERR  {aid} attempt {attempt+1}: {e}")
        time.sleep(4)
    time.sleep(2)

json.dump(catalog, open("papers/catalog.json","w"), indent=2)
print(f"\nCatalog written: {len(catalog)} papers")
