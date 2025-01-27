SOURCE="env"
TARGET="profit"
NUM_STEPS=10

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --model "claude-3-5-haiku-latest" \
    --run_range "10" "11" \
    --checkpoint_dir "checkpoints_haiku_1" \
    --distractions \
    --use_soft_system_prompt \
    --resume

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --model "claude-3-5-haiku-latest" \
    --run_range "12" "13" \
    --checkpoint_dir "checkpoints_haiku_1" \
    --distractions \
    --use_soft_system_prompt \
    --resume

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --model "claude-3-5-haiku-latest" \
    --run_range "14" "16" \
    --checkpoint_dir "checkpoints_haiku_1" \
    --distractions \
    --use_soft_system_prompt \
    --resume

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --model "claude-3-5-haiku-latest" \
    --run_range "17" "18" \
    --checkpoint_dir "checkpoints_haiku_1" \
    --distractions \
    --use_soft_system_prompt \
    --resume

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --model "claude-3-5-haiku-latest" \
    --run_range "19" "20" \
    --checkpoint_dir "checkpoints_haiku_1" \
    --distractions \
    --use_soft_system_prompt \
    --resume

echo "Done"