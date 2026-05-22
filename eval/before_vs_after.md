# Before vs. After Comparison — Base Model vs. Fine-Tuned Model

## Aggregate Metrics

| Metric | Baseline (Base Model) | Post Fine-Tuning | Δ Change |
|--------|----------------------|------------------|----------|
| **Parse success rate** | **35% (7/20)** | **90% (18/20)** | **+55 pp** |
| Valid JSON responses | 40% (8/20) | 95% (19/20) | +55 pp |
| Avg key accuracy | 0.72 | 0.97 | +0.25 |
| Avg value accuracy | 0.65 | 0.93 | +0.28 |
| Responses with markdown fences | 7 (35%) | 0 (0%) | -35 pp |
| Responses with prose preamble | 9 (45%) | 1 (5%) | -40 pp |
| Responses with wrong schema keys | 3 (15%) | 1 (5%) | -10 pp |

## Per-Document Comparison

| Doc ID | Type | Baseline Valid? | Baseline Keys? | FT Valid? | FT Keys? | Improvement |
|--------|------|----------------|---------------|-----------|----------|-------------|
| EVAL-001 | Invoice | ❌ | ❌ | ✅ | ✅ | Fixed: removed prose + fences |
| EVAL-002 | Invoice | ✅ | ✅ | ✅ | ✅ | No change (already passing) |
| EVAL-003 | Invoice | ❌ | ❌ | ✅ | ✅ | Fixed: removed fences + corrected key names |
| EVAL-004 | Invoice | ❌ | ❌ | ✅ | ✅ | Fixed: removed prose preamble |
| EVAL-005 | Invoice | ✅ | ✅ | ✅ | ✅ | No change (already passing) |
| EVAL-006 | Invoice | ❌ | ❌ | ✅ | ✅ | Fixed: removed prose + fences |
| EVAL-007 | Invoice | ✅ | ✅ | ✅ | ✅ | No change (already passing) |
| EVAL-008 | Invoice | ❌ | ❌ | ✅ | ✅ | Fixed: removed prose + fixed date format |
| EVAL-009 | Invoice | ❌ | ✅ | ✅ | ✅ | Fixed: removed markdown fences |
| EVAL-010 | Invoice | ✅ | ✅ | ✅ | ✅ | No change (already passing) |
| EVAL-011 | Invoice | ❌ | ❌ | ✅ | ✅ | Fixed: removed prose + added missing keys |
| EVAL-012 | Invoice | ❌ | ✅ | ✅ | ✅ | Fixed: removed markdown fences |
| EVAL-013 | Invoice | ✅ | ✅ | ✅ | ✅ | No change (already passing) |
| EVAL-014 | Invoice | ❌ | ❌ | ❌ | ❌ | Still fails: prose preamble persists |
| EVAL-015 | Invoice | ❌ | ❌ | ✅ | ✅ | Fixed: removed prose + corrected type errors |
| EVAL-016 | PO | ❌ | ✅ | ✅ | ✅ | Fixed: removed markdown fences |
| EVAL-017 | PO | ✅ | ✅ | ✅ | ✅ | No change (already passing) |
| EVAL-018 | PO | ❌ | ❌ | ✅ | ✅ | Fixed: removed prose + corrected all key names |
| EVAL-019 | PO | ✅ | ✅ | ✅ | ✅ | No change (already passing) |
| EVAL-020 | PO | ❌ | ✅ | ✅ | ❌ | Partial: removed fences but used wrong array key |

## Key Findings

1. **Markdown code fences eliminated**: The most dramatic improvement. The base model wrapped 35% of responses in ` ```json ``` ` fences; the fine-tuned model uses fences in 0% of responses. Fine-tuning taught the model that raw JSON (no wrapper) is the expected output format.

2. **Prose preambles nearly eliminated**: Dropped from 45% to 5%. The single remaining failure (EVAL-014) suggests the model still occasionally falls back to conversational patterns for documents with unusual formatting (Egyptian export invoice with non-standard field ordering).

3. **Schema key consistency dramatically improved**: Wrong key names dropped from 15% to 5%. The base model would invent keys like `vendor_name`, `invoice_id`, `sub_total`; the fine-tuned model consistently uses the trained schema keys.

4. **Null handling learned**: The fine-tuned model correctly returns `null` for absent optional fields (due_date, tax, delivery_date) instead of omitting the key or using string placeholders like `"N/A"`.

5. **Date format standardized**: The base model sometimes returned dates as "September 7, 2024" or "28 December 2024"; the fine-tuned model consistently outputs YYYY-MM-DD format.

6. **Remaining failures are edge cases**: The 2 failures involve (a) a persistent prose habit on an unusual document and (b) confusion between `items` and `line_items` across invoice vs. PO schemas — both addressable with targeted training data additions.
