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
    --run_range "4" "5" \
    --checkpoint_dir "checkpoints_sonnet_3" \
    --distractions \
    --use_soft_system_prompt

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --model "claude-3-5-sonnet-latest" \
    --run_range "6" "7" \
    --checkpoint_dir "checkpoints_sonnet_3" \
    --distractions \
    --use_soft_system_prompt

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --model "claude-3-5-sonnet-latest" \
    --run_range "8" "10" \
    --checkpoint_dir "checkpoints_sonnet_3" \
    --distractions \
    --use_soft_system_prompt

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --model "claude-3-5-sonnet-latest" \
    --run_range "15" "16" \
    --checkpoint_dir "checkpoints_sonnet_3" \
    --distractions \
    --use_soft_system_prompt

echo "Done"

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --model "claude-3-5-sonnet-latest" \
    --run_range "17" "18" \
    --checkpoint_dir "checkpoints_sonnet_3" \
    --distractions \
    --use_soft_system_prompt

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --model "claude-3-5-sonnet-latest" \
    --run_range "19" "20" \
    --checkpoint_dir "checkpoints_sonnet_3" \
    --distractions \
    --use_soft_system_prompt

echo "Done"