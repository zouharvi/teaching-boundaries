for SEED in $(seq 0 2); do
    python3 analysis/scripts/03-generate_dataset.py --model tree_simple --tags 3 --seed ${SEED}
    python3 analysis/scripts/03-generate_dataset.py --model random --tags 3 --seed ${SEED}
done