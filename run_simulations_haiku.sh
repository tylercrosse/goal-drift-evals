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
    --model "claude-3-5-haiku-latest" \
    --run_range "6" "10" \
    --branch_from "1" "33" \
    --checkpoint_dir "checkpoints_haiku" \
    --distractions

echo "Done"
