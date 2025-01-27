SOURCE="profit"
TARGET="env"
NUM_STEPS=30

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --model "gpt-4o-mini" \
    --run_range "16" "20" \
    --checkpoint_dir "checkpoints_4omini" \
    --distractions \
    --use_soft_system_prompt

echo "Done"