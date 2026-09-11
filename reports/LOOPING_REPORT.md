# Generation Looping Analysis Report

This report analyzes generation looping across evaluation runs using Liquid AI's `antidoom` repetition detection heuristic.

| Run Name                                      | Total Samples | Looping Samples | Looping %  |
|-----------------------------------------------|---------------|-----------------|------------|
| 9b_official_base_gpqa_diamond_16k_greedy      | 594           | 36              |     6.06% |
| 9b_official_gpqa_diamond_16k_greedy           | 594           | 31              |     5.22% |
| 9b_v30_e5_gpqa_diamond_16k_greedy             | 594           | 4               |     0.67% |
| 3b_granite_official_math500_16k               | 1500          | 15              |     1.00% |
| 3b_granite_v3_5x5_zebra_16k                   | 300           | 79              |    26.33% |
| 3b_granite_v3_math500_16k                     | 1500          | 145             |     9.67% |
| 4b_v264_e5_4x4_zebra_16k_rerun                | 300           | 59              |    19.67% |
| 4b_v264_e5_5x5_zebra_16k                      | 300           | 129             |    43.00% |
| 4b_v264_e5_full_math_16k                      | 5000          | 24              |     0.48% |
| 4b_v264_e5_math500_16k_rerun                  | 1500          | 44              |     2.93% |
| 4b_v265_e5_4x4_zebra_16k                      | 300           | 12              |     4.00% |
| 4b_v265_e5_5x5_zebra_16k                      | 300           | 37              |    12.33% |
| 4b_v265_e5_math500_16k                        | 1500          | 12              |     0.80% |
| 4b_v266_e5_4x4_zebra_16k                      | 300           | 143             |    47.67% |
| 4b_v266_e5_math500_16k                        | 500           | 23              |     4.60% |
| 4b_v267_e5_4x4_zebra_16k                      | 300           | 11              |     3.67% |
| 4b_v267_e5_math500_16k                        | 500           | 4               |     0.80% |
| 4b_v268_e5_4x4_zebra_16k                      | 300           | 65              |    21.67% |
| 4b_v268_e5_math500_16k                        | 500           | 8               |     1.60% |
| 9b_official_5x5_zebra_16k                     | 300           | 3               |     1.00% |
| 9b_official_6x6_zebra_16k                     | 300           | 8               |     2.67% |
| 9b_official_arxivmath_0526                    | 240           | 5               |     2.08% |
| 9b_official_base_5x5_zebra_16k                | 300           | 8               |     2.67% |
| 9b_official_base_arxivmath_0526               | 240           | 0               |     0.00% |
| 9b_official_base_gpqa_diamond_16k             | 594           | 0               |     0.00% |
| 9b_official_base_math500_16k                  | 1500          | 3               |     0.20% |
| 9b_official_base_mmlu_redux_16k               | 5330          | 4               |     0.08% |
| 9b_official_gpqa_diamond_16k_correct          | 594           | 5               |     0.84% |
| 9b_official_math500_16k                       | 1500          | 5               |     0.33% |
| 9b_official_mmlu_redux_16k_correct            | 5330          | 1               |     0.02% |
| 9b_v30_e5_5x5_zebra_16k                       | 600           | 2               |     0.33% |
| 9b_v30_e5_6x6_zebra_16k                       | 300           | 0               |     0.00% |
| 9b_v30_e5_arxivmath_0526                      | 240           | 0               |     0.00% |
| 9b_v30_e5_gpqa_diamond_16k                    | 594           | 2               |     0.34% |
| 9b_v30_e5_math500_16k                         | 1500          | 1               |     0.07% |
| 9b_v30_e5_mmlu_redux_16k                      | 5330          | 9               |     0.17% |
| aime25_3b_granite_official_16k_greedy         | 180           | 9               |     5.00% |
| aime25_3b_granite_v3_16k_greedy               | 180           | 50              |    27.78% |
| aime25_4b_v264_e5_16k_greedy                  | 180           | 29              |    16.11% |
| aime25_4b_v265_e5_16k_greedy                  | 180           | 21              |    11.67% |
| aime25_4b_v266_e5_16k_greedy                  | 180           | 46              |    25.56% |
| aime25_4b_v267_e5_16k_greedy                  | 180           | 12              |     6.67% |
| aime25_4b_v268_e5_16k_greedy                  | 180           | 21              |    11.67% |
| aime25_9b_official_16k                        | 180           | 3               |     1.67% |
| aime25_9b_official_base_16k                   | 180           | 0               |     0.00% |
| aime25_9b_v30_e5_16k_rerun                    | 300           | 0               |     0.00% |
| aime26_9b_official_16k                        | 180           | 7               |     3.89% |
| aime26_9b_official_base_16k                   | 180           | 0               |     0.00% |
| aime26_9b_v30_e5_16k_rerun                    | 300           | 1               |     0.33% |
