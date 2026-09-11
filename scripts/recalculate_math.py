import pandas as pd
import argparse
import sys
import os
import math
from tqdm import tqdm

# Add raw_eval_snippets to path to import math500_check
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'raw_eval_snippets'))
from math500_check import check_math500

def pass_at_k(n, c, k):
    """
    Codex pass@k formula.
    n: total samples drawn for the problem
    c: number of correct samples
    k: k in pass@k
    """
    if n < k:
        return 0.0
    if n - c < k:
        return 1.0
    return 1.0 - math.comb(n - c, k) / math.comb(n, k)

def main():
    parser = argparse.ArgumentParser(description="Recalculate Math pass@k from parquet results.")
    parser.add_argument("parquet_file", type=str, help="Path to the eval run parquet file")
    parser.add_argument("--k", type=int, nargs="+", default=[1], help="Values of k for pass@k")
    args = parser.parse_args()

    df = pd.read_parquet(args.parquet_file)
    
    total_problems = len(df)
    
    # Store metrics per problem
    # pass_scores[k] will store the list of scores for that k
    pass_scores = {k: [] for k in args.k}
    
    # Find the correct column for ground truth
    gt_col = None
    for col in ['ground_truth', 'answer', 'solution']:
        if col in df.columns:
            gt_col = col
            break
    if not gt_col:
        raise ValueError(f"Could not find a ground truth column in {list(df.columns)}")
    
    print(f"Evaluating {args.parquet_file} ({total_problems} problems)...")
    
    for row in tqdm(df.itertuples(), total=total_problems):
        ground_truth = str(getattr(row, gt_col))
        samples = row.samples
        
        n = len(samples)
        if n == 0:
            for k in args.k:
                pass_scores[k].append(0.0)
            continue
            
        c = 0
        for sample in samples:
            # check_math500 can sometimes throw exceptions for weird LaTeX, let's catch it just in case
            try:
                if check_math500(ground_truth, sample):
                    c += 1
            except Exception as e:
                # If parsing fails, count as wrong
                pass
                
        # Calculate pass@k for this problem
        for k in args.k:
            pass_scores[k].append(pass_at_k(n, c, k))
            
    print(f"\n--- Results for {os.path.basename(args.parquet_file)} ---")
    for k in args.k:
        avg_pass_k = sum(pass_scores[k]) / len(pass_scores[k]) if pass_scores[k] else 0.0
        print(f"Pass@{k}: {avg_pass_k * 100:.2f}%")
        
if __name__ == "__main__":
    main()
