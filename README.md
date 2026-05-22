# Structured Output Fine-Tuning: Llama 3.2 for Reliable JSON Extraction

Fine-tune Llama 3.2 3B-Instruct using LoRA (via LlamaFactory) to reliably extract structured JSON from unstructured business documents — invoices and purchase orders.

## Key Results

| Metric | Baseline (Pre-Training) | Fine-Tuned (Post-Training) |
|--------|------------------------|---------------------------|
| **Parse Success Rate** | 35% (7/20) | **90% (18/20)** |
| Avg Key Accuracy | 0.72 | 0.97 |
| Avg Value Accuracy | 0.65 | 0.93 |
| Markdown Fences | 35% of responses | 0% |
| Prose Preambles | 45% of responses | 5% |

## Project Overview

Enterprise document processing requires LLM outputs to be consistently machine-parseable JSON — not free-text responses wrapped in markdown or preceded by explanatory prose. This project demonstrates that LoRA fine-tuning on 80 curated examples transforms Llama 3.2's parse success rate from 35% to 90%, making it viable for production data pipelines.

## Methodology

1. **Schema Design**: Defined JSON schemas for invoices (9 keys) and purchase orders (8 keys) with strict type rules and null-handling conventions
2. **Data Curation**: Created 80 training examples (50 invoices + 30 POs) from CORD v2, SROIE, and synthetic sources with diverse layouts, currencies, and field combinations
3. **Baseline Evaluation**: Tested the base Llama 3.2 3B-Instruct model on 20 held-out documents
4. **LoRA Fine-Tuning**: Trained via LlamaFactory web UI (rank=16, alpha=32, lr=2e-4, 3 epochs)
5. **Post-Training Evaluation**: Re-tested on the same 20 documents with identical prompts
6. **Failure Analysis**: Deep-dived 5 remaining failure cases with data-centric fix proposals
7. **Prompt Engineering Comparison**: Tested 3 prompt strategies against fine-tuning

## Repository Structure

```
├── schema/
│   ├── invoice_schema.md        # Invoice JSON schema definition
│   └── po_schema.md             # Purchase order JSON schema definition
├── data/
│   ├── curated_train.jsonl      # 80 training examples (JSONL)
│   └── curation_log.md          # Detailed review log for each example
├── training_config.md           # Hyperparameter choices with justifications
├── screenshots/
│   ├── training_config.png      # LlamaFactory config panel screenshot
│   └── loss_curve.png           # Training loss curve screenshot
├── eval/
│   ├── baseline_responses.md    # Raw base model outputs (20 docs)
│   ├── baseline_scores.csv      # Baseline scoring metrics
│   ├── finetuned_responses.md   # Raw fine-tuned model outputs (20 docs)
│   ├── finetuned_scores.csv     # Fine-tuned scoring metrics
│   ├── before_vs_after.md       # Side-by-side comparison table
│   ├── summary.md               # Parse success rates summary
│   └── failures/
│       ├── failure_01.md        # Prose preamble on international doc
│       ├── failure_02.md        # Cross-schema key contamination
│       ├── failure_03.md        # Value extraction error (unit price)
│       ├── failure_04.md        # Hallucinated freight line item
│       └── failure_05.md        # Schema misidentification (sparse PO)
├── prompts/
│   ├── prompt_iterations.md     # 3 prompt engineering versions
│   └── prompt_eval.md           # Prompt vs fine-tuning results
├── report.md                    # Final analysis (~300 words)
└── README.md                    # This file
```

## Training Configuration

| Parameter | Value | Justification |
|-----------|-------|---------------|
| Base Model | Llama-3.2-3B-Instruct | Smallest instruct variant; fits on consumer hardware |
| Method | LoRA | 99% parameter reduction; CPU-feasible |
| LoRA Rank | 16 | Balanced capacity for JSON format learning |
| LoRA Alpha | 32 | Standard 2× rank scaling |
| Learning Rate | 2e-4 | Standard for LoRA fine-tuning |
| Epochs | 3 | Convergence without overfitting |
| Batch Size | 2 (effective 8) | RAM-constrained with gradient accumulation |

## Data Curation Summary

- **80 training examples**: 50 invoices + 30 purchase orders
- **15+ examples** with null optional fields (due_date, tax, delivery_date)
- **41 examples** with 3+ line items
- **35 examples** with non-USD currencies (EUR, GBP, INR, JPY)
- **5 distinct layout formats** per document type
- **10 rejected examples** documented with reasons

## Datasets Used

| Dataset | Purpose |
|---------|---------|
| [CORD v2](https://huggingface.co/datasets/naver-clova-ix/cord-v2) | Primary invoice/receipt source |
| [SROIE 2019](https://huggingface.co/datasets/AdamCodd/sroie2019) | Scanned receipt key-value pairs |
| [DocVQA](https://huggingface.co/datasets/nielsr/docvqa_1200_examples) | Diverse document layouts |
| [Invoices Donut Data](https://huggingface.co/datasets/katanaml-org/invoices-donut-data-v1) | Purchase order examples |

## Tools Used

- **LlamaFactory** — No-code Gradio web UI for LoRA fine-tuning
- **Hugging Face Datasets** — Dataset sourcing and exploration
- **Python** — JSON validation and metric computation
- **Llama 3.2 3B-Instruct** — Base model

## Key Findings

1. **Fine-tuning > Prompt Engineering for format reliability**: Best prompt achieved 67% parse rate on hardest docs; fine-tuning achieved 90% across all docs
2. **Behavioral vs. knowledge gaps**: Prompting fixes knowledge gaps (unknown schema); fine-tuning fixes behavioral gaps (conversational formatting habits)
3. **Data diversity matters more than data volume**: 80 examples with diverse layouts outperform more examples with repetitive formats
4. **Cross-schema confusion is a real risk**: Models trained on multiple schemas can conflate key names when document format is ambiguous

## License

This project is for educational purposes as part of the Partnr Global Placement Program.
