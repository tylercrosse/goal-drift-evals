
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
        upper_bound = np.minimum(1, mean + confidence_interval)
    else:
        lower_bound = mean - confidence_interval
        upper_bound = mean + confidence_interval
    return mean, lower_bound, upper_bound



# %%
def load_data():
    """Load data for a specific model and its variants."""
    paths = [
        f'scaling_law_2/results.json',
        f'scaling_law_4/results.json',
        f'scaling_law_8/results.json',
        f'scaling_law_16/results.json',
        f'scaling_law_2/baseline.json',
        f'scaling_law_4/baseline.json',
        f'scaling_law_8/baseline.json',
        f'scaling_law_16/baseline.json',
    ]
    
    data = []
    for path in paths:
        with open(path, 'r') as f:
            data.append(json.load(f))
    return data

def extract_emissions(data, model_key):
    emissions = []
    for run in data['Task 1'][model_key]:
        emissions.append(run['intermediate_profitable_stock_ratios'])
    return emissions  # Return as list, not numpy array

def calculate_last_5_mean(model_name, emissions):
    # Convert to numpy array only when calculating the mean
    last_5_means = []
    for emission in emissions:
        last_5_means.append(np.mean(emission[-10:]))
    return np.mean(last_5_means) * 100

def plot_intrinsification():
    # Model configurations
    models = {
        # 'haiku': {'key': 'claude-3-5-haiku-latest'},
        # 'sonnet': {'key': 'claude-3-5-sonnet-latest'},
        '4omini': {'key': 'gpt-4o-mini'}
    }
    
    # Load and process data for each model
    results = {}
    for model_name, config in models.items():
        data = load_data()
        results[model_name] = {
            '2_steps': calculate_last_5_mean(model_name, extract_emissions(data[0], config['key'])),
            '4_steps': calculate_last_5_mean(model_name, extract_emissions(data[1], config['key'])),
            '8_steps': calculate_last_5_mean(model_name, extract_emissions(data[2], config['key'])),
            '16_steps': calculate_last_5_mean(model_name, extract_emissions(data[3], config['key'])),
            '2_steps_baseline': calculate_last_5_mean(model_name, extract_emissions(data[4], config['key'])),
            '4_steps_baseline': calculate_last_5_mean(model_name, extract_emissions(data[5], config['key'])),
            '8_steps_baseline': calculate_last_5_mean(model_name, extract_emissions(data[6], config['key'])),
            '16_steps_baseline': calculate_last_5_mean(model_name, extract_emissions(data[7], config['key'])),
        }

    # Calculate abs differences for both normal and 15-steps
    signed_differences = [
        results['4omini']['2_steps'] - results['4omini']['2_steps_baseline'],
        results['4omini']['4_steps'] - results['4omini']['4_steps_baseline'],
        results['4omini']['8_steps'] - results['4omini']['8_steps_baseline'],
        results['4omini']['16_steps'] - results['4omini']['16_steps_baseline']
    ]

    # Create plot
    plt.figure(figsize=(12, 6))
    x_values = [2, 4, 8, 16]  # Define the x-axis values
    plt.plot(x_values, signed_differences, marker='o', color='blue')  # Pass both x and y values to plot
    plt.xscale('log')  # Set x-axis to logarithmic scale
    plt.title('Intrinsification: Signed Mean Percentage Point Difference in Investments in High-Emission Stocks\nBetween Baseline and Instrumental Goal Conditioned Runs (last 5 steps)')
    plt.ylabel('SMPPD')
    plt.xlabel('Number of Instrumental Steps')
    plt.xticks([2, 4, 8, 16], ['2¹', '2²', '2³', '2⁴'])
    plt.gca().minorticks_off()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('plots/intrinsification_comparison.png', dpi=300)
    plt.close()

plot_intrinsification()


# %%
