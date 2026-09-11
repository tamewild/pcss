import pandas as pd
import argparse
import sys
import os
import math
import re
from tqdm import tqdm

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'raw_eval_snippets'))
import zebra_puzzle_check

original_parse_answer = zebra_puzzle_check.parse_answer

def parse_markdown_table(text, house_amount):
    lines = text.split('\n')
    tables = []
    current_table = []
    for l in lines:
        if l.strip().startswith('|'):
            current_table.append(l.strip())
        else:
            if current_table:
                tables.append(current_table)
                current_table = []
    if current_table:
        tables.append(current_table)
        
    if not tables:
        return None
        
    last_table = tables[-1]
    table_lines = [l for l in last_table if not re.match(r'^[|\s:\-]+$', l)]
    if len(table_lines) <= 1:
        return None
        
    houses = [[] for _ in range(house_amount)]
    for line in table_lines[1:]:
        raw_items = [x.strip() for x in line.split('|')[1:-1]]
        if not raw_items: continue
        items = [re.sub(r"[*_`]", "", x).strip() for x in raw_items]
        m = re.match(r"^(?:house\s*|#\s*)?(\d+)", items[0], re.IGNORECASE)
        if m:
            house_idx = int(m.group(1)) - 1
            if 0 <= house_idx < house_amount:
                houses[house_idx].extend(items[1:])
        else:
            # Columns are houses
            if len(items) >= house_amount + 1:
                for i in range(house_amount):
                    houses[i].append(items[i+1])
            elif len(items) == house_amount:
                for i in range(house_amount):
                    houses[i].append(items[i])
    return houses

def my_parse_answer(str_val, house_amount, strict_latex=False):
    if strict_latex:
        if "\\boxed{" not in str_val:
            return None
        return original_parse_answer(str_val, house_amount)

    if "\\boxed{" in str_val:
        ans = original_parse_answer(str_val, house_amount)
        if ans is not None:
            return ans

    # Try markdown first if it has table formatting
    if '|' in str_val and '---' in str_val:
        houses = parse_markdown_table(str_val, house_amount)
        if houses and any(len(h) > 0 for h in houses):
            return houses
    # Fallback to latex
    return original_parse_answer(str_val, house_amount)

def pass_at_k(n, c, k):
    if n < k:
        return 0.0
    if n - c < k:
        return 1.0
    return 1.0 - math.comb(n - c, k) / math.comb(n, k)

def main():
    parser = argparse.ArgumentParser(description="Recalculate Zebra pass@k from parquet results.")
    parser.add_argument("parquet_file", type=str, help="Path to the eval run parquet file")
    parser.add_argument("--k", type=int, nargs="+", default=[1], help="Values of k for pass@k")
    parser.add_argument("--strict-latex", action="store_true", help="Only parse LaTeX grids containing \\boxed{}")
    args = parser.parse_args()

    zebra_puzzle_check.parse_answer = lambda s, h: my_parse_answer(s, h, strict_latex=args.strict_latex)

    df = pd.read_parquet(args.parquet_file)
    total_problems = len(df)
    
    pass_scores = {k: [] for k in args.k}
    
    print(f"Evaluating {args.parquet_file} ({total_problems} problems)...")
    
    for row in tqdm(df.itertuples(), total=total_problems):
        solution_json = row.solution
        solution_houses = zebra_puzzle_check.parse_solution(solution_json)
        samples = row.samples
        
        n = len(samples)
        if n == 0:
            for k in args.k:
                pass_scores[k].append(0.0)
            continue
            
        c = 0
        for sample in samples:
            if zebra_puzzle_check.compare_answer(sample, solution_houses):
                c += 1
                
        for k in args.k:
            pass_scores[k].append(pass_at_k(n, c, k))
            
    print(f"\n--- Results for {os.path.basename(args.parquet_file)} ---")
    for k in args.k:
        avg_pass_k = sum(pass_scores[k]) / len(pass_scores[k]) if pass_scores[k] else 0.0
        print(f"Pass@{k}: {avg_pass_k * 100:.2f}%")
        
if __name__ == "__main__":
    main()
