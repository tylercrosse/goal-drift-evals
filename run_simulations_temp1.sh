#!/bin/bash

# Base parameters
SOURCE="profit"
TARGET="env"

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "32" \
    --parallel \
    --model "gpt-4o-mini" \
    --run_range "1" "3" \
    --checkpoint_dir "profit_env_4omini_baseline" \
    --use_soft_system_prompt \
    --resume
    
if [ $? -ne 0 ]; then
    echo "Error occurred during simulation"
fi

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "32" \
    --parallel \
    --model "gpt-4o-mini" \
    --run_range "1" "3" \
    --checkpoint_dir "profit_env_4omini_elicit_baseline" \
    --resume

if [ $? -ne 0 ]; then
    echo "Error occurred during simulation"
fi

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "32" \
    --parallel \
    --model "claude-3-5-sonnet-latest" \
    --run_range "1" "3" \
    --checkpoint_dir "profit_env_sonnet_baseline" \
    --use_soft_system_prompt \
    --resume
    
if [ $? -ne 0 ]; then
    echo "Error occurred during simulation"
fi

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "32" \
    --parallel \
    --model "claude-3-5-sonnet-latest" \
    --run_range "1" "3" \
    --checkpoint_dir "profit_env_sonnet_elicit_baseline" \
    --resume

if [ $? -ne 0 ]; then
    echo "Error occurred during simulation"
fi

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "32" \
    --parallel \
    --model "claude-3-5-haiku-latest" \
    --run_range "1" "3" \
    --checkpoint_dir "profit_env_haiku_baseline" \
    --use_soft_system_prompt \
    --resume
    
if [ $? -ne 0 ]; then
    echo "Error occurred during simulation"
fi

echo "Running simulation..."
python run_simulation.py \
    --source "${SOURCE}" \
    --target "${TARGET}" \
    --num_steps "32" \
    --parallel \
    --model "claude-3-5-haiku-latest" \
    --run_range "1" "3" \
    --checkpoint_dir "profit_env_haiku_elicit_baseline" \
    --resume

if [ $? -ne 0 ]; then
    echo "Error occurred during simulation"
fi

echo "All simulations completed successfully!"