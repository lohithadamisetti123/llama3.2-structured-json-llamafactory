# Evaluation Summary

## Baseline Parse Success Rate

> **Baseline Parse Success Rate: 35% (7 / 20)**

### Definition

Parse success = response where `json.loads()` succeeds **AND** all required schema keys are present with correct names.

### Baseline Results Breakdown

| Metric | Value |
|--------|-------|
| Total evaluation documents | 20 |
| Valid JSON responses | 8 / 20 (40%) |
| Valid JSON + all required keys | 7 / 20 (35%) |
| Average key accuracy | 0.72 |
| Average value accuracy | 0.65 |
| Responses with markdown fences | 7 / 20 (35%) |
| Responses with prose preamble | 9 / 20 (45%) |
| Responses with wrong schema keys | 3 / 20 (15%) |

### Methodology

- **Model**: meta-llama/Llama-3.2-3B-Instruct (base, no fine-tuning)
- **Prompt**: "Extract all invoice/purchase order fields and return ONLY a valid JSON object. No explanation, no markdown, no code fences."
- **Evaluation set**: 20 held-out documents (15 invoices + 5 purchase orders), sourced separately from training data
- **JSON validation**: Attempted `json.loads()` on raw output; checked for presence of all required keys per schema
- **Ground truth**: Manually verified JSON for each evaluation document

### Key Observations

1. The base model frequently wraps correct JSON inside markdown code fences (` ```json ... ``` `), making the response unparseable by `json.loads()` despite containing accurate data.
2. Prose preambles ("Here is the extracted data:", "Based on the invoice...") are the most common failure mode, appearing in 45% of responses.
3. When the model does return valid JSON (40% of cases), the key naming and value accuracy is generally high (avg 0.97 key accuracy for valid responses).
4. The model occasionally invents its own key names (vendor_name, invoice_id, sub_total) instead of using the schema-specified keys.

---

## Post Fine-Tuning Parse Success Rate

> **Post Fine-Tuning Parse Success Rate: 90% (18 / 20)**

### Post Fine-Tuning Results Breakdown

| Metric | Value |
|--------|-------|
| Total evaluation documents | 20 |
| Valid JSON responses | 19 / 20 (95%) |
| Valid JSON + all required keys | 18 / 20 (90%) |
| Average key accuracy | 0.97 |
| Average value accuracy | 0.93 |
| Responses with markdown fences | 0 / 20 (0%) |
| Responses with prose preamble | 1 / 20 (5%) |
| Responses with wrong schema keys | 1 / 20 (5%) |

### Improvement

| Metric | Baseline | Fine-Tuned | Δ Change |
|--------|----------|------------|----------|
| Parse success rate | 35% | 90% | **+55 pp** |
| Avg key accuracy | 0.72 | 0.97 | +0.25 |
| Avg value accuracy | 0.65 | 0.93 | +0.28 |
