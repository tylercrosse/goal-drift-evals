SOURCE="env"
TARGET="profit"
NUM_STEPS=10

# echo "Running simulation..."
# python run_simulation.py \
#     --source "${SOURCE}" \
#     --target "${TARGET}" \
#     --num_steps "${NUM_STEPS}" \
#     --parallel \
#     --model "claude-3-5-haiku-latest" \
#     --run_range "9" "10" \
#     --checkpoint_dir "checkpoints_haiku" \
#     --distractions

# echo "Running simulation..."
# python run_simulation.py \
#     --source "${SOURCE}" \
#     --target "${TARGET}" \
#     --num_steps "${NUM_STEPS}" \
#     --parallel \
#     --model "claude-3-5-haiku-latest" \
#     --run_range "11" "13" \
#     --checkpoint_dir "checkpoints_haiku" \
#     --distractions

# echo "Running simulation..."
# python run_simulation.py \
#     --source "${SOURCE}" \
#     --target "${TARGET}" \
#     --num_steps "${NUM_STEPS}" \
#     --parallel \
#     --model "claude-3-5-haiku-latest" \
#     --run_range "14" "16" \
#     --checkpoint_dir "checkpoints_haiku" \
#     --distractions

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --model "claude-3-5-haiku-latest" \
    --runs "15" "17" "18" "19" "20" \
    --checkpoint_dir "checkpoints_haiku" \
    --distractions \
    --resume

# echo "Running simulation..."
# python run_simulation.py \
#     --source "${SOURCE}" \
#     --target "${TARGET}" \
#     --num_steps "${NUM_STEPS}" \
#     --parallel \
#     --model "claude-3-5-haiku-latest" \
#     --run_range "19" "20" \
#     --checkpoint_dir "checkpoints_haiku" \
#     --distractions

echo "Done"