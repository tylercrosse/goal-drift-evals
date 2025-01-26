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
    --run_range "10" "12" \
    --checkpoint_dir "checkpoints_haiku_3" \
    --distractions \
    --use_soft_system_prompt

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --model "claude-3-5-haiku-latest" \
    --run_range "13" "14" \
    --checkpoint_dir "checkpoints_haiku_3" \
    --distractions \
    --use_soft_system_prompt

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --model "claude-3-5-haiku-latest" \
    --run_range "15" "16" \
    --checkpoint_dir "checkpoints_haiku_3" \
    --distractions \
    --use_soft_system_prompt

echo "Done"

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --model "claude-3-5-haiku-latest" \
    --run_range "17" "18" \
    --checkpoint_dir "checkpoints_haiku_3" \
    --distractions \
    --use_soft_system_prompt

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --model "claude-3-5-haiku-latest" \
    --run_range "19" "20" \
    --checkpoint_dir "checkpoints_haiku_3" \
    --distractions \
    --use_soft_system_prompt

echo "Done"