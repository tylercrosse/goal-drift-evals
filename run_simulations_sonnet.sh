SOURCE="env"
TARGET="profit"
NUM_STEPS=10

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --num_instrumental_steps "32" \
    --model "anthropic/claude-3-5-sonnet" \
    --runs "16" \
    # --branch_from "1" "33" \
    # --checkpoint_dir "checkpoints_sonnet"

echo "Done"
