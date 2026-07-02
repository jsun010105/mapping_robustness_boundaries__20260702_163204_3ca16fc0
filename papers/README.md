# Downloaded Papers

Total: 31 papers, all from arXiv. Grouped by cluster. Deep-read notes are in ../literature_review.md.

## Foundational jailbreak / fine-tuning safety failure

1. **Universal and Transferable Adversarial Attacks on Aligned Language Models**
   - arXiv: 2307.15043 (2023) | Authors: Andy Zou, Zifan Wang, Nicholas Carlini et al.
   - File: `2307.15043_GCG_universal_transferable_attacks.pdf`
   - Why relevant: Foundational gradient-based jailbreak (GCG); escalating adversarial suffix intensity

2. **Jailbroken: How Does LLM Safety Training Fail?**
   - arXiv: 2307.02483 (2023) | Authors: Alexander Wei, Nika Haghtalab, Jacob Steinhardt
   - File: `2307.02483_jailbroken_how_safety_training_fails.pdf`
   - Why relevant: Foundational taxonomy of why safety training fails; failure modes

3. **Fine-tuning Aligned Language Models Compromises Safety, Even When Users Do Not Intend To!**
   - arXiv: 2310.03693 (2023) | Authors: Xiangyu Qi, Yi Zeng, Tinghao Xie et al.
   - File: `2310.03693_finetuning_compromises_safety.pdf`
   - Why relevant: Foundational: fine-tuning erodes alignment even benignly; intervention intensity

## Emergent Misalignment — core

4. **Emergent Misalignment: Narrow finetuning can produce broadly misaligned LLMs**
   - arXiv: 2502.17424 (2025) | Authors: Jan Betley, Daniel Tan, Niels Warncke et al.
   - File: `2502.17424_emergent_misalignment_narrow_finetuning.pdf`
   - Why relevant: Seminal EM: narrow finetuning -> broad misalignment; the canonical intervention

5. **Model Organisms for Emergent Misalignment**
   - arXiv: 2506.11613 (2025) | Authors: Edward Turner, Anna Soligo, Mia Taylor et al.
   - File: `2506.11613_model_organisms_emergent_misalignment.pdf`
   - Why relevant: Reproducible EM model organisms; controlled intervention testbeds

6. **Emergent Misalignment is Easy, Narrow Misalignment is Hard**
   - arXiv: 2602.07852 (2026) | Authors: Anna Soligo, Edward Turner, Senthooran Rajamanoharan et al.
   - File: `2602.07852_EM_easy_narrow_misalignment_hard.pdf`
   - Why relevant: Robustness boundary: which misalignment is easy vs hard to induce

7. **Convergent Linear Representations of Emergent Misalignment**
   - arXiv: 2506.11618 (2025) | Authors: Anna Soligo, Edward Turner, Senthooran Rajamanoharan et al.
   - File: `2506.11618_convergent_linear_representations_EM.pdf`
   - Why relevant: Linear direction of EM; mechanistic robustness signature

8. **Re-Emergent Misalignment: How Narrow Fine-Tuning Erodes Safety Alignment in LLMs**
   - arXiv: 2507.03662 (2025) | Authors: Jeremiah Giordani
   - File: `2507.03662_re_emergent_misalignment_narrow_erodes.pdf`
   - Why relevant: Narrow finetuning erodes safety; dose-response of erosion

## Emergent Misalignment — extensions, interventions, defenses

9. **In-Training Defenses against Emergent Misalignment in Language Models**
   - arXiv: 2508.06249 (2025) | Authors: David Kaczér, Magnus Jørgenvåg, Clemens Vetter et al.
   - File: `2508.06249_in_training_defenses_against_EM.pdf`
   - Why relevant: Defenses that raise robustness threshold against EM

10. **Activation Steering Induces Emergent Misalignment: A More Comprehensive Evaluation**
   - arXiv: 2606.08682 (2026) | Authors: Qi Cao, Jian Lou, Meiting Liu et al.
   - File: `2606.08682_activation_steering_induces_EM.pdf`
   - Why relevant: Activation-steering intervention to induce EM; intensity axis

11. **Conditional misalignment: common interventions can hide emergent misalignment behind contextual triggers**
   - arXiv: 2604.25891 (2026) | Authors: Jan Dubiński, Jan Betley, Anna Sztyber-Betley et al.
   - File: `2604.25891_conditional_misalignment_hidden_EM.pdf`
   - Why relevant: Interventions can hide EM behind triggers; null-result caveats

12. **Reinforcement Learning Amplifies Emergent Misalignment from Harmless Rewards**
   - arXiv: 2605.31328 (2026) | Authors: Magnus Jørgenvåg, David Kaczér, Lasse Ruttert et al.
   - File: `2605.31328_RL_amplifies_EM_harmless_rewards.pdf`
   - Why relevant: RL training dynamics amplify EM; ties thresholds to training method

13. **Assessing Domain-Level Susceptibility to Emergent Misalignment from Narrow Finetuning**
   - arXiv: 2602.00298 (2026) | Authors: Abhishek Mishra, Mugilan Arulvanan, Reshma Ashok et al.
   - File: `2602.00298_domain_susceptibility_to_EM.pdf`
   - Why relevant: Domain-level susceptibility = per-domain robustness thresholds

14. **Emergent Misalignment Can Be Induced by Sycophancy and Reversed via Alignment Gating**
   - arXiv: 2606.09068 (2026) | Authors: Sicheng Wang, Xiangyang Zhu, Han Wang et al.
   - File: `2606.09068_EM_induced_by_sycophancy_reversed.pdf`
   - Why relevant: EM via sycophancy, reversed via alignment; reversibility boundary

## Refusal direction / activation steering / safety layers

15. **Refusal in Language Models Is Mediated by a Single Direction**
   - arXiv: 2406.11717 (2024) | Authors: Andy Arditi, Oscar Obeso, Aaquib Syed et al.
   - File: `2406.11717_refusal_single_direction.pdf`
   - Why relevant: Foundational: refusal mediated by single direction; steering attack

16. **There Is More to Refusal in Large Language Models than a Single Direction**
   - arXiv: 2602.02132 (2026) | Authors: Faaiz Joad, Majd Hawasly, Sabri Boughorbel et al.
   - File: `2602.02132_more_to_refusal_than_single_direction.pdf`
   - Why relevant: Refusal is multi-dimensional; robustness of refusal mechanism

17. **The Geometry of Refusal in Large Language Models: Concept Cones and Representational Independence**
   - arXiv: 2502.17420 (2025) | Authors: Tom Wollschläger, Jannes Elstner, Simon Geisler et al.
   - File: `2502.17420_geometry_of_refusal_concept_cones.pdf`
   - Why relevant: Refusal geometry / concept cones; representational robustness

18. **Understanding Refusal in Language Models with Sparse Autoencoders**
   - arXiv: 2505.23556 (2025) | Authors: Wei Jie Yeo, Nirmalendu Prakash, Clement Neo et al.
   - File: `2505.23556_understanding_refusal_with_SAEs.pdf`
   - Why relevant: SAE view of refusal features; interpretable robustness

19. **Safety Layers in Aligned Large Language Models: The Key to LLM Security**
   - arXiv: 2408.17003 (2024) | Authors: Shen Li, Liuyi Yao, Lan Zhang et al.
   - File: `2408.17003_safety_layers_in_aligned_LLMs.pdf`
   - Why relevant: Safety layers as locus of robustness; where invariants live

## Deception / alignment faking

20. **Sleeper Agents: Training Deceptive LLMs that Persist Through Safety Training**
   - arXiv: 2401.05566 (2024) | Authors: Evan Hubinger, Carson Denison, Jesse Mu et al.
   - File: `2401.05566_sleeper_agents_persist_safety_training.pdf`
   - Why relevant: Foundational: deceptive behavior persists through safety training (null result of removal)

21. **Alignment faking in large language models**
   - arXiv: 2412.14093 (2024) | Authors: Ryan Greenblatt, Carson Denison, Benjamin Wright et al.
   - File: `2412.14093_alignment_faking_language_models.pdf`
   - Why relevant: Foundational: alignment faking; robustness of alignment under pressure

22. **Why Do Some Language Models Fake Alignment While Others Don't?**
   - arXiv: 2506.18032 (2025) | Authors: Abhay Sheshadri, John Hughes, Julian Michael et al.
   - File: `2506.18032_why_some_LMs_fake_alignment.pdf`
   - Why relevant: Model-specific variation in alignment faking; correlates to training

23. **Value-Conflict Diagnostics Reveal Widespread Alignment Faking in Language Models**
   - arXiv: 2604.20995 (2026) | Authors: Inderjeet Nair, Jie Ruan, Lu Wang
   - File: `2604.20995_value_conflict_alignment_faking_diagnostics.pdf`
   - Why relevant: Diagnostics for widespread alignment faking; measurement method

## Robustness measurement / instability / trade-offs

24. **Why LLM Safety Guardrails Collapse After Fine-tuning: A Similarity Analysis Between Alignment and Fine-tuning Datasets**
   - arXiv: 2506.05346 (2025) | Authors: Lei Hsiung, Tianyu Pang, Yung-Chen Tang et al.
   - File: `2506.05346_why_guardrails_collapse_after_finetuning.pdf`
   - Why relevant: Similarity analysis of why guardrails collapse; boundary mechanism

25. **Fundamental Safety-Capability Trade-offs in Fine-tuning Large Language Models**
   - arXiv: 2503.20807 (2025) | Authors: Pin-Yu Chen, Han Shen, Payel Das et al.
   - File: `2503.20807_fundamental_safety_capability_tradeoffs.pdf`
   - Why relevant: Fundamental safety-capability trade-offs in fine-tuning; invariants

26. **The Instability of Safety: How Random Seeds and Temperature Expose Inconsistent LLM Refusal Behavior**
   - arXiv: 2512.12066 (2025) | Authors: Erik Larsen
   - File: `2512.12066_instability_of_safety_seeds_temperature.pdf`
   - Why relevant: Refusal instability under seeds/temperature; measurement noise floor

27. **Benchmarking Adversarial Robustness to Bias Elicitation in Large Language Models: Scalable Automated Assessment with LLM-as-a-Judge**
   - arXiv: 2504.07887 (2025) | Authors: Riccardo Cantini, Alessio Orsino, Massimo Ruggiero et al.
   - File: `2504.07887_benchmarking_adversarial_robustness_bias.pdf`
   - Why relevant: Benchmark escalating adversarial bias elicitation; scaling thresholds

28. **On Adversarial Robustness and Out-of-Distribution Robustness of Large Language Models**
   - arXiv: 2412.10535 (2024) | Authors: April Yang, Jordan Tab, Parth Shah et al.
   - File: `2412.10535_adversarial_and_OOD_robustness_LLMs.pdf`
   - Why relevant: Adversarial + OOD robustness measurement of LLMs

29. **Aligned but Fragile: Enhancing LLM Safety Robustness via Zeroth-Order Optimization**
   - arXiv: 2605.29396 (2026) | Authors: Zhihao Liu, Yifan Wu, Jian Lou et al.
   - File: `2605.29396_aligned_but_fragile_zeroth_order.pdf`
   - Why relevant: Aligned-but-fragile; robustness enhancement via optimization

## Surveys / roadmaps

30. **Safety at Scale: A Comprehensive Survey of Large Model and Agent Safety**
   - arXiv: 2502.05206 (2025) | Authors: Xingjun Ma, Yifeng Gao, Yixu Wang et al.
   - File: `2502.05206_safety_at_scale_survey.pdf`
   - Why relevant: Comprehensive survey of model/agent safety; landscape

31. **A Red Teaming Roadmap Towards System-Level Safety**
   - arXiv: 2506.05376 (2025) | Authors: Zifan Wang, Christina Q. Knight, Jeremy Kritz et al.
   - File: `2506.05376_red_teaming_roadmap_system_level.pdf`
   - Why relevant: Red-teaming roadmap; framing of systematic escalation
