# Goal Drift Evaluations

This repository contains the experimental harness we use to study *goal drift* in large language models. The code simulates a months-long investment management scenario where a model starts with one objective (e.g., maximize profit) and is later pressured toward a conflicting target (e.g., minimize carbon emissions). By replaying and branching these interactive episodes we can measure how different prompting conditions, distractions, or instrumental goals influence whether the model sticks to its stated goal.

## Repository Layout
- `run_simulation.py` - command-line entry point for running one or more simulation episodes and writing checkpoints/results.
- `manage_simulation.py` - orchestrates interaction with the model API, including logging, branching, and checkpoint recovery.
- `simulation/` - core simulation logic shared across experiments. `default_simulation.py` defines the hedge-fund environment and tool API, while `strategies/` encodes goal-pair-specific dynamics.
- `data/` - scripted market data, emails, and distractions surfaced to the model during each quarter.
- `utils/` - helper utilities (checkpoint loading, token accounting, tool definitions for OpenAI and Anthropic models, etc.).
- `plots*.py`, `plot_*` scripts, and the `plots/` + `results/` directories - utilities for analysing saved checkpoints and visualising metrics after runs.
- `run_simulations_*.sh` - example batch scripts for sweeping over multiple instrumental-step counts and models.

## Prerequisites
- Python 3.12 (matching the version used to lock `requirements.txt`).
- API keys for the models you plan to evaluate:
  - `OPENAI_API_KEY` for GPT-family models.
  - `ANTHROPIC_API_KEY` for Claude-family models.
- Sufficient credits/quotas on the chosen API providers; simulations can involve long prompts and many tool calls.

Export the keys before running experiments, for example:

```bash
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
```

## Environment Setup
1. (Recommended) create a virtual environment:
   ```bash
   python3.12 -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

## Running Simulations
The primary workflow is driven by `run_simulation.py`.

```bash
python run_simulation.py \
  --model gpt-4o-mini \
  --runs 1 2 3 \
  --source profit \
  --target env \
  --num_steps 30
```

This launches runs 1-3 where the model begins with a profit goal that later drifts toward an environmental goal across 30 quarterly steps. Key options:
- `--runs` *n1 n2 ...* **or** `--run_range start end` - choose specific run IDs to execute.
- `--model` - any OpenAI or Anthropic model string recognised by `config.get_api_client` (e.g., `claude-3-5-sonnet-latest`).
- `--source` / `--target` - goal pairing to study (`profit`, `env`, `health`, `privacy`). Source and target must differ.
- `--num_steps` - maximum quarters to simulate.
- `--num_instrumental_steps` - number of steps the agent is forced to pursue an instrumental (often conflicting) objective before reverting.
- `--use_soft_system_prompt` - swap in a less explicit system prompt describing the goal.
- `--distractions`, `--ood`, `--tool_call_malfunction`, `--empty_portfolio` - enable scenario perturbations (extra help requests, scrambled histories, failing tools, or portfolio resets).
- `--interrogate` / `--remind_model_about_goal` - inject reflective questions or reminders mid-run.
- `--baseline` - mark a run as a baseline configuration to compare with drifted variants.
- `--parallel` - fan out runs across processes (one per CPU core by default).

### Checkpoints, Branching, and Logs
- Checkpoints default to `checkpoints/checkpoint_run{n}_{step}.pkl`; they store the message transcript and simulation state.
- Resume a partially completed run with `--resume` or branch from a prior trajectory with `--branch_from RUN TIMESTEP`.
- Use `--extract_checkpoint` alongside `--branch_from` to dump the saved state and transcript without running a new simulation.
- Per-run transcripts are mirrored to `logs_<model>/task1_output_run{n}.txt`; aggregate experiment results land in `results.json` (or the file passed via `--results_file`).

### Batch Scripts
The `run_simulations_*.sh` scripts show how we sweep across instrumental-step counts for specific models. Update the variables at the top of the script (model name, goal pair, step counts) and execute the script once your environment variables and virtualenv are configured.

## Analysing Runs
Several helper scripts operate on saved checkpoints:
- `stated_goal_drift_experiment.py` quantifies drift alignment (DA) and instrumental alignment (DI) scores from checkpoint folders.
- `process_checkpoints.py` and `generate_logs.py` assist with extracting transcripts and metrics.
- `plots.py`, `plots_no_conditioning.py`, and `stated_goal_drift_plots.py` generate Matplotlib visualisations of aggregated scores. Figures are written under `plots/`.

Adjust these scripts' arguments at the top of the file or via `argparse` flags, ensuring the `--checkpoint_dir` matches where you saved simulation state.

## Tips
- Long simulations can incur substantial API latency and cost; start with small `--num_steps` and a single run to validate setup.
- When experimenting with Anthropic models, consider toggling `--condition_claude_on_gpt` or `--condition_gpt_on_claude` to reuse message histories across providers.
- Keep an eye on `logs_<model>/task1_output_run*.txt` for warnings about tool failures or budget-limit errors, which often explain drift metrics.

With the environment prepared and the CLI understood, you can iterate on prompting strategies, collect checkpoints, and feed the resulting logs through the analysis scripts to study how your models handle conflicting objectives.
