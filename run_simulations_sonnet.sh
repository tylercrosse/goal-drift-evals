SOURCE="profit"
TARGET="env"
NUM_STEPS=30

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --model "claude-3-5-sonnet-latest" \
    --run_range "5" "6" \
    --checkpoint_dir "checkpoints_sonnet" \
    --distractions

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --model "claude-3-5-sonnet-latest" \
    --run_range "7" "8" \
    --checkpoint_dir "checkpoints_sonnet" \
    --distractions

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --model "claude-3-5-sonnet-latest" \
    --run_range "9" "10" \
    --checkpoint_dir "checkpoints_sonnet" \
    --distractions

echo "Done"