# Qwen 3 4B Ablation Checkpoints Guide

This guide indexes the fine-tuned model checkpoints for the **Qwen 3 4B Base 100-sample ablation matrix** described in Section 3.1 of [`BLOG_POST.md`](BLOG_POST.md).

To ensure complete transparency and independent verification without requiring re-training from scratch, all merged model weights are published on Hugging Face. Because these checkpoints are exploratory ablation artifacts rather than the primary model release, they retain their internal version identifiers (`4b_v<num>_merged_e5`).

For benchmark scores, empirical analysis, and important notes on single-seed variance across these 100-sample runs, please refer directly to **Section 3.1** in [`BLOG_POST.md`](BLOG_POST.md) and [`reports/RECALCULATION_REPORT.md`](reports/RECALCULATION_REPORT.md).

---

## Checkpoint & Configuration Mapping

All models below were fine-tuned on 100 5x5 zebra puzzle traces from [`tamewild/zebra_100`](https://huggingface.co/datasets/tamewild/zebra_100) starting from [`unsloth/Qwen3-4B-Base`](https://huggingface.co/unsloth/Qwen3-4B-Base) on a single NVIDIA H200 NVL GPU.

Unless otherwise specified in the table, all runs share the following base configuration:
- **Duration**: 5 epochs
- **Warmup**: 1-epoch linear warmup
- **Optimizer (8-bit AdamW)**: Runs with `bsz=1` use the scaled `beta2` parameter `0.99994`, while `bsz=16` uses the default `0.999`.
- **PEFT Defaults**: All LoRA configurations use `r=512, alpha=512` with a learning rate of `9e-5`. The MiSS run uses `r=512`.

> [!NOTE]
> To map exact evaluation `.parquet` files to their respective model versions, please refer to the `CONFIGS` dictionary in [`scripts/recalculate_all.py`](scripts/recalculate_all.py).

| Version | Configuration | Hugging Face Repository | Training Configuration |
| :--- | :--- | :--- | :--- |
| **v264** | **PCSS + MiSS** | [`tamewild/PCSS-Qwen3-4B`](https://huggingface.co/tamewild/PCSS-Qwen3-4B) | PCSS (beta=0.65, peak_scale=5.0), MiSS, bsz=1, Constant LR, LR=5e-6 |
| **v265** | **PCSS + LoRA** | [`tamewild/4b_v265_merged_e5`](https://huggingface.co/tamewild/4b_v265_merged_e5) | PCSS (beta=0.65, peak_scale=5.0), LoRA, bsz=1, Constant LR |
| **v267** | **LoRA bsz=1 (Cosine)** | [`tamewild/4b_v267_merged_e5`](https://huggingface.co/tamewild/4b_v267_merged_e5) | LoRA, bsz=1, Cosine Decay |
| **v268** | **LoRA bsz=1 (Constant)** | [`tamewild/4b_v268_merged_e5`](https://huggingface.co/tamewild/4b_v268_merged_e5) | LoRA, bsz=1, Constant LR |
| **v266** | **LoRA bsz=16 (Cosine)** | [`tamewild/4b_v266_merged_e5`](https://huggingface.co/tamewild/4b_v266_merged_e5) | LoRA, bsz=16, Cosine Decay |

---

## Usage & Inference

All checkpoints are standard merged full-weight models compatible with vLLM and Transformers.

### Serving with vLLM

To serve any ablation checkpoint (e.g. `tamewild/4b_v265_merged_e5`):

```bash
vllm serve tamewild/4b_v265_merged_e5 \
  --max-model-len 32000 \
  --generation-config vllm \
  --host 127.0.0.1 \
  --port 18000 \
  --gpu-memory-utilization 0.90
```

### Prompt Formats

Evaluations were conducted using the following zero-shot Chain-of-Thought templates:

#### Mathematical Benchmarks (MATH-500, Full MATH, AIME 2025)

```text
{problem}

Please reason step by step, and put your final answer within \boxed{}
```

#### Logic Grid Benchmarks (Zebra Puzzles)

```text
{problem}

Provide the solution grid as the final answer.

Please reason step by step, and put your final answer within \boxed{}
```
