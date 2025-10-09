SOURCE="env"
TARGET="profit"
NUM_STEPS=10

# Array of number of steps to run sequentially
STEPS_ARRAY=(2 4 8 16 32)
RUNS="1"

# Run simulations with increasing steps
for steps in "${STEPS_ARRAY[@]}"; do
    echo "Running ${MODEL} simulation with ${steps} instrumental steps (runs ${RUNS})..."
    python run_simulation.py \
        --model "qwen/qwen3-next-80b-a3b-instruct" \
        --runs "${RUNS}" \
        --source "${SOURCE}" \
        --target "${TARGET}" \
        --num_steps "${NUM_STEPS}" \
        --num_instrumental_steps "${steps}" \
        --distractions
        # --branch_from "1" "$((steps + 1))" \
        # --checkpoint_dir "checkpoints_qwen" \
        # --easy_setup \
        # --easy_name "qwen" \

    # Check if the previous command was successful
    if [ $? -ne 0 ]; then
        echo "❌ Error occurred during simulation with ${steps} instrumental steps (runs ${RUNS})"
        exit 1
    fi
done

echo "Done"
