#!/bin/bash

# Base parameters
SOURCE="env"
TARGET="profit"
MODEL="claude-3-5-sonnet-latest"
NUM_STEPS=10

# Array of number of steps to run sequentially
STEPS_ARRAY=(64)
# Number of parallel runs
START_RUN=3
MIDDLE_RUN=3
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
        --model "${MODEL}" \
        --run_range "${START_RUN}" "${MIDDLE_RUN}" \
        --branch_from "1" "$((steps + 1))" \
        --checkpoint_dir "checkpoints_sonnet" \
        --distractions

    # Check if the previous command was successful
    if [ $? -ne 0 ]; then
        echo "Error occurred during simulation with ${steps} steps"
        exit 1
    fi
    
    echo "Completed simulation with ${steps} steps"
    echo "----------------------------------------"
done

echo "All simulations completed successfully!"
