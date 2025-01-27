SOURCE="env"
TARGET="profit"
NUM_STEPS=10

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --model "claude-3-5-sonnet-latest" \
    --run_range "8" "9" \
    --checkpoint_dir "checkpoints_sonnet" \
    --distractions \
    --use_soft_system_prompt \
    --resume

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --model "claude-3-5-sonnet-latest" \
    --run_range "10" "11" \
    --checkpoint_dir "checkpoints_sonnet" \
    --distractions \
    --use_soft_system_prompt \
    --resume

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --model "claude-3-5-sonnet-latest" \
    --run_range "12" "13" \
    --checkpoint_dir "checkpoints_sonnet" \
    --distractions \
    --use_soft_system_prompt \
    --resume

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --model "claude-3-5-sonnet-latest" \
    --run_range "14" "15" \
    --checkpoint_dir "checkpoints_sonnet" \
    --distractions \
    --use_soft_system_prompt \
    --resume

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --model "claude-3-5-sonnet-latest" \
    --run_range "16" "18" \
    --checkpoint_dir "checkpoints_sonnet" \
    --distractions \
    --use_soft_system_prompt \
    --resume

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --model "claude-3-5-sonnet-latest" \
    --run_range "19" "20" \
    --checkpoint_dir "checkpoints_sonnet" \
    --distractions \
    --use_soft_system_prompt \
    --resume

# echo "Running simulation..."
# python run_simulation.py \
#     --source "${SOURCE}" \
#     --target "${TARGET}" \
#     --num_steps "${NUM_STEPS}" \
#     --parallel \
#     --model "claude-3-5-sonnet-latest" \
#     --run_range "17" "18" \
#     --checkpoint_dir "checkpoints_sonnet" \
#     --distractions

# echo "Running simulation..."
# python run_simulation.py \
#     --source "${SOURCE}" \
#     --target "${TARGET}" \
#     --num_steps "${NUM_STEPS}" \
#     --parallel \
#     --model "claude-3-5-sonnet-latest" \
#     --run_range "19" "20" \
#     --checkpoint_dir "checkpoints_sonnet" \
#     --distractions

echo "Done"