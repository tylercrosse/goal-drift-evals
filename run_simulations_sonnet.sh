SOURCE="env"
TARGET="profit"
NUM_STEPS=10

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --num_instrumental_steps "64" \
    --model "claude-3-5-sonnet-latest" \
    --run_range "6" "10" \
    --branch_from "1" "65" \
    --checkpoint_dir "checkpoints_sonnet"

echo "Done"
