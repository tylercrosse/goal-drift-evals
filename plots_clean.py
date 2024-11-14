# %%
import json
import numpy as np
import matplotlib.pyplot as plt

# %%
with open('logs_gpt_no_dist_100_steps/results.json', 'r') as f:
    data_no_distractions = json.load(f)

with open('logs_gpt_with_distractions_100_steps/results.json', 'r') as f:
    data_with_distractions = json.load(f)

with open('logs_gpt_mixed_distractions_100_steps/results.json', 'r') as f:
    data_mixed = json.load(f)

data_no_distractions = data_no_distractions['Task 1']['gpt-4o-mini']
data_with_distractions = data_with_distractions['Task 1']['gpt-4o-mini']
data_mixed = data_mixed['Task 1']['gpt-4o-mini']

def create_combined_line_plot(data_with_distr, data_no_distr, data_mixed, title, filename):
    # Initialize lists to store the averaged values for each timestep
    with_distr_averages = []
    no_distr_averages = []
    mixed_averages = []
    
    baselines = ['greedy_decisions', 'greedy_investments', 'do_nothing_baseline', 'fixed_strategy']
    
    # Get number of timesteps from first run
    num_timesteps = len(data_with_distr[0]['intermediate_results'][baselines[0]])
    
    # Calculate average across all baselines for each run
    for run in data_with_distr:
        baseline_values = np.array([run['intermediate_results'][b] for b in baselines])
        with_distr_averages.append(np.mean(baseline_values, axis=0))
    
    for run in data_no_distr:
        baseline_values = np.array([run['intermediate_results'][b] for b in baselines])
        no_distr_averages.append(np.mean(baseline_values, axis=0))

    for run in data_mixed:
        baseline_values = np.array([run['intermediate_results'][b] for b in baselines])
        mixed_averages.append(np.mean(baseline_values, axis=0))

    # Convert to numpy arrays
    with_distr_averages = np.array(with_distr_averages)
    no_distr_averages = np.array(no_distr_averages)
    mixed_averages = np.array(mixed_averages)

    # Calculate means and standard errors
    with_distr_means = np.mean(with_distr_averages, axis=0)
    with_distr_errors = np.std(with_distr_averages, axis=0) / np.sqrt(len(with_distr_averages))
    no_distr_means = np.mean(no_distr_averages, axis=0)
    no_distr_errors = np.std(no_distr_averages, axis=0) / np.sqrt(len(no_distr_averages))
    mixed_means = np.mean(mixed_averages, axis=0)
    mixed_errors = np.std(mixed_averages, axis=0) / np.sqrt(len(mixed_averages))

    # Create the plot with increased font sizes
    plt.rcParams.update({'font.size': 12})  # Increase base font size
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.axhline(y=1.0, color='black', linestyle='--', alpha=0.5)

    x = np.arange(num_timesteps) + 1  # Add 1 to start from timestep 1 instead of 0

    # Add vertical dotted lines with labels
    for timestep in [15, 45, 75]:
        ax.axvline(x=timestep, color='gray', linestyle=':', alpha=0.5)
        # Add label slightly above the top of the plot
        ax.text(timestep - 0.75, -0.2, f'distractions added', rotation=90, ha='center', va='bottom')

    # Add vertical dotted lines with labels
    for timestep in [30, 60, 90]:
        ax.axvline(x=timestep, color='gray', linestyle=':', alpha=0.5)
        # Add label slightly above the top of the plot
        ax.text(timestep - 0.75, -0.2, f'distractions removed', rotation=90, ha='center', va='bottom')

    # Plot lines with shaded error regions
    
    ax.plot(x, no_distr_means, label='No adversarial pressure', marker='o')
    ax.fill_between(x, no_distr_means - no_distr_errors, 
                   no_distr_means + no_distr_errors, alpha=0.2)
    
    ax.plot(x, mixed_means, label='Adversarial pressure included on half of the time steps', marker='o')
    ax.fill_between(x, mixed_means - mixed_errors, 
                   mixed_means + mixed_errors, alpha=0.2)
    
    ax.plot(x, with_distr_means, label='Adversarial pressure always included', marker='o')
    ax.fill_between(x, with_distr_means - with_distr_errors, 
                   with_distr_means + with_distr_errors, alpha=0.2)

    # Increase font sizes for labels and title
    ax.set_ylabel("Model's profit divided by the mean baseline profit", fontsize=12)
    ax.set_xlabel("Timestep", fontsize=12)
    ax.set_title(title, fontsize=16, pad=20)
    
    # Increase tick label sizes
    ax.tick_params(axis='both', which='major', labelsize=11)
    
    # Increase legend font size
    ax.legend(fontsize=12)
    
    # Set x-axis ticks to show every 5 timesteps
    ax.set_xticks(np.arange(0, num_timesteps + 1, 5))
    
    ax.grid(True, alpha=0.3)
    ax.set_ylim(-0.3, 2.2)
    ax.set_yticks(np.arange(-0.2, 2.3, 0.2))

    plt.tight_layout()
    plt.savefig(filename, dpi=300)  # Increased DPI for better quality
    plt.close()

    print(f"Plot saved as {filename}")

# Create the comparison plot
create_combined_line_plot(
    data_with_distractions,
    data_no_distractions,
    data_mixed,
    "Comparison of model performance with and without distractions\n(4o-mini, averaged across all baselines)",
    'plots/line_plot_comparison_averaged.png'
)
