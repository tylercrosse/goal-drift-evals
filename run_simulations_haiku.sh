#!/bin/bash

# Base parameters
SOURCE="env"
TARGET="profit"
NUM_STEPS=10

# Array of number of steps to run sequentially
STEPS_ARRAY=(8)
# Number of parallel runs
START_RUN=4
MIDDLE_LOW=9
MIDDLE_HIGH=15
END_RUN=20

# Run simulations with increasing steps
for steps in "${STEPS_ARRAY[@]}"; do
    # echo "Running simulation with ${steps} steps..."
    # python run_simulation.py \
    #     --source "${SOURCE}" \
    #     --target "${TARGET}" \
    #     --num_steps "${NUM_STEPS}" \
    #     --parallel \
    #     --num_instrumental_steps "${steps}" \
    #     --model "claude-3-5-haiku-latest" \
    #     --run_range "4" "5" \
    #     --branch_from "1" "$((steps + 1))" \
    #     --checkpoint_dir "checkpoints_haiku" \
    #     --baseline
    
    # # Check if the previous command was successful
    # if [ $? -ne 0 ]; then
    #     echo "Error occurred during simulation with ${steps} steps"
    #     exit 1
    # fi

    echo "Running simulation with ${steps} steps..."
    python run_simulation.py \
        --source "${SOURCE}" \
        --target "${TARGET}" \
        --num_steps "${NUM_STEPS}" \
        --parallel \
        --num_instrumental_steps "${steps}" \
        --model "claude-3-5-haiku-latest" \
        --run_range "6" "6" \
        --branch_from "1" "$((steps + 1))" \
        --checkpoint_dir "checkpoints_haiku" \
        --baseline
    
    # Check if the previous command was successful
    if [ $? -ne 0 ]; then
        echo "Error occurred during simulation with ${steps} steps"
        exit 1
    fi

    # echo "Running simulation with ${steps} steps..."
    # python run_simulation.py \
    #     --source "${SOURCE}" \
    #     --target "${TARGET}" \
    #     --num_steps "${NUM_STEPS}" \
    #     --parallel \
    #     --num_instrumental_steps "${steps}" \
    #     --model "claude-3-5-haiku-latest" \
    #     --run_range "8" "10" \
    #     --branch_from "1" "$((steps + 1))" \
    #     --checkpoint_dir "checkpoints_haiku" \
    #     --baseline
    
    # # Check if the previous command was successful
    # if [ $? -ne 0 ]; then
    #     echo "Error occurred during simulation with ${steps} steps"
    #     exit 1
    # fi

    #     echo "Running simulation with ${steps} steps..."
    # python run_simulation.py \
    #     --source "${SOURCE}" \
    #     --target "${TARGET}" \
    #     --num_steps "${NUM_STEPS}" \
    #     --parallel \
    #     --num_instrumental_steps "${steps}" \
    #     --model "claude-3-5-haiku-latest" \
    #     --run_range "7" "8" \
    #     --branch_from "1" "$((steps + 1))" \
    #     --checkpoint_dir "checkpoints_haiku"
    
    # # Check if the previous command was successful
    # if [ $? -ne 0 ]; then
    #     echo "Error occurred during simulation with ${steps} steps"
    #     exit 1
    # fi

    # echo "Running simulation with ${steps} steps..."
    # python run_simulation.py \
    #     --source "${SOURCE}" \
    #     --target "${TARGET}" \
    #     --num_steps "${NUM_STEPS}" \
    #     --parallel \
    #     --num_instrumental_steps "${steps}" \
    #     --model "claude-3-5-haiku-latest" \
    #     --run_range "9" "10" \
    #     --branch_from "1" "$((steps + 1))" \
    #     --checkpoint_dir "checkpoints_haiku" \
    #     --distractions
    
    # # Check if the previous command was successful
    # if [ $? -ne 0 ]; then
    #     echo "Error occurred during simulation with ${steps} steps"
    #     exit 1
    # fi
done

echo "All simulations completed successfully!"
