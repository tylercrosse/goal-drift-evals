SOURCE="profit"
TARGET="env"
NUM_STEPS=30

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --model "claude-3-5-haiku-latest" \
    --run_range "4" "5" \
    --checkpoint_dir "checkpoints_haiku" \
    --distractions

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --model "claude-3-5-haiku-latest" \
    --run_range "6" "7" \
    --checkpoint_dir "checkpoints_haiku" \
    --distractions

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --model "claude-3-5-haiku-latest" \
    --run_range "8" "10" \
    --checkpoint_dir "checkpoints_haiku" \
    --distractions

echo "Done"