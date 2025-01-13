#!/bin/bash

# Base parameters
SOURCE="env"
TARGET="profit"
NUM_STEPS=10



echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --num_instrumental_steps "64" \
    --model "claude-3-5-sonnet-latest" \
    --run_range "4" "5" \
    --branch_from "1" "65" \
    --checkpoint_dir "results/env_profit_64_steps_sonnet_on_sonnet"
    
if [ $? -ne 0 ]; then
    echo "Error occurred during simulation"
fi


echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --num_instrumental_steps "64" \
    --model "claude-3-5-sonnet-latest" \
    --run_range "4" "5" \
    --branch_from "1" "65" \
    --checkpoint_dir "results/env_profit_64_steps_sonnet_on_sonnet_distractions" \
    --distractions
    
if [ $? -ne 0 ]; then
    echo "Error occurred during simulation"
fi


echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --num_instrumental_steps "64" \
    --model "claude-3-5-sonnet-latest" \
    --run_range "4" "5" \
    --branch_from "1" "65" \
    --checkpoint_dir "results/env_profit_64_steps_sonnet_on_sonnet_ood_distractions" \
    --ood \
    --distractions


echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --num_instrumental_steps "64" \
    --model "claude-3-5-sonnet-latest" \
    --run_range "4" "5" \
    --branch_from "1" "65" \
    --checkpoint_dir "results/env_profit_64_steps_sonnet_on_sonnet_baseline" \
    --baseline


echo "All simulations completed successfully!"