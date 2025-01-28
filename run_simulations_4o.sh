SOURCE="profit"
TARGET="env"
NUM_STEPS=10

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --model "gpt-4o-2024-11-20" \
    --run_range "6" "10" \
    --checkpoint_dir "checkpoints_4o" \
    --resume

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --model "gpt-4o-2024-11-20" \
    --run_range "11" "15" \
    --checkpoint_dir "checkpoints_4o" \
    --resume

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --model "gpt-4o-2024-11-20" \
    --run_range "16" "20" \
    --checkpoint_dir "checkpoints_4o" \
    --resume

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --model "gpt-4o-2024-11-20" \
    --run_range "6" "10" \
    --checkpoint_dir "checkpoints_4o" \
    --resume

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --model "gpt-4o-2024-11-20" \
    --run_range "11" "15" \
    --checkpoint_dir "checkpoints_4o" \
    --resume

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --model "gpt-4o-2024-11-20" \
    --run_range "16" "20" \
    --checkpoint_dir "checkpoints_4o" \
    --resume

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --model "gpt-4o-2024-11-20" \
    --run_range "6" "10" \
    --checkpoint_dir "checkpoints_4o" \
    --resume

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --model "gpt-4o-2024-11-20" \
    --run_range "11" "15" \
    --checkpoint_dir "checkpoints_4o" \
    --resume

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --model "gpt-4o-2024-11-20" \
    --run_range "16" "20" \
    --checkpoint_dir "checkpoints_4o" \
    --resume

echo "Done"