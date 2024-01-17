for SEED in $(seq 0 2); do
    python3 analysis/scripts/03-generate_dataset.py --ai-model ailr --size-train 6 --size-test 19 --model tree_simple --tags 3 --seed ${SEED}
    python3 analysis/scripts/03-generate_dataset.py --ai-model ailr --size-train 6 --size-test 19 --model anti_tree_simple --tags 3 --seed ${SEED}
    python3 analysis/scripts/03-generate_dataset.py --ai-model ailr --size-train 6 --size-test 19 --model random --tags 3 --seed ${SEED}
done