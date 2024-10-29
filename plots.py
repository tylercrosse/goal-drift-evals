# %%
import json
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def plot_profit_comparison():
    # Load the data
    with open('logs_privacy_no_dist/results.json', 'r') as f:
        no_dist_data = json.load(f)
    with open('logs_privacy/results.json', 'r') as f:
        privacy_data = json.load(f)
    
    # Extract profits
    no_dist_profits = [run['portfolio_value'] for run in no_dist_data['Task 1']['gpt-4o-mini']]
    privacy_profits = [run['portfolio_value'] for run in privacy_data['Task 1']['gpt-4o-mini']]
    
    # Calculate means and confidence intervals
    def get_stats(data):
        mean = np.mean(data)
        ci = stats.t.interval(0.95, len(data)-1, loc=mean, scale=stats.sem(data))
        return mean, ci[0], ci[1]
    
    no_dist_mean, no_dist_ci_low, no_dist_ci_high = get_stats(no_dist_profits)
    privacy_mean, privacy_ci_low, privacy_ci_high = get_stats(privacy_profits)
    
    # Create the plot
    plt.figure(figsize=(10, 6))
    conditions = ['Without nudges', 'With nudges']
    means = [no_dist_mean, privacy_mean]
    yerr = [[no_dist_mean - no_dist_ci_low, privacy_mean - privacy_ci_low],
            [no_dist_ci_high - no_dist_mean, privacy_ci_high - privacy_mean]]
    
    plt.bar(conditions, means, yerr=yerr, capsize=10)
    plt.ylabel('Portfolio Value')
    plt.title('Comparison of Profits With and Without Nudges')
    
    # Add value labels on top of bars
    for i, mean in enumerate(means):
        plt.text(i, mean, f'${mean:,.0f}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.show()

plot_profit_comparison()
# %%
