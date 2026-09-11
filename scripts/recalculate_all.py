import os
import subprocess
import glob
import pandas as pd

import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define the exact configurations based on RESULTS.md
# Format: (Filename, Benchmark Name, [k values], script)
CONFIGS = [
    # Qwen 3.5 9B v30
    ("9b_v30_e5_mmlu_redux_16k.parquet", "MMLU Redux (16k, avg 1)", [1], "scripts/recalculate_mcq.py"),
    ("9b_v30_e5_gpqa_diamond_16k.parquet", "GPQA Diamond (16k, avg 3)", [1], "scripts/recalculate_mcq.py"),
    ("aime25_9b_v30_e5_16k_rerun.parquet", "AIME25 (16k, avg 10)", [1, 3], "scripts/recalculate_math.py"),
    ("aime26_9b_v30_e5_16k_rerun.parquet", "AIME26 (16k, avg 10)", [1, 3], "scripts/recalculate_math.py"),
    ("9b_v30_e5_math500_16k.parquet", "MATH-500 (16k, avg 3)", [1], "scripts/recalculate_math.py"),
    ("9b_v30_e5_arxivmath_0526.parquet", "ArXivMath 05/26 (16k, avg 6)", [1, 3], "scripts/recalculate_math.py"),
    ("9b_v30_e5_5x5_zebra_16k.parquet", "5x5 Zebra (16k, avg 6)", [1, 3], "scripts/recalculate_zebra.py"),
    ("9b_v30_e5_6x6_zebra_16k.parquet", "6x6 Zebra (16k, avg 3)", [1], "scripts/recalculate_zebra.py"),

    # Qwen 3.5 9B Official
    ("9b_official_mmlu_redux_16k_correct.parquet", "MMLU Redux (16k, avg 1)", [1], "scripts/recalculate_mcq.py"),
    ("9b_official_gpqa_diamond_16k_correct.parquet", "GPQA Diamond (16k, avg 3)", [1], "scripts/recalculate_mcq.py"),
    ("aime25_9b_official_16k.parquet", "AIME25 (16k, avg 6)", [1, 3], "scripts/recalculate_math.py"),
    ("aime26_9b_official_16k.parquet", "AIME26 (16k, avg 6)", [1, 3], "scripts/recalculate_math.py"),
    ("9b_official_math500_16k.parquet", "MATH-500 (16k, avg 3)", [1], "scripts/recalculate_math.py"),
    ("9b_official_arxivmath_0526.parquet", "ArXivMath 05/26 (16k, avg 6)", [1, 3], "scripts/recalculate_math.py"),
    ("9b_official_5x5_zebra_16k.parquet", "5x5 Zebra (16k, avg 3)", [1], "scripts/recalculate_zebra.py"),
    ("9b_official_6x6_zebra_16k.parquet", "6x6 Zebra (16k, avg 3)", [1], "scripts/recalculate_zebra.py"),

    # Qwen 3.5 9B Base
    ("9b_official_base_mmlu_redux_16k.parquet", "MMLU Redux (16k, avg 1)", [1], "scripts/recalculate_mcq.py"),
    ("9b_official_base_gpqa_diamond_16k.parquet", "GPQA Diamond (16k, avg 3)", [1], "scripts/recalculate_mcq.py"),
    ("aime25_9b_official_base_16k.parquet", "AIME25 (16k, avg 6)", [1, 3], "scripts/recalculate_math.py"),
    ("aime26_9b_official_base_16k.parquet", "AIME26 (16k, avg 6)", [1, 3], "scripts/recalculate_math.py"),
    ("9b_official_base_math500_16k.parquet", "MATH-500 (16k, avg 3)", [1], "scripts/recalculate_math.py"),
    ("9b_official_base_arxivmath_0526.parquet", "ArXivMath 05/26 (16k, avg 6)", [1, 3], "scripts/recalculate_math.py"),
    ("9b_official_base_5x5_zebra_16k.parquet", "5x5 Zebra (16k, avg 3)", [1], "scripts/recalculate_zebra.py"),

    # Granite 3B Base (PCSS + MiSS, v3)
    ("aime25_3b_granite_v3_16k_greedy.parquet", "AIME25 (16k, avg 6)", [1], "scripts/recalculate_math.py"),
    ("3b_granite_v3_math500_16k.parquet", "MATH-500 (16k, avg 3)", [1], "scripts/recalculate_math.py"),
    ("3b_granite_v3_5x5_zebra_16k.parquet", "5x5 Zebra (16k, avg 6)", [1], "scripts/recalculate_zebra.py"),

    # Granite 3B Instruct official
    ("aime25_3b_granite_official_16k_greedy.parquet", "AIME25 (16k, avg 6)", [1], "scripts/recalculate_math.py"),
    ("3b_granite_official_math500_16k.parquet", "MATH-500 (16k, avg 3)", [1], "scripts/recalculate_math.py"),


    # 4B v264
    ("4b_v264_e5_math500_16k_rerun.parquet", "MATH-500 (16k, avg 3)", [1], "scripts/recalculate_math.py"),
    ("4b_v264_e5_full_math_16k.parquet", "MATH (full 5,000, 16k)", [1], "scripts/recalculate_math.py"),
    ("aime25_4b_v264_e5_16k_greedy.parquet", "AIME25 (16k, avg 6)", [1], "scripts/recalculate_math.py"),
    ("4b_v264_e5_5x5_zebra_16k.parquet", "5x5 Zebra (16k, avg 3)", [1], "scripts/recalculate_zebra.py"),
    ("4b_v264_e5_4x4_zebra_16k_rerun.parquet", "4x4 Zebra (16k, avg 3)", [1], "scripts/recalculate_zebra.py"),

    # 4B v266
    ("4b_v266_e5_math500_16k.parquet", "MATH-500 (16k, avg 1)", [1], "scripts/recalculate_math.py"),
    ("aime25_4b_v266_e5_16k_greedy.parquet", "AIME25 (16k, avg 6)", [1], "scripts/recalculate_math.py"),
    ("4b_v266_e5_4x4_zebra_16k.parquet", "4x4 Zebra (16k, avg 3)", [1], "scripts/recalculate_zebra.py"),

    # 4B v267
    ("4b_v267_e5_math500_16k.parquet", "MATH-500 (16k, avg 1)", [1], "scripts/recalculate_math.py"),
    ("aime25_4b_v267_e5_16k_greedy.parquet", "AIME25 (16k, avg 6)", [1], "scripts/recalculate_math.py"),
    ("4b_v267_e5_4x4_zebra_16k.parquet", "4x4 Zebra (16k, avg 3)", [1], "scripts/recalculate_zebra.py"),

    # 4B v268
    ("4b_v268_e5_math500_16k.parquet", "MATH-500 (16k, avg 1)", [1], "scripts/recalculate_math.py"),
    ("aime25_4b_v268_e5_16k_greedy.parquet", "AIME25 (16k, avg 6)", [1], "scripts/recalculate_math.py"),
    ("4b_v268_e5_4x4_zebra_16k.parquet", "4x4 Zebra (16k, avg 3)", [1], "scripts/recalculate_zebra.py"),

    # 4B v265
    ("4b_v265_e5_math500_16k.parquet", "MATH-500 (16k, avg 3)", [1], "scripts/recalculate_math.py"),
    ("aime25_4b_v265_e5_16k_greedy.parquet", "AIME25 (16k, avg 6)", [1], "scripts/recalculate_math.py"),
    ("4b_v265_e5_5x5_zebra_16k.parquet", "5x5 Zebra (16k, avg 3)", [1], "scripts/recalculate_zebra.py"),
    ("4b_v265_e5_4x4_zebra_16k.parquet", "4x4 Zebra (16k, avg 3)", [1], "scripts/recalculate_zebra.py"),
]

def run_eval(script, parquet_file, k_args):
    eval_path = os.path.join(BASE_DIR, "eval_runs", "standard", parquet_file)
    script_path = os.path.join(BASE_DIR, script)
    python_bin = sys.executable
    cmd = [python_bin, script_path, eval_path, "--k"] + [str(x) for x in k_args]
    print(f"Running: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        passes = {}
        for line in result.stdout.split('\n'):
            if line.startswith("Pass@"):
                parts = line.split(":")
                k_val = parts[0].replace("Pass@", "")
                score = parts[1].strip()
                passes[k_val] = score
        return passes
    except subprocess.CalledProcessError as e:
        print(f"Error running {parquet_file}: {e}")
        return {}

def format_row(benchmark_name, passes, expected_ks):
    s = f"- {benchmark_name}: "
    if 1 in expected_ks and '1' in passes:
        s += f"{passes['1']}"
    if 3 in expected_ks and '3' in passes:
        s += f"\n    - Pass@3: {passes['3']}"
    return s

def main():
    eval_dir = os.path.join(BASE_DIR, "eval_runs", "standard")
    results = {}
    for filename, bench, ks, script in CONFIGS:
        target_file = os.path.join(eval_dir, filename)
        if not os.path.exists(target_file):
            print(f"File {filename} not found, skipping...")
            passes = {str(k): "N/A" for k in ks}
        else:
            df = pd.read_parquet(target_file)
            actual_n = len(df.iloc[0].samples) if len(df) > 0 and hasattr(df.iloc[0], 'samples') else None
            if actual_n and "avg " in bench:
                bench = bench.replace(f"avg {bench.split('avg ')[-1].split(')')[0]}", f"avg {actual_n}")
            
            passes = run_eval(script, filename, ks)
        
        results[filename] = (bench, passes, ks)

    sections = [
        ("Qwen 3.5 9B Base (PCSS + MiSS, v30)", [
            "9b_v30_e5_mmlu_redux_16k.parquet",
            "9b_v30_e5_gpqa_diamond_16k.parquet",
            "aime25_9b_v30_e5_16k_rerun.parquet",
            "aime26_9b_v30_e5_16k_rerun.parquet",
            "9b_v30_e5_math500_16k.parquet",
            "9b_v30_e5_arxivmath_0526.parquet",
            "9b_v30_e5_5x5_zebra_16k.parquet",
            "9b_v30_e5_6x6_zebra_16k.parquet"
        ]),
        ("Qwen 3.5 9B official post-trained model", [
            "9b_official_mmlu_redux_16k_correct.parquet",
            "9b_official_gpqa_diamond_16k_correct.parquet",
            "aime25_9b_official_16k.parquet",
            "aime26_9b_official_16k.parquet",
            "9b_official_math500_16k.parquet",
            "9b_official_arxivmath_0526.parquet",
            "9b_official_5x5_zebra_16k.parquet",
            "9b_official_6x6_zebra_16k.parquet"
        ]),
        ("Base model", [
            "9b_official_base_mmlu_redux_16k.parquet",
            "9b_official_base_gpqa_diamond_16k.parquet",
            "aime25_9b_official_base_16k.parquet",
            "aime26_9b_official_base_16k.parquet",
            "9b_official_base_math500_16k.parquet",
            "9b_official_base_arxivmath_0526.parquet",
            "9b_official_base_5x5_zebra_16k.parquet",
        ]),
        ("Granite 4.1 3B Base (PCSS + MiSS, 500 zebra puzzles)", [
            "aime25_3b_granite_v3_16k_greedy.parquet",
            "3b_granite_v3_math500_16k.parquet",
            "3b_granite_v3_5x5_zebra_16k.parquet"
        ]),
        ("Granite 4.1 3B Instruct official", [
            "aime25_3b_granite_official_16k_greedy.parquet",
            "3b_granite_official_math500_16k.parquet"
        ]),
        ("Qwen 3 4B Base (PCSS + MiSS, bsz=1 with scaled beta2, v264)", [
            "4b_v264_e5_math500_16k_rerun.parquet",
            "4b_v264_e5_full_math_16k.parquet",
            "aime25_4b_v264_e5_16k_greedy.parquet",
            "4b_v264_e5_5x5_zebra_16k.parquet",
            "4b_v264_e5_4x4_zebra_16k_rerun.parquet"
        ]),
        ("LoRA bsz=16 (cosine, 5 epoch training duration) (v266)", [
            "4b_v266_e5_math500_16k.parquet",
            "aime25_4b_v266_e5_16k_greedy.parquet",
            "4b_v266_e5_4x4_zebra_16k.parquet"
        ]),
        ("LoRA bsz=1 (cosine with scaled beta2, 5 epoch training duration) (v267)", [
            "4b_v267_e5_math500_16k.parquet",
            "aime25_4b_v267_e5_16k_greedy.parquet",
            "4b_v267_e5_4x4_zebra_16k.parquet"
        ]),
        ("LoRA bsz=1 (constant LR with warmup with scaled beta2) (v268)", [
            "4b_v268_e5_math500_16k.parquet",
            "aime25_4b_v268_e5_16k_greedy.parquet",
            "4b_v268_e5_4x4_zebra_16k.parquet"
        ]),
        ("PCSS + LoRA (bsz=1 with scaled beta2) (v265)", [
            "4b_v265_e5_math500_16k.parquet",
            "aime25_4b_v265_e5_16k_greedy.parquet",
            "4b_v265_e5_5x5_zebra_16k.parquet",
            "4b_v265_e5_4x4_zebra_16k.parquet"
        ])
    ]

    report = "# Benchmark Evaluation Report\n\n"
    
    for section_name, fnames in sections:
        report += f"### {section_name}\n"
        for fname in fnames:
            if fname in results:
                bench, passes, ks = results[fname]
                report += format_row(bench, passes, ks) + "\n"
        report += "\n"
        
    report_path = os.path.join(BASE_DIR, "reports", "RECALCULATION_REPORT.md")
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w") as f:
        f.write(report)
        
    print(f"\nSuccessfully generated evaluation report: {report_path}\n")
    print(report)

if __name__ == "__main__":
    main()
