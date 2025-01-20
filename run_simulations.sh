#!/bin/bash

# Base parameters
SOURCE="env"
TARGET="profit"
NUM_STEPS=10

# Array of number of steps to run sequentially
STEPS_ARRAY=(2 4 8 16 32)
# Number of parallel runs
START_RUN=16
MIDDLE_RUN=20
END_RUN=15

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
        --run_range "${START_RUN}" "${MIDDLE_RUN}" \
        --branch_from "1" "$((steps + 1))" \
        --checkpoint_dir "checkpoints_gpt"

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
    #     --model "gpt-4o-mini" \
    #     --run_range "$((MIDDLE_RUN + 1))" "${END_RUN}" \
    #     --branch_from "1" "$((steps + 1))" \
    #     --checkpoint_dir "checkpoints_gpt"

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
    #     --run_range "${START_RUN}" "${MIDDLE_RUN}" \
    #     --branch_from "1" "$((steps + 1))" \
    #     --checkpoint_dir "checkpoints_haiku" \
    #     --distractions

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
    #     --run_range "$((MIDDLE_RUN + 1))" "${END_RUN}" \
    #     --branch_from "1" "$((steps + 1))" \
    #     --checkpoint_dir "checkpoints_haiku" \
    #     --distractions

    # if [ $? -ne 0 ]; then
    #     echo "Error occurred during simulation with ${steps} steps"
    #     exit 1
    # fi
    
    # echo "Completed simulation with ${steps} steps"
    # echo "----------------------------------------"
done

echo "All simulations completed successfully!"
