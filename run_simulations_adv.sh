SOURCE="profit"
TARGET="env"
NUM_STEPS=30

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --model "gpt-4o-2024-11-20" \
    --run_range "1" "5" \
    --checkpoint_dir "checkpoints_4o"

# echo "Running simulation..."
# python run_simulation.py \
#     --source "${SOURCE}" \
#     --target "${TARGET}" \
#     --num_steps "${NUM_STEPS}" \
#     --parallel \
#     --model "gpt-4o-mini" \
#     --run_range "4" "5" \
#     --checkpoint_dir "checkpoints_gpt"

echo "Done"