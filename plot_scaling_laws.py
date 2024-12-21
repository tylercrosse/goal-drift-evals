
# %%
import json
import numpy as np
import matplotlib.pyplot as plt

def get_stats(data, clamp=False):
    mean = np.mean(data, axis=0)
    std_err = np.std(data, axis=0) / np.sqrt(len(data))
    confidence_interval = 1.96 * std_err
    if clamp:
        lower_bound = np.maximum(0, mean - confidence_interval)
        upper_bound = np.minimum(100, mean + confidence_interval)
    else:
        lower_bound = mean - confidence_interval
        upper_bound = mean + confidence_interval
    return mean, lower_bound, upper_bound



# %%
def load_data():
    """Load data for a specific model and its variants."""
    paths = [
        f'scaling_laws/ep_sonnet_2/results.json',
        f'scaling_laws/ep_sonnet_4/results.json',
        f'scaling_laws/ep_sonnet_8/results.json',
        # f'scaling_laws/sonnet_16/results.json',
        f'scaling_laws/ep_sonnet_2_gpt/results.json',
        f'scaling_laws/ep_sonnet_4_gpt/results.json',
        f'scaling_laws/ep_sonnet_8_gpt/results.json',
        # f'scaling_laws/hp_sonnet_16_gpt/results.json',
        f'scaling_laws/hp_scaling_law_2/baseline.json',
        f'scaling_laws/hp_scaling_law_4/baseline.json',
        f'scaling_laws/hp_scaling_law_8/baseline.json',
        # f'scaling_laws/hp_scaling_law_16/baseline.json',
    ]
    
    data = []
    for path in paths:
        with open(path, 'r') as f:
            data.append(json.load(f))
    return data

def extract_emissions(data, model_key):
    emissions = []
    for run in data['Task 1'][model_key]:
        emissions.append(run['intermediate_combined_ratios'])
    return emissions  # Return as list, not numpy array

def calculate_last_10_mean_with_ci(model_name, emissions):
    # Get the last 10 means for each run
    last_10_means = []
    for emission in emissions:
        last_10_means.append(np.mean(emission[-10:]))
    
    # Calculate mean and confidence intervals using get_stats directly on the array
    mean, lower, upper = get_stats(np.array(last_10_means), clamp=True)
    return mean, lower, upper

def plot_intrinsification():
    # Model configurations
    models = {
        'sonnet': {'key': 'claude-3-5-sonnet-latest'}
    }

    data = load_data()
    # Load and process data for each model
    normal_results = {
        '2_steps': calculate_last_10_mean_with_ci('sonnet', extract_emissions(data[0], 'claude-3-5-sonnet-latest')),
        '4_steps': calculate_last_10_mean_with_ci('sonnet', extract_emissions(data[1], 'claude-3-5-sonnet-latest')),
        '8_steps': calculate_last_10_mean_with_ci('sonnet', extract_emissions(data[2], 'claude-3-5-sonnet-latest')),
        # '16_steps': calculate_last_10_mean_with_ci('sonnet', extract_emissions(data[3], 'claude-3-5-sonnet-latest')),
    }

    # Process normal data (indices 4-7)
    ablation_results = {
        '2_steps': calculate_last_10_mean_with_ci('sonnet', extract_emissions(data[3], 'claude-3-5-sonnet-latest')),
        '4_steps': calculate_last_10_mean_with_ci('sonnet', extract_emissions(data[4], 'claude-3-5-sonnet-latest')),
        '8_steps': calculate_last_10_mean_with_ci('sonnet', extract_emissions(data[5], 'claude-3-5-sonnet-latest')),
        # '16_steps': calculate_last_10_mean_with_ci('sonnet', extract_emissions(data[7], 'claude-3-5-sonnet-latest')),
    }

    # Calculate values for both conditions
    x_values = [2, 4, 8]
    
    # Extract values for single source
    ss_differences = []
    ss_ci_lower = []
    ss_ci_upper = []
    for steps in [2, 4, 8]:
        key = f'{steps}_steps'
        mean, lower, upper = ablation_results[key]
        ss_differences.append(mean)
        ss_ci_lower.append(lower)
        ss_ci_upper.append(upper)

    # Extract values for normal
    normal_differences = []
    normal_ci_lower = []
    normal_ci_upper = []
    for steps in [2, 4, 8]:
        key = f'{steps}_steps'
        mean, lower, upper = normal_results[key]
        normal_differences.append(mean)
        normal_ci_lower.append(lower)
        normal_ci_upper.append(upper)

    # Create plot
    plt.figure(figsize=(12, 6))
    
    # Plot single source line
    plt.errorbar(x_values, ss_differences, 
                yerr=[np.array(ss_differences) - np.array(ss_ci_lower), 
                      np.array(ss_ci_upper) - np.array(ss_differences)], 
                fmt='o-', color='blue',
                label='Conditioned on 4o-mini', capsize=5, capthick=1, elinewidth=1)
    
    # Plot normal line
    plt.errorbar(x_values, normal_differences, 
                yerr=[np.array(normal_differences) - np.array(normal_ci_lower), 
                      np.array(normal_ci_upper) - np.array(normal_differences)], 
                fmt='o-', color='red', 
                label='Normal conditioning', capsize=5, capthick=1, elinewidth=1)
    
    plt.xscale('log')
    plt.title('Effect of Instrumental Steps on Goal Drift Score (Sonnet)')
    plt.ylabel('Goal drift score')
    plt.ylim(-0.1, 1.1)
    plt.xlabel('Number of instrumental steps')
    plt.xticks([2, 4, 8], ['2¹', '2²', '2³'])
    plt.gca().minorticks_off()
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig('plots/intrinsification_comparison.png', dpi=300)
    plt.close()

plot_intrinsification()

# %%

def load_data():
    """Load data for a specific model and its variants."""
    paths = [
        f'scaling_laws/ph_scaling_law_2_single_source/results.json',
        f'scaling_laws/ph_scaling_law_4_single_source/results.json',
        f'scaling_laws/ph_scaling_law_8_single_source/results.json',
        f'scaling_laws/ph_scaling_law_16_single_source/results.json',
        f'scaling_laws/pe_scaling_law_2_single_source/results.json',
        f'scaling_laws/pe_scaling_law_4_single_source/results.json',
        f'scaling_laws/pe_scaling_law_8_single_source/results.json',
        f'scaling_laws/pe_scaling_law_16_single_source/results.json',
        f'scaling_laws/ph_scaling_law_2_single_source/baseline.json',
        f'scaling_laws/ph_scaling_law_4_single_source/baseline.json',
        f'scaling_laws/ph_scaling_law_8_single_source/baseline.json',
        f'scaling_laws/ph_scaling_law_16_single_source/baseline.json',
    ]
    
    data = []
    for path in paths:
        with open(path, 'r') as f:
            data.append(json.load(f))
    return data

def extract_emissions(data, model_key):
    emissions = []
    for run in data['Task 1'][model_key]:
        emissions.append(run['intermediate_combined_ratios'])
    return emissions  # Return as list, not numpy array

def calculate_last_10_mean_with_ci(model_name, emissions):
    # Get the last 10 means for each run
    last_10_means = []
    for emission in emissions:
        last_10_means.append(np.mean(emission[-10:]))
    
    # Calculate mean and confidence intervals using get_stats directly on the array
    mean, lower, upper = get_stats(np.array(last_10_means), clamp=True)
    return mean, lower, upper

def plot_intrinsification():
    # Model configurations
    models = {
        '4omini': {'key': 'gpt-4o-mini'}
    }

    data = load_data()
    # Load and process data for each model
    single_source_results = {
        '2_steps': calculate_last_10_mean_with_ci('4omini', extract_emissions(data[0], 'gpt-4o-mini')),
        '4_steps': calculate_last_10_mean_with_ci('4omini', extract_emissions(data[1], 'gpt-4o-mini')),
        '8_steps': calculate_last_10_mean_with_ci('4omini', extract_emissions(data[2], 'gpt-4o-mini')),
        '16_steps': calculate_last_10_mean_with_ci('4omini', extract_emissions(data[3], 'gpt-4o-mini')),
    }

    # Process normal data (indices 4-7)
    normal_results = {
        '2_steps': calculate_last_10_mean_with_ci('4omini', extract_emissions(data[4], 'gpt-4o-mini')),
        '4_steps': calculate_last_10_mean_with_ci('4omini', extract_emissions(data[5], 'gpt-4o-mini')),
        '8_steps': calculate_last_10_mean_with_ci('4omini', extract_emissions(data[6], 'gpt-4o-mini')),
        '16_steps': calculate_last_10_mean_with_ci('4omini', extract_emissions(data[7], 'gpt-4o-mini')),
    }

    # Calculate values for both conditions
    x_values = [2, 4, 8, 16]
    
    # Extract values for single source
    ss_differences = []
    ss_ci_lower = []
    ss_ci_upper = []
    for steps in [2, 4, 8, 16]:
        key = f'{steps}_steps'
        mean, lower, upper = single_source_results[key]
        ss_differences.append(mean)
        ss_ci_lower.append(lower)
        ss_ci_upper.append(upper)

    # Extract values for normal
    normal_differences = []
    normal_ci_lower = []
    normal_ci_upper = []
    for steps in [2, 4, 8, 16]:
        key = f'{steps}_steps'
        mean, lower, upper = normal_results[key]
        normal_differences.append(mean)
        normal_ci_lower.append(lower)
        normal_ci_upper.append(upper)

    # Create plot
    plt.figure(figsize=(12, 6))
    
    # Plot single source line
    plt.errorbar(x_values, ss_differences, 
                yerr=[np.array(ss_differences) - np.array(ss_ci_lower), 
                      np.array(ss_ci_upper) - np.array(ss_differences)], 
                fmt='o-', color='blue',
                label='Drift from minimizing health externalities to profit maximization', capsize=5, capthick=1, elinewidth=1)
    
    # Plot normal line
    plt.errorbar(x_values, normal_differences, 
                yerr=[np.array(normal_differences) - np.array(normal_ci_lower), 
                      np.array(normal_ci_upper) - np.array(normal_differences)], 
                fmt='o-', color='red', 
                label='Drift from minimizing emissions to profit maximization', capsize=5, capthick=1, elinewidth=1)
    
    plt.xscale('log')
    plt.title('Effect of Instrumental Steps on Goal Drift Score (branched from a single run, 4o-mini)')
    plt.ylabel('Goal drift score')
    plt.ylim(-0.1, 1.1)
    plt.xlabel('Number of instrumental steps')
    plt.xticks([2, 4, 8, 16], ['2¹', '2²', '2³', '2⁴'])
    plt.gca().minorticks_off()
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig('plots/intrinsification_comparison.png', dpi=300)
    plt.close()

plot_intrinsification()

# %%
