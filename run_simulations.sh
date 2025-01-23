#!/bin/bash

# Base parameters
SOURCE="env"
TARGET="profit"
NUM_STEPS=10

# Array of number of steps to run sequentially
STEPS_ARRAY=(4 8 16 32)
# Number of parallel runs
START_RUN=4
MIDDLE_LOW=9
MIDDLE_HIGH=15
END_RUN=20

# Run simulations with increasing steps
for steps in "${STEPS_ARRAY[@]}"; do
    echo "Running simulation with ${steps} steps..."
    python run_simulation.py \
        --source "${SOURCE}" \
        --target "${TARGET}" \
        --num_steps "${NUM_STEPS}" \
        --parallel \
        --num_instrumental_steps "${steps}" \
        --model "claude-3-5-sonnet-latest" \
        --run_range "4" "6" \
        --branch_from "1" "$((steps + 1))" \
        --checkpoint_dir "checkpoints_sonnet" \
        --distractions \
        --ood
    
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
    #     --run_range "$((MIDDLE_LOW + 1))" "${MIDDLE_HIGH}" \
    #     --branch_from "1" "$((steps + 1))" \
    #     --checkpoint_dir "checkpoints_gpt" \
    #     --distractions \
    #     --ood

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
    #     --model "gpt-4o-mini" \
    #     --run_range "$((MIDDLE_HIGH + 1))" "${END_RUN}" \
    #     --branch_from "1" "$((steps + 1))" \
    #     --checkpoint_dir "checkpoints_gpt" \
    #     --distractions \
    #     --ood

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
    #     --run_range "${START_RUN}" "${MIDDLE_LOW}" \
    #     --branch_from "1" "$((steps + 1))" \
    #     --checkpoint_dir "checkpoints_haiku" \
    #     --distractions \
    #     --ood

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
    #     --runs "$((MIDDLE_LOW + 1))" "$((MIDDLE_HIGH - 1))" \
    #     --branch_from "1" "$((steps + 1))" \
    #     --checkpoint_dir "checkpoints_haiku" \
    #     --distractions \
    #     --ood

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
    #     --run_range "$((MIDDLE_HIGH + 1))" "${END_RUN}" \
    #     --branch_from "1" "$((steps + 1))" \
    #     --checkpoint_dir "checkpoints_haiku" \
    #     --distractions \
    #     --ood

    # if [ $? -ne 0 ]; then
    #     echo "Error occurred during simulation with ${steps} steps"
    #     exit 1
    # fi
    
    # echo "Completed simulation with ${steps} steps"
    # echo "----------------------------------------"
done

echo "All simulations completed successfully!"
