#!/usr/bin/bash


python3 analysis/scripts/10-measure_user_accuracy.py "computed/collected/ailr_random_tdomain_8n15_s0.jsonl"
python3 analysis/scripts/10-measure_user_accuracy.py "computed/collected/ailr_random_tlength_answer_8n15_s1.jsonl"

python3 analysis/scripts/10-measure_user_accuracy.py "computed/collected/ailr_linear_simple_t2_10n15_s0.jsonl"
python3 analysis/scripts/10-measure_user_accuracy.py "computed/collected/ailr_random_t2_10n15_s0.jsonl"