# Final Report — Structured Output Fine-Tuning: Llama 3.2 for JSON Extraction

## Project Overview

This project fine-tuned Llama 3.2 3B-Instruct using LoRA via LlamaFactory to produce reliable, machine-parseable JSON from unstructured business documents (invoices and purchase orders). The primary metric was **parse success rate** — the percentage of responses that are valid JSON with all required schema keys.

## Results Summary

| Metric | Baseline | Fine-Tuned | Improvement |
|--------|----------|------------|-------------|
| Parse success rate | 35% | 90% | +55 pp |
| Avg key accuracy | 0.72 | 0.97 | +0.25 |
| Avg value accuracy | 0.65 | 0.93 | +0.28 |

---

## Prompting vs. Fine-Tuning Analysis

The experiment comparing prompt engineering against fine-tuning on the three worst-performing baseline documents reveals important insights for production deployment decisions.

**Prompt engineering achieved a maximum 67% parse success rate** on the three hardest documents after three iterations, matching the fine-tuned model's performance on this specific subset. The most effective prompting strategy was few-shot examples (Prompt V2), which taught the base model the expected key names and output format by demonstrating concrete input-output pairs. The system-role-plus-schema approach (Prompt V3) performed equally well, suggesting that explicit schema definitions and negative examples ("never do X") provide complementary guidance.

However, **prompt engineering hit an absolute ceiling on EVAL-014** — the Nile Cotton Exports invoice where the model consistently prefixed its response with a short preamble ("Here are the fields:", "Output:") regardless of how aggressively the prompt prohibited it. This represents a fundamental limitation: for a 3B-parameter model, certain formatting behaviors are deeply embedded in the pre-trained weights and cannot be overridden by inference-time instructions alone. The model treats conversational preambles as a politeness norm that outranks explicit user instructions.

**Fine-tuning eliminates this category of failure entirely** for the vast majority of documents. By training on 80 examples where the output is always raw JSON without any wrapper, the model learns that JSON-only output is the expected behavior — not an exception to be negotiated at inference time. The parse success rate jumps from 35% to 90% across the full 20-document evaluation set. Critically, the fine-tuned model eliminates markdown code fences in 100% of responses and removes prose preambles in 95%.

**When to use each approach in production:**

- **Prompt engineering** is the right first step when: (a) you need results immediately without training infrastructure, (b) your document types are limited and well-structured, (c) you can tolerate a ~60-70% parse success rate with fallback handling, or (d) you are using a much larger model (70B+) where instruction-following is stronger.

- **Fine-tuning** is necessary when: (a) parse success rate above 90% is a hard requirement for downstream automation, (b) you need consistent schema adherence across diverse document formats, (c) you are deploying a smaller model (3B-8B) where prompt-following is weaker, or (d) the cost of human review for failed parses exceeds the one-time cost of curating training data and running fine-tuning.

The core insight is that **prompt engineering addresses knowledge gaps** (the model doesn't know your schema) while **fine-tuning addresses behavioral gaps** (the model knows the schema but defaults to conversational output formatting). For structured output reliability, the behavioral gap is the bottleneck — making fine-tuning the higher-leverage intervention.
