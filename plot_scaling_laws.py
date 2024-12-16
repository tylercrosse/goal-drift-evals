
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
        f'scaling_laws/hp_scaling_law_2_single_source/results.json',
        f'scaling_laws/hp_scaling_law_4_single_source/results.json',
        f'scaling_laws/hp_scaling_law_8_single_source/results.json',
        f'scaling_laws/hp_scaling_law_16_single_source/results.json',
        f'scaling_laws/hp_scaling_law_2/baseline.json',
        f'scaling_laws/hp_scaling_law_4/baseline.json',
        f'scaling_laws/hp_scaling_law_8/baseline.json',
        f'scaling_laws/hp_scaling_law_16/baseline.json',
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
        last_10_means.append(np.mean(emission[-10:]) * 100)
    
    # Calculate mean and confidence intervals using get_stats directly on the array
    mean, lower, upper = get_stats(np.array(last_10_means), clamp=True)
    return mean, lower, upper

def plot_intrinsification():
    # Model configurations
    models = {
        '4omini': {'key': 'gpt-4o-mini'}
    }
    
    # Load and process data for each model
    results = {}
    for model_name, config in models.items():
        data = load_data()
        results[model_name] = {
            '2_steps': calculate_last_10_mean_with_ci(model_name, extract_emissions(data[0], config['key'])),
            '4_steps': calculate_last_10_mean_with_ci(model_name, extract_emissions(data[1], config['key'])),
            '8_steps': calculate_last_10_mean_with_ci(model_name, extract_emissions(data[2], config['key'])),
            '16_steps': calculate_last_10_mean_with_ci(model_name, extract_emissions(data[3], config['key'])),
        }

    # Calculate differences with confidence intervals
    differences = []
    ci_lower = []
    ci_upper = []
    for steps in [2, 4, 8, 16]:
        key = f'{steps}_steps'

        # Get values for both conditions
        instr_mean, instr_lower, instr_upper = results['4omini'][key]
        
        differences.append(instr_mean)
        ci_lower.append(instr_lower)
        ci_upper.append(instr_upper)

    # Create plot
    plt.figure(figsize=(12, 6))
    x_values = [2, 4, 8, 16]
    
    # Plot main line with error bars
    plt.errorbar(x_values, differences, 
                yerr=[np.array(differences) - np.array(ci_lower), 
                      np.array(ci_upper) - np.array(differences)], 
                fmt='o-', color='blue', 
                label='Mean difference', capsize=5, capthick=1, elinewidth=1)
    
    plt.xscale('log')
    plt.title('Intrinsification: Signed Mean Percentage Point Difference in Investments in High-Emission Stocks\nBetween Baseline and Instrumental Goal Conditioned Runs (last 10 steps)')
    plt.ylabel('SMPPD')
    plt.xlabel('Number of Instrumental Steps')
    plt.xticks([2, 4, 8, 16], ['2¹', '2²', '2³', '2⁴'])
    plt.gca().minorticks_off()
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig('plots/intrinsification_comparison.png', dpi=300)
    plt.close()

plot_intrinsification()

# %%
