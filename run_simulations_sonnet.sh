SOURCE="profit"
TARGET="env"
NUM_STEPS=10

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --model "claude-3-5-sonnet-latest" \
    --runs "15" "16" \
    --checkpoint_dir "checkpoints_sonnet" \
    --resume

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --model "claude-3-5-sonnet-latest" \
    --runs "17" "18" \
    --checkpoint_dir "checkpoints_sonnet" \
    --resume

# echo "Running simulation..."
# python run_simulation.py \
#     --source "${SOURCE}" \
#     --target "${TARGET}" \
#     --num_steps "${NUM_STEPS}" \
#     --parallel \
#     --model "claude-3-5-sonnet-latest" \
#     --runs "15" "16" \
#     --checkpoint_dir "checkpoints_sonnet" \
#     --resume 

# echo "Running simulation..."
# python run_simulation.py \
#     --source "${SOURCE}" \
#     --target "${TARGET}" \
#     --num_steps "${NUM_STEPS}" \
#     --parallel \
#     --model "claude-3-5-sonnet-latest" \
#     --runs "17" "18" \
#     --checkpoint_dir "checkpoints_sonnet" \
#     --resume 

echo "Done"
