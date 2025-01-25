#!/bin/bash

# Base parameters
SOURCE="env"
TARGET="profit"
NUM_STEPS=10

# Array of number of steps to run sequentially
STEPS_ARRAY=(64)
# Number of parallel runs
START_RUN=1
END_RUN=5

# Run simulations with increasing steps
for steps in "${STEPS_ARRAY[@]}"; do
    echo "Running simulation with ${steps} steps..."
    python run_simulation.py \
        --source "${SOURCE}" \
        --target "${TARGET}" \
        --num_steps "${NUM_STEPS}" \
        --parallel \
        --num_instrumental_steps "${steps}" \
        --model "gpt-4o-mini" \
        --run_range "6" "10" \
        --branch_from "1" "$((steps + 1))" \
        --checkpoint_dir "checkpoints_4omini" \
        --distractions
    
    # Check if the previous command was successful
    if [ $? -ne 0 ]; then
        echo "Error occurred during simulation with ${steps} steps"
        exit 1
    fi
done

echo "All simulations completed successfully!"
