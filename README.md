# PCSS: Per-Example Calibrated Sigmoid Scaler

Official repository for **PCSS (Per-Example Calibrated Sigmoid Scaler)**.

This repository contains reproduction notebooks, evaluation scripts, and raw generation parquets for fine-tuning small base models on pure logic deduction traces (100–500 zebra puzzles).

For detailed mathematical derivations, empirical analyses, and discussion, see [`BLOG_POST.md`](BLOG_POST.md).

---

## Benchmark Results

For full empirical analysis, benchmark tables, and important evaluation notes (including details on sampling stochasticity and exploratory single-seed training dynamics), please refer to **Section 3** in [`BLOG_POST.md`](BLOG_POST.md).

---

## Hugging Face Models & Datasets

- **Datasets**: [`tamewild/zebra_100`](https://huggingface.co/datasets/tamewild/zebra_100) (100 samples) | [`tamewild/instruct5`](https://huggingface.co/datasets/tamewild/instruct5) (500 samples)
- **Flagship Models**: [`tamewild/PCSS-Qwen3-4B`](https://huggingface.co/tamewild/PCSS-Qwen3-4B) | [`tamewild/PCSS-Qwen3.5-9B`](https://huggingface.co/tamewild/PCSS-Qwen3.5-9B) | [`tamewild/PCSS-Granite-4.1-3B`](https://huggingface.co/tamewild/PCSS-Granite-4.1-3B)
- **4B Ablation Checkpoints**: See [`ABLATION_GUIDE.md`](ABLATION_GUIDE.md) for Hugging Face checkpoint links and configuration mappings across the 100-sample ablation matrix.

---

## Quickstart & Reproduction

For a detailed walkthrough, including individual evaluation scripts and exact prompt templates, see [`REPRODUCTION_GUIDE.md`](REPRODUCTION_GUIDE.md).

### 1. Recalculate Benchmark Scores (CPU)
Recalculate benchmark scores across all 46 evaluated configurations directly from raw generation files:

```bash
pip install -r requirements.txt
python scripts/recalculate_all.py
```

### 2. Reproduce Repetition & Looping Analysis (CPU)
Reproduce the Greedy GPQA Diamond repetition rate table from **Section 3.4** of [`BLOG_POST.md`](BLOG_POST.md) using the vendored `antidoom` repetition detection heuristic:

```bash
python scripts/analyze_looping_greedy.py
```

Or analyze generation loops across all standard evaluation runs:
```bash
python scripts/analyze_looping.py
```

### 3. Full Training & Inference (GPU)
Interactive end-to-end reproduction notebooks (tested on Vast.ai Hopper Docker `vastai/pytorch:2.10.0-cuda-13.0.2-py312-24.04-2026-03-26`):
- [`notebooks/qwen3_4b_base.ipynb`](notebooks/qwen3_4b_base.ipynb)
- [`notebooks/qwen3.5_9b_base.ipynb`](notebooks/qwen3.5_9b_base.ipynb)
- [`notebooks/granite4.1_3b_base.ipynb`](notebooks/granite4.1_3b_base.ipynb)
