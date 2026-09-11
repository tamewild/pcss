import pandas as pd
from transformers import AutoTokenizer
import numpy as np
import os
from tqdm import tqdm

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
    tokenizer = AutoTokenizer.from_pretrained("unsloth/Qwen3.5-9B")
    
    eval_dir = os.path.join(BASE_DIR, "eval_runs", "standard")
    files = {
        "Qwen 3.5 9B Official Post-Trained (5x5 Zebra)": os.path.join(eval_dir, "9b_official_5x5_zebra_16k.parquet"),
        "Qwen 3.5 9B Base PCSS Fine-Tuned (5x5 Zebra)": os.path.join(eval_dir, "9b_v30_e5_5x5_zebra_16k.parquet"),
        "Qwen 3.5 9B Official Post-Trained (6x6 Zebra)": os.path.join(eval_dir, "9b_official_6x6_zebra_16k.parquet"),
        "Qwen 3.5 9B Base PCSS Fine-Tuned (6x6 Zebra)": os.path.join(eval_dir, "9b_v30_e5_6x6_zebra_16k.parquet")
    }
    
    report_lines = [
        "# Zebra Logic Puzzle Generation Lengths",
        "",
        "| Model | Median Tokens | Average Tokens | Max Tokens |",
        "|---|---|---|---|"
    ]
    
    print("Token Analysis for Zebra completions:")
    for label, filepath in files.items():
        if not os.path.exists(filepath):
            print(f"{label} file not found: {filepath}")
            continue
            
        df = pd.read_parquet(filepath)
        token_lengths = []
        
        for row in tqdm(df.itertuples(), total=len(df), desc=label):
            samples = row.samples if hasattr(row, 'samples') else row.generated_text
            if not isinstance(samples, (list, np.ndarray)):
                samples = [samples]
            for sample in samples:
                tokens = tokenizer.encode(sample, add_special_tokens=False)
                token_lengths.append(len(tokens))
                
        if token_lengths:
            avg_len = np.mean(token_lengths)
            median_len = np.median(token_lengths)
            max_len = np.max(token_lengths)
            print(f"\n{label}:")
            print(f"  Average tokens: {avg_len:.2f}")
            print(f"  Median tokens:  {median_len:.2f}")
            print(f"  Max tokens:     {max_len}")
            
            report_lines.append(f"| {label} | {median_len:,.1f} | {avg_len:,.1f} | {max_len:,} |")
        else:
            print(f"\n{label}: No samples found.")

    report_content = "\n".join(report_lines)
    report_path = os.path.join(BASE_DIR, "reports", "ZEBRA_LENGTH_REPORT.md")
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w") as f:
        f.write(report_content)
    
    print(f"\nReport saved to: {report_path}")

if __name__ == "__main__":
    main()
