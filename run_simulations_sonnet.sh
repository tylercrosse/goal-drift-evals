SOURCE="env"
TARGET="profit"
NUM_STEPS=10

# Array of number of steps to run sequentially

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --num_instrumental_steps "32" \
    --model "claude-3-5-sonnet-latest" \
    --runs "2" \
    --branch_from "1" "33" \
    --checkpoint_dir "checkpoints_sonnet_adv" \
    --distractions

echo "Done"
