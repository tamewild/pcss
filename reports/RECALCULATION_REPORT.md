# Benchmark Evaluation Report

### Qwen 3.5 9B Base (PCSS + MiSS, v30)
- MMLU Redux (16k, avg 1): 90.45%
- GPQA Diamond (16k, avg 3): 71.04%
- AIME25 (16k, avg 10): 60.67%
    - Pass@3: 75.58%
- AIME26 (16k, avg 10): 64.33%
    - Pass@3: 75.50%
- MATH-500 (16k, avg 3): 96.60%
- ArXivMath 05/26 (16k, avg 6): 22.92%
    - Pass@3: 34.88%
- 5x5 Zebra (16k, avg 6): 80.50%
    - Pass@3: 97.05%
- 6x6 Zebra (16k, avg 3): 26.00%

### Qwen 3.5 9B official post-trained model
- MMLU Redux (16k, avg 1): 90.15%
- GPQA Diamond (16k, avg 3): 79.63%
- AIME25 (16k, avg 6): 60.56%
    - Pass@3: 77.50%
- AIME26 (16k, avg 6): 69.44%
    - Pass@3: 84.67%
- MATH-500 (16k, avg 3): 97.40%
- ArXivMath 05/26 (16k, avg 6): 24.17%
    - Pass@3: 31.87%
- 5x5 Zebra (16k, avg 3): 48.00%
- 6x6 Zebra (16k, avg 3): 5.00%

### Base model
- MMLU Redux (16k, avg 1): 89.32%
- GPQA Diamond (16k, avg 3): 61.11%
- AIME25 (16k, avg 6): 49.44%
    - Pass@3: 61.83%
- AIME26 (16k, avg 6): 50.00%
    - Pass@3: 65.50%
- MATH-500 (16k, avg 3): 93.53%
- ArXivMath 05/26 (16k, avg 6): 5.42%
    - Pass@3: 12.00%
- 5x5 Zebra (16k, avg 3): 17.00%

### Granite 4.1 3B Base (PCSS + MiSS, 500 zebra puzzles)
- AIME25 (16k, avg 6): 19.44%
- MATH-500 (16k, avg 3): 77.73%
- 5x5 Zebra (16k, avg 3): 20.00%

### Granite 4.1 3B Instruct official
- AIME25 (16k, avg 6): 6.67%
- MATH-500 (16k, avg 3): 66.60%

### Qwen 3 4B Base (PCSS + MiSS, bsz=1 with scaled beta2, v264)
- MATH-500 (16k, avg 3): 84.60%
- MATH (full 5,000, 16k): 85.26%
- AIME25 (16k, avg 6): 21.67%
- 5x5 Zebra (16k, avg 3): 4.33%
- 4x4 Zebra (16k, avg 3): 31.67%

### LoRA bsz=16 (cosine, 5 epoch training duration) (v266)
- MATH-500 (16k, avg 1): 79.40%
- AIME25 (16k, avg 6): 16.67%
- 4x4 Zebra (16k, avg 3): 23.67%

### LoRA bsz=1 (cosine with scaled beta2, 5 epoch training duration) (v267)
- MATH-500 (16k, avg 1): 81.60%
- AIME25 (16k, avg 6): 15.00%
- 4x4 Zebra (16k, avg 3): 59.67%

### LoRA bsz=1 (constant LR with warmup with scaled beta2) (v268)
- MATH-500 (16k, avg 1): 79.80%
- AIME25 (16k, avg 6): 13.33%
- 4x4 Zebra (16k, avg 3): 37.67%

### PCSS + LoRA (bsz=1 with scaled beta2) (v265)
- MATH-500 (16k, avg 3): 83.07%
- AIME25 (16k, avg 6): 16.67%
- 5x5 Zebra (16k, avg 3): 11.00%
- 4x4 Zebra (16k, avg 3): 59.00%

