# PCSS Evaluation & Reproduction Guide

This document provides instructions for reproducing all benchmark results for **PCSS (Per-Example Calibrated Sigmoid Scaler)** across two modes:

1. **Score Recalculation from Raw Generations (CPU)**: Verify all reported scores across 46 evaluation configurations in `eval_runs/standard/` using `math-verify`, boxed letter extraction, and grid parsers.
2. **Full Training & Inference from Scratch (GPU)**: Fine-tune base models on pure logic micro-datasets (100–500 zebra puzzles) and generate new benchmark responses via vLLM.

---

## 1. Score Recalculation from Raw Generations (CPU)

All 46 raw model generation parquets across 46 evaluation configurations are provided in `eval_runs/standard/`.

### Installation

```bash
pip install -r requirements.txt
```

### Running Full Recalculation Suite

To parse all 46 parquet files and generate the complete benchmark matrix:

```bash
python scripts/recalculate_all.py
```

This will output results to the console and save the summary to [`reports/RECALCULATION_REPORT.md`](reports/RECALCULATION_REPORT.md).

### Running Individual Benchmark Parsers

You can also evaluate specific parquet files individually:

#### A. Mathematics Benchmarks (MATH-500, Full MATH, AIME 2025, AIME 2026, ArXivMath)
Evaluated using Hugging Face `math-verify`:
```bash
# Evaluate Qwen 3.5 9B (PCSS + MiSS) on AIME 2025 (Pass@1 and Pass@3)
python scripts/recalculate_math.py eval_runs/standard/aime25_9b_v30_e5_16k_rerun.parquet --k 1 3

# Evaluate Qwen 3.5 9B (PCSS + MiSS) on ArXivMath 05/26 (Pass@1 and Pass@3)
python scripts/recalculate_math.py eval_runs/standard/9b_v30_e5_arxivmath_0526.parquet --k 1 3

# Evaluate Qwen 3 4B (PCSS + MiSS) on Full 5,000 MATH benchmark
python scripts/recalculate_math.py eval_runs/standard/4b_v264_e5_full_math_16k.parquet --k 1

# Evaluate Granite 4.1 3B (PCSS + MiSS) on MATH-500
python scripts/recalculate_math.py eval_runs/standard/3b_granite_v3_math500_16k.parquet --k 1
```

#### B. Logic Deduction Benchmarks (4x4, 5x5, 6x6 Zebra Puzzles)
Evaluated using grid and LaTeX table parsers:
```bash
# Evaluate Qwen 3.5 9B (PCSS + MiSS) on 5x5 Zebra (Pass@1 and Pass@3)
python scripts/recalculate_zebra.py eval_runs/standard/9b_v30_e5_5x5_zebra_16k.parquet --k 1 3

# Evaluate Qwen 3 4B (PCSS + MiSS) on 4x4 Zebra
python scripts/recalculate_zebra.py eval_runs/standard/4b_v264_e5_4x4_zebra_16k_rerun.parquet --k 1
```

#### C. Multiple-Choice Benchmarks (GPQA Diamond, MMLU Redux)
Evaluated using boxed letter extraction:
```bash
# Evaluate Qwen 3.5 9B (PCSS + MiSS) on GPQA Diamond
python scripts/recalculate_mcq.py eval_runs/standard/9b_v30_e5_gpqa_diamond_16k.parquet --k 1

# Evaluate Qwen 3.5 9B (PCSS + MiSS) on MMLU Redux
python scripts/recalculate_mcq.py eval_runs/standard/9b_v30_e5_mmlu_redux_16k.parquet --k 1
```

#### D. Repetition & Looping Analysis (antidoom)
Repetition failure modes ("doom loops") are detected using Liquid AI's [`antidoom`](https://github.com/Liquid4All/antidoom) inner-repetition detection heuristic, vendored in `raw_eval_snippets/antidoom/`:

```bash
# Reproduce Section 3.4 Greedy GPQA Diamond Looping Rates
python scripts/analyze_looping_greedy.py

# Expected Output:
# ================================================================================
# Greedy GPQA Diamond Looping Rates (Section 3.4 Reproduction)
# ================================================================================
# Model (Greedy GPQA Diamond)                | Looping Samples   | Looping Rate
# --------------------------------------------------------------------------------
# Qwen 3.5 9B Base (Untrained)               | 36 / 594          |  6.06%
# Qwen 3.5 9B Official Post-Trained          | 31 / 594          |  5.22%
# Qwen 3.5 9B Base (PCSS Fine-Tuned)         | 4 / 594           |  0.67%
# --------------------------------------------------------------------------------

# Analyze repetition rates across all standard benchmark runs
python scripts/analyze_looping.py

# Or analyze a specific parquet file
python scripts/analyze_looping.py eval_runs/standard/9b_v30_e5_5x5_zebra_16k.parquet
```

#### E. Token Generation Length Analysis

Calculate token length statistics (median, average, and max completion tokens) on model generation outputs:

```bash
# Reproduce Section 3.4 MATH-500 completion token length statistics
python scripts/analyze_tokens.py

# Analyze 5x5 and 6x6 Zebra puzzle generation lengths (saves summary table to reports/ZEBRA_LENGTH_REPORT.md)
python scripts/analyze_zebra_lengths.py
```

---

## 2. Full End-to-End Training & Inference (GPU)

Self-contained Jupyter notebooks are provided in `notebooks/`.

### Recommended Environment & Hardware

* **Base Docker Image**: `vastai/pytorch:2.10.0-cuda-13.0.2-py312-24.04-2026-03-26`
* **Hardware**: NVIDIA H100 SXM / H200 NVL (Hopper architecture with `cu130` and FlashAttention-3).
* *Other GPUs (e.g. A100, RTX 4090)*: In the model initialization cell, set `attn_implementation="sdpa"` instead of FlashAttention-3.

### Reproduction Notebooks

| Model | Notebook | Dataset | Hardware / Time |
|---|---|---|---|
| **Qwen 3 4B Base** | [`notebooks/qwen3_4b_base.ipynb`](notebooks/qwen3_4b_base.ipynb) | [`tamewild/zebra_100`](https://huggingface.co/datasets/tamewild/zebra_100) (100 samples) | 1x H100 SXM (~6.5 min) |
| **Qwen 3.5 9B Base (MTP)** | [`notebooks/qwen3.5_9b_base.ipynb`](notebooks/qwen3.5_9b_base.ipynb) | [`tamewild/instruct5`](https://huggingface.co/datasets/tamewild/instruct5) (500 samples) | 1x H100 SXM (~40 min) |
| **Granite 4.1 3B Base** | [`notebooks/granite4.1_3b_base.ipynb`](notebooks/granite4.1_3b_base.ipynb) | [`tamewild/instruct5`](https://huggingface.co/datasets/tamewild/instruct5) (500 samples) | 1x H100 SXM (~24 min) |

> **Note on Reproduction & Determinism:** All notebooks provided above use the **exact same hyperparameters, datasets, and training configurations** as the primary published checkpoints. However, they represent independent reproduction runs. Because training is not perfectly deterministic (and vLLM introduces slight variance during evaluation), running these notebooks will yield scores in the same neighborhood as the released models, rather than exact matches. For example, while the primary released Qwen 3.5 9B checkpoint was trained on an H200 NVL (scoring 60.67% on AIME 2025), its corresponding reproduction notebook was tested on an H100 SXM and achieves ~58%.

### Notebook Execution Flow
1. **Dependencies**: Installs pinned Transformers, TRL, PEFT, BitsAndBytes, and Liger-Kernel via `uv`.
2. **Reference Loss Pre-computation**: Evaluates frozen base model (`with torch.no_grad():`) to compute and attach `L_ref` per sample.
3. **PEFT Setup**: Configures MiSS (`r=512`) in `bfloat16` (`autocast_adapter_dtype=False`).
4. **PCSS Training**: Trains 5 epochs at batch size 1 with `beta2=0.99994`, constant learning rate (`5e-6`) with a 1-epoch linear warmup, and PCSS loss scaling.
5. **Adapter Merge**: Merges adapter into base model in `fp32` (`autocast_adapter_dtype=True`) and saves `./merged`.
6. **vLLM Benchmark Verification**: Launches vLLM (0.19.1) and evaluates the merged model on MATH-500 or AIME 2025.

---

## 3. Evaluation Prompts & Sampling Parameters

### System Prompt
**No system prompt was used for any benchmark evaluation.**

### Prompt Templates

#### 1. Mathematics Benchmarks (MATH-500, Full MATH, AIME 2025, AIME 2026, ArXivMath)
```
{problem}

Please reason step by step, and put your final answer within \boxed{}
```

#### 2. Multiple-Choice Benchmarks (GPQA Diamond, MMLU Redux)
```
{problem}

Please reason step by step, and put your final letter choice within \boxed{\text{}}
```

#### 3. Logic / Zebra Deduction Puzzles (Fine-Tuned Models Expecting LaTeX Grid)
```
{problem}

Provide the solution grid as the final answer.

Please reason step by step, and put your final answer within \boxed{}
```

#### 4. Logic / Zebra Deduction Puzzles (Official Post-Trained Qwen 3.5 9B Expecting Markdown Table)
```
{problem}

Provide the solution table as the final answer.
```

> **Notes:**
> - **Prompt Rationale**: The prompt was adjusted for the official post-trained model to request a markdown table, as it struggled to consistently output parsable LaTeX grids.
> - **Data Storage**: In some stored `.parquet` files in `eval_runs/standard/`, the zero-shot prompt string was appended directly to the problem text column during serialization, while in others the problem column contains only the raw benchmark question text (with the prompt template applied during inference prompt formatting). Since evaluation scripts evaluate the generated response strings in `samples` against ground truth answers, this difference does not affect score verification.

---

### Decoding & Sampling Configurations

All evaluations used a maximum generation length of **16,384** tokens.

- **Qwen 3.5 9B Models**: Sampled decoding with `temperature=1.0`, `top_p=0.95`, `top_k=20`. For the official post-trained model, `presence_penalty=1.5` was applied per Qwen's recommendation; for base and PCSS fine-tuned checkpoints, no presence penalty was applied.
- **Granite 4.1 3B & Qwen 3 4B Models**: Greedy decoding.
- **Pass@k Estimation**: For sampled evaluations with multiple generations per problem (`n >= 6`), unbiased Pass@k estimates were computed using the Codex pass@k formulation:
  ```text
  Pass@k = 1 - binom(n - c, k) / binom(n, k)
  ```

---

### Serving & Evaluation Setup (Qwen 3.5 9B)

Qwen 3.5 9B Base was released with its chat template control tokens (e.g. `<|im_start|>`, `<|im_end|>`) pre-trained into the base weights. To evaluate the untrained base baseline and the fine-tuned model under the identical zero-shot CoT setup in non-thinking mode, models were served using vLLM (0.19.1):

#### 1. Evaluating the Untrained Base Model
For the raw `Qwen/Qwen3.5-9B-Base` checkpoint (which lacks `chat_template.jinja` in the upstream base repository), fetch the template and launch:

```bash
curl -o chat_template.jinja https://huggingface.co/unsloth/Qwen3.5-9B/raw/main/chat_template.jinja

vllm serve Qwen/Qwen3.5-9B-Base \
  --max-model-len 32000 \
  --language-model-only \
  --generation-config vllm \
  --chat-template chat_template.jinja \
  --host 127.0.0.1 \
  --port 18000 \
  --gpu-memory-utilization 0.95 \
  --default-chat-template-kwargs '{"enable_thinking": false}' \
  --speculative-config '{"method": "mtp", "num_speculative_tokens": 2}'
```

#### 2. Evaluating the PCSS Fine-Tuned Model
The fine-tuned repository (`tamewild/PCSS-Qwen3.5-9B`) bundles `chat_template.jinja` directly:

```bash
vllm serve tamewild/PCSS-Qwen3.5-9B \
  --max-model-len 32000 \
  --language-model-only \
  --generation-config vllm \
  --host 127.0.0.1 \
  --port 18000 \
  --gpu-memory-utilization 0.95 \
  --default-chat-template-kwargs '{"enable_thinking": false}' \
  --speculative-config '{"method": "mtp", "num_speculative_tokens": 2}'
```
