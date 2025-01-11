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
    --num_instrumental_steps "16" \
    --model "claude-3-5-haiku-latest" \
    --run_range "4" "5" \
    --branch_from "1" "17" \
    --checkpoint_dir "results/env_profit_16_steps_haiku_on_haiku"
    
if [ $? -ne 0 ]; then
    echo "Error occurred during simulation"
fi


echo "All simulations completed successfully!"