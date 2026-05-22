# Training Configuration — LlamaFactory LoRA Fine-Tuning

## Model

- **Base Model**: `meta-llama/Llama-3.2-3B-Instruct`
- **Model Size**: 3.21 billion parameters
- **Justification**: Llama 3.2 3B-Instruct is the smallest instruction-tuned variant in the Llama 3.2 family. Its compact size enables fine-tuning on consumer hardware (CPU/limited GPU) while still offering strong instruction-following capability. The instruct variant is preferred over the base model because it already understands instruction-response formatting, reducing the amount of behavioral learning the fine-tuning needs to accomplish — our fine-tuning only needs to teach JSON schema adherence, not instruction following from scratch.

## Fine-Tuning Method

- **Method**: LoRA (Low-Rank Adaptation)
- **Justification**: LoRA freezes all pre-trained weights and inserts small trainable adapter matrices into the attention layers. This reduces trainable parameters by ~99%, from 3.2B to ~3.4M, making fine-tuning feasible on a machine with 16GB RAM and no dedicated GPU. Full fine-tuning would require 40+ GB of memory and multiple GPUs.

## LoRA Hyperparameters

### LoRA Rank: 16

- **Range considered**: 8, 16, 32
- **Chosen value**: 16
- **Justification**: Rank controls the dimensionality of the adapter matrices. For this task, the model needs to learn a specific output format (JSON schema) rather than new knowledge — this is a format-constrained generation task. Rank 8 would provide minimal capacity and risks underfitting on the structural complexity of nested JSON with arrays. Rank 32 would be excessive for 80 training examples and increases overfitting risk. Rank 16 provides sufficient capacity to learn the JSON formatting patterns (key ordering, nesting, type consistency) without over-parameterizing relative to our small dataset.

### LoRA Alpha: 32

- **Chosen value**: 32 (2× rank)
- **Justification**: Alpha is the scaling factor applied to the LoRA adapter outputs before they are added to the frozen weights. The standard practice is to set alpha = 2 × rank, which produces an effective learning rate scaling of alpha/rank = 2.0. This scaling ensures the adapter updates have meaningful influence on the model's outputs without being so large that they destabilize the pre-trained representations. With alpha = 2 × rank, the effective contribution of LoRA updates is normalized, making the learning rate hyperparameter more interpretable and transferable across different rank choices.

### LoRA Target Modules: `q_proj, v_proj`

- **Justification**: Targeting the query and value projection matrices in the self-attention layers is the standard LoRA configuration. These matrices control what the model attends to (query) and what information it retrieves (value). For structured output tasks, attention patterns are the primary mechanism the model uses to track which JSON keys have been emitted and which remain — making Q and V the highest-leverage intervention points.

### LoRA Dropout: 0.05

- **Justification**: A small dropout (5%) on the adapter layers provides mild regularization against overfitting on 80 examples without significantly reducing training signal. Higher dropout (e.g., 0.1–0.2) would slow convergence on our already-small dataset.

## Training Hyperparameters

### Learning Rate: 2e-4

- **Range considered**: 1e-4 to 3e-4
- **Chosen value**: 2e-4
- **Justification**: This is the standard learning rate for LoRA fine-tuning of instruction-tuned models. Lower rates (1e-4) would require more epochs to converge on 80 examples, increasing total training time without clear benefit. Higher rates (3e-4) risk overshooting and unstable loss curves, particularly in early training when the adapter weights are randomly initialized. 2e-4 provides reliable convergence within 3 epochs based on published LoRA fine-tuning results on similar-sized datasets.

### Epochs: 3

- **Range considered**: 2–5
- **Chosen value**: 3
- **Justification**: With 80 training examples, each epoch processes the full dataset once. At 2 epochs, the model may not fully learn the consistent JSON schema patterns across all 80 examples — particularly the null-handling rules and multi-item array formatting. At 4–5 epochs, the model risks overfitting: memorizing specific vendor names and amounts rather than learning the generalizable extraction-to-JSON mapping. Three epochs provides a standard balance. The loss curve confirmed this: loss decreased steadily through epoch 2, began plateauing in epoch 3, suggesting the model had learned the target patterns without memorizing specific examples.

### Batch Size: 2

- **Chosen value**: 2
- **Justification**: Constrained by available system RAM (16GB). Each training example contains both the raw document text (input) and the JSON output, which tokenize to approximately 300–600 tokens each. With Llama 3.2 3B's model footprint and LoRA adapters loaded, a batch size of 2 fits within memory limits. Gradient accumulation steps are set to 4, giving an effective batch size of 8, which provides stable gradient estimates for the small dataset.

### Gradient Accumulation Steps: 4

- **Effective batch size**: 2 × 4 = 8
- **Justification**: Simulates a larger batch size without exceeding memory limits. An effective batch size of 8 means the model sees 8 examples before each weight update, which is 10% of the dataset — providing reasonably stable gradient estimates while still updating frequently enough to converge in 3 epochs.

### Warmup Steps: 10

- **Justification**: With 80 examples, batch size 2, and gradient accumulation 4, each epoch has 10 optimizer steps (80 / 2 / 4 = 10). Warming up over 10 steps (1 full epoch) gradually increases the learning rate from 0 to 2e-4, preventing the randomly initialized LoRA adapters from producing large, destabilizing gradient updates in early training.

### Weight Decay: 0.01

- **Justification**: Standard L2 regularization to prevent adapter weight magnitudes from growing unchecked. At 0.01, the regularization pressure is minimal but provides a gentle bias toward smaller weights, which helps generalization on unseen document layouts.

### Max Sequence Length: 1024

- **Justification**: Our longest training example (input + output) tokenizes to approximately 700 tokens. Setting max length to 1024 provides headroom for longer documents without wasting memory on padding for the shorter examples (which are packed efficiently by LlamaFactory's data collator).

## Quantization

- **Quantization**: None (full precision fp32)
- **Justification**: While 4-bit quantization (QLoRA) would reduce memory usage, it introduces quantization noise that can slightly reduce fine-tuning quality. Since our model fits in memory at fp32 with LoRA, we avoid this trade-off.

## Loss Curve Analysis

The training loss curve (see `screenshots/loss_curve.png`) shows:

1. **Epoch 1 (steps 1–10)**: Loss drops sharply from ~2.8 to ~1.2. The model quickly learns the basic JSON output structure — opening/closing braces, key-value syntax, and the instruction-to-JSON mapping.

2. **Epoch 2 (steps 11–20)**: Loss continues decreasing from ~1.2 to ~0.6. The model refines key naming consistency, null handling, and array formatting for line_items/items.

3. **Epoch 3 (steps 21–30)**: Loss plateaus around ~0.45–0.55. The model has learned the target patterns. The plateau indicates convergence rather than further memorization — training was correctly stopped here.

**Overfitting assessment**: The loss did NOT drop to near-zero, which would indicate memorization. A final training loss of ~0.5 indicates the model has learned the general JSON formatting behavior while retaining some uncertainty about specific values — which is the desired outcome. The model should predict the JSON structure with high confidence but remain uncertain about specific field values (which vary per document).

## Training Runs

### Run 1 (Final)
- **Configuration**: As described above (rank=16, alpha=32, lr=2e-4, epochs=3, batch=2, accum=4)
- **Duration**: ~45 minutes on CPU
- **Final loss**: ~0.50
- **Result**: Accepted — loss curve shows healthy convergence without overfitting

### Run 0 (Exploratory — discarded)
- **Configuration**: rank=8, alpha=16, lr=3e-4, epochs=5
- **Duration**: ~60 minutes on CPU
- **Final loss**: ~0.15
- **Result**: Rejected — loss dropped too fast and too low by epoch 3, indicating overfitting. Evaluation showed the model memorized training vendor names and produced them even for unseen documents. Increased rank to 16 and reduced epochs to 3 for the final run.
