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
        description="Analyze generation looping rates across evaluation runs using antidoom."
    )
    parser.add_argument(
        "parquet_files",
        nargs="*",
        help="Optional parquet file(s) to analyze. Defaults to all in eval_runs/standard/ and eval_runs/greedy_looping/",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Optional path to write a Markdown report. Defaults to reports/LOOPING_REPORT.md when running full suite.",
    )
    args = parser.parse_args()

    custom_files_mode = bool(args.parquet_files)
    if custom_files_mode:
        files = [Path(f) for f in args.parquet_files]
        default_out = args.output
    else:
        eval_dir = Path(os.path.join(BASE_DIR, "eval_runs"))
        if not eval_dir.exists():
            print(f"Directory {eval_dir} not found.")
            sys.exit(1)
        files = sorted(eval_dir.glob("**/*.parquet"))
        default_out = args.output or os.path.join(BASE_DIR, "reports", "LOOPING_REPORT.md")

    if not files:
        print("No parquet files found to analyze.")
        sys.exit(1)

    lines = []
    lines.append("# Generation Looping Analysis Report\n")
    lines.append("This report analyzes generation looping across evaluation runs using Liquid AI's `antidoom` repetition detection heuristic.\n")
    lines.append(f"| {'Run Name':<45} | {'Total Samples':<13} | {'Looping Samples':<15} | {'Looping %':<10} |")
    lines.append(f"|{'-' * 47}|{'-' * 15}|{'-' * 17}|{'-' * 12}|")

    print(f"Analyzing {len(files)} parquet file(s)...")
    for pf in files:
        if not pf.exists():
            print(f"File not found: {pf}")
            continue
        total, looping = analyze_parquet(pf)
        if total > 0:
            pct = (looping / total) * 100
            line = f"| {pf.stem:<45} | {total:<13} | {looping:<15} | {pct:>8.2f}% |"
            lines.append(line)
            print(f"  {pf.stem}: {looping}/{total} ({pct:.2f}%)")
        else:
            line = f"| {pf.stem:<45} | {'0':<13} | {'0':<15} | {'N/A':>8} |"
            lines.append(line)

    report_str = "\n".join(lines) + "\n"
    if default_out:
        out_path = Path(default_out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w") as f:
            f.write(report_str)
        print(f"\nReport successfully generated: {out_path}")

if __name__ == "__main__":
    main()
