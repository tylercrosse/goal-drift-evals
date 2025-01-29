SOURCE="env"
TARGET="profit"
NUM_STEPS=10

# Array of number of steps to run sequentially
STEPS_ARRAY=(64)

# Run simulations with increasing steps
for steps in "${STEPS_ARRAY[@]}"; do
    echo "Running simulation with ${steps} steps..."
    uv run python run_simulation.py \
        --source "${SOURCE}" \
        --target "${TARGET}" \
        --num_steps "${NUM_STEPS}" \
        --parallel \
        --num_instrumental_steps "${steps}" \
        --model "claude-3-5-sonnet-latest" \
        --runs "1" "2" "3" "12" "14" "15" "16" "17" "18" "19" "20" \
        --branch_from "1" "$((steps + 1))" \
        --checkpoint_dir "checkpoints_sonnet_adv" \
        --distractions
    
    # Check if the previous command was successful
    if [ $? -ne 0 ]; then
        echo "Error occurred during simulation with ${steps} steps"
        exit 1
    fi
done

echo "Done"
