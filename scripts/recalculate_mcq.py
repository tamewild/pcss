import pandas as pd
import argparse
import os
import math
import re
from tqdm import tqdm

def pass_at_k(n, c, k):
    if n < k:
        return 0.0
    if n - c < k:
        return 1.0
    return 1.0 - math.comb(n - c, k) / math.comb(n, k)

def last_box(s):
    tag = "\\boxed{"
    tag_start = s.rfind(tag)
    if tag_start == -1:
        return ""
    
    content = s[tag_start + len(tag):]
    depth = 1
    for i, char in enumerate(content):
        if char == '{':
            depth += 1
        elif char == '}':
            depth -= 1
            if depth == 0:
                return content[:i].strip()
                
    return content.strip()

def check_mcq_answer(response, ground_truth):
    ans = last_box(response)
    if not ans:
        return False
        
    ans_upper = ans.strip().upper()
    gt_upper = ground_truth.upper()
    
    if ans_upper == gt_upper:
        return True
        
    if f"{{{gt_upper}}}" in ans_upper:
        return True
        
    if f"{gt_upper})" in ans_upper:
        return True
        
    return False

def main():
    parser = argparse.ArgumentParser(description="Recalculate MCQ pass@k from parquet results.")
    parser.add_argument("parquet_file", type=str, help="Path to the eval run parquet file")
    parser.add_argument("--k", type=int, nargs="+", default=[1], help="Values of k for pass@k")
    args = parser.parse_args()

    df = pd.read_parquet(args.parquet_file)
    total_problems = len(df)
    
    pass_scores = {k: [] for k in args.k}
    
    gt_col = None
    for col in ['ground_truth', 'answer']:
        if col in df.columns:
            gt_col = col
            break
    if not gt_col:
        raise ValueError(f"Could not find a ground truth column in {list(df.columns)}")
    
    print(f"Evaluating {args.parquet_file} ({total_problems} problems)...")
    
    for row in tqdm(df.itertuples(), total=total_problems):
        # handle dynamic column names (some use question, some use problem)
        problem_col = "problem" if "problem" in df.columns else "question"
        gt_col = "ground_truth" if "ground_truth" in df.columns else "answer"
        
        problem_text = getattr(row, problem_col, None)
        ground_truth = str(getattr(row, gt_col)).strip().upper()
        samples = row.samples
        
        n = len(samples)
        if n == 0:
            for k in args.k:
                pass_scores[k].append(0.0)
            continue
            
        c = 0
        for sample in samples:
            if check_mcq_answer(sample, ground_truth):
                c += 1
                
        for k in args.k:
            pass_scores[k].append(pass_at_k(n, c, k))
            
    print(f"\n--- Results for {os.path.basename(args.parquet_file)} ---")
    for k in args.k:
        avg_pass_k = sum(pass_scores[k]) / len(pass_scores[k]) if pass_scores[k] else 0.0
        print(f"Pass@{k}: {avg_pass_k * 100:.2f}%")
        
if __name__ == "__main__":
    main()
