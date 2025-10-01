SOURCE="env"
TARGET="profit"
NUM_STEPS=10
CHECKPOINT_DIR="checkpoints_sonnet"

# Array of number of steps to run sequentially
STEPS_ARRAY=(2 4 8 16 32)
RUNS="1"

# Run simulations with increasing steps
for steps in "${STEPS_ARRAY[@]}"; do
    echo "Running ${MODEL} simulation with ${steps} instrumental steps (runs ${RUNS})..."
    python run_simulation.py \
        --model "gpt-5-mini-2025-08-07" \
        --runs "${RUNS}" \
        --source "${SOURCE}" \
        --target "${TARGET}" \
        --num_steps "${NUM_STEPS}" \
        --num_instrumental_steps "${steps}" \
        --branch_from "1" "$((steps + 1))" \
        --checkpoint_dir "checkpoints_5mini" \
        --distractions
        # --easy_setup \
        # --easy_name "5mini" \

    # Check if the previous command was successful
    if [ $? -ne 0 ]; then
        echo "❌ Error occurred during simulation with ${steps} instrumental steps (runs ${RUNS})"
        exit 1
    fi
done

echo "Done"
