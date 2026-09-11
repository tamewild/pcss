import os
import sys
import argparse
from pathlib import Path
import pandas as pd
import numpy as np

# Add raw_eval_snippets to path to import antidoom
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, "raw_eval_snippets"))

try:
    from antidoom.repetition import find_inner_repetition
except ImportError as e:
    print(f"Failed to import antidoom from raw_eval_snippets: {e}")
    sys.exit(1)

# Display names for the Section 3.4 Blog Post table
DISPLAY_NAMES = {
    "9b_official_base_gpqa_diamond_16k_greedy": "Qwen 3.5 9B Base (Untrained)",
    "9b_official_gpqa_diamond_16k_greedy": "Qwen 3.5 9B Official Post-Trained",
    "9b_v30_e5_gpqa_diamond_16k_greedy": "Qwen 3.5 9B Base (PCSS Fine-Tuned)",
}

def analyze_parquet(filepath):
    df = pd.read_parquet(filepath)
    if "samples" not in df.columns:
        return 0, 0

    total_samples = 0
    looping_samples = 0

    for idx, row in df.iterrows():
        samples_list = row["samples"]
        if samples_list is None:
            continue

        if isinstance(samples_list, np.ndarray):
            samples_list = samples_list.tolist()
        elif not isinstance(samples_list, (list, tuple)):
            continue

        for sample in samples_list:
            if not isinstance(sample, str):
                continue
            total_samples += 1

            is_loop, _ = find_inner_repetition(sample)
            if is_loop:
                looping_samples += 1

    return total_samples, looping_samples

def main():
    parser = argparse.ArgumentParser(
        description="Reproduce Section 3.4 Greedy GPQA Diamond Looping Rates using antidoom."
    )
    parser.add_argument(
        "parquet_files",
        nargs="*",
        help="Optional specific parquet file(s) to analyze. Defaults to all in eval_runs/greedy_looping/",
    )
    args = parser.parse_args()

    if args.parquet_files:
        files = [Path(f) for f in args.parquet_files]
    else:
        eval_dir = Path(os.path.join(BASE_DIR, "eval_runs", "greedy_looping"))
        if not eval_dir.exists():
            print(f"Directory {eval_dir} not found.")
            sys.exit(1)
        files = sorted(eval_dir.glob("*.parquet"))

    if not files:
        print("No parquet files found to analyze.")
        sys.exit(1)

    print("=" * 80)
    print("Greedy GPQA Diamond Looping Rates (Section 3.4 Reproduction)")
    print("=" * 80)
    print(f"{'Model (Greedy GPQA Diamond)':<42} | {'Looping Samples':<17} | {'Looping Rate'}")
    print("-" * 80)

    for pf in files:
        stem = pf.stem
        display_name = DISPLAY_NAMES.get(stem, stem)
        total, looping = analyze_parquet(pf)
        if total > 0:
            rate = (looping / total) * 100
            print(f"{display_name:<42} | {f'{looping} / {total}':<17} | {rate:>5.2f}%")
        else:
            print(f"{display_name:<42} | {'0 / 0':<17} | N/A")

    print("-" * 80)

if __name__ == "__main__":
    main()
