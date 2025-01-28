SOURCE="env"
TARGET="profit"
NUM_STEPS=10

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --model "gpt-4o-mini" \
    --run_range "4" "10" \
    --checkpoint_dir "checkpoints_4omini" \
    --resume

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --model "gpt-4o-mini" \
    --run_range "11" "15" \
    --checkpoint_dir "checkpoints_4omini" \
    --resume

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --model "gpt-4o-mini" \
    --run_range "16" "20" \
    --checkpoint_dir "checkpoints_4omini" \
    --resume

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --model "gpt-4o-mini" \
    --run_range "4" "10" \
    --checkpoint_dir "checkpoints_4omini" \
    --resume

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --model "gpt-4o-mini" \
    --run_range "11" "15" \
    --checkpoint_dir "checkpoints_4omini" \
    --resume

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --model "gpt-4o-mini" \
    --run_range "16" "20" \
    --checkpoint_dir "checkpoints_4omini" \
    --resume

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --model "gpt-4o-mini" \
    --run_range "4" "10" \
    --checkpoint_dir "checkpoints_4omini" \
    --resume

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --model "gpt-4o-mini" \
    --run_range "11" "15" \
    --checkpoint_dir "checkpoints_4omini" \
    --resume

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "${NUM_STEPS}" \
    --parallel \
    --model "gpt-4o-mini" \
    --run_range "16" "20" \
    --checkpoint_dir "checkpoints_4omini" \
    --resume

echo "Done"