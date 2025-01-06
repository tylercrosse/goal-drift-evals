#!/bin/bash

# Base parameters
SOURCE="env"
TARGET="profit"

# echo "Running first simulation..."

# python run_simulation.py \
#     --source "${SOURCE}" \
#     --target "${TARGET}" \
#     --num_steps "10" \
#     --parallel \
#     --num_instrumental_steps "32" \
#     --model "claude-3-5-haiku-latest" \
#     --run_range "4" "5" \
#     --branch_from "1" "33" \
#     --checkpoint_dir "checkpoints_haiku" \
#     --distractions \
#     --ood

# if [ $? -ne 0 ]; then
#     echo "Error occurred during simulation"
# fi

echo "Running second simulation..."

python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "10" \
    --parallel \
    --num_instrumental_steps "64" \
    --model "claude-3-5-sonnet-latest" \
    --run_range "1" "3" \
    --branch_from "1" "65" \
    --checkpoint_dir "checkpoints_sonnet" \
    --distractions \
    --ood

if [ $? -ne 0 ]; then
    echo "Error occurred during simulation"
fi

echo "All simulations completed successfully!"
