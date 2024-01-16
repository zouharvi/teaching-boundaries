#!/bin/bash

mkdir -p computed/trees
python3 teaching-boundaries/scripts/01-print_random_decision_tree.py --seed 0 --nodes 5
python3 teaching-boundaries/scripts/01-print_random_decision_tree.py --seed 1 --nodes 5
python3 teaching-boundaries/scripts/01-print_random_decision_tree.py --seed 0 --nodes 3
python3 teaching-boundaries/scripts/01-print_random_decision_tree.py --seed 0 --nodes 8

cat computed/trees/random_*.out 