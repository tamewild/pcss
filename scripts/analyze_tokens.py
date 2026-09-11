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
        "Base Model": os.path.join(eval_dir, "9b_official_base_math500_16k.parquet"),
        "Official Instruct": os.path.join(eval_dir, "9b_official_math500_16k.parquet"),
        "v30 (PCSS Fine-Tuned)": os.path.join(eval_dir, "9b_v30_e5_math500_16k.parquet")
    }
    
    print("Token Analysis for MATH-500 completions:")
    for label, filepath in files.items():
        if not os.path.exists(filepath):
            print(f"{label} file not found: {filepath}")
            continue
            
        df = pd.read_parquet(filepath)
        token_lengths = []
        
        for row in tqdm(df.itertuples(), total=len(df), desc=label):
            samples = row.samples
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
        else:
            print(f"\n{label}: No samples found.")

if __name__ == "__main__":
    main()
