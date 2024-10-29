# %%
import json
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def plot_metrics_comparison():
    # Load the data
    with open('logs_health_no_nudge/results.json', 'r') as f:
        no_dist_data = json.load(f)
    with open('logs_health/results.json', 'r') as f:
        privacy_data = json.load(f)
    
    # Extract metrics for both conditions
    def extract_metrics(data):
        runs = data['Task 1']['gpt-4o-mini']
        # Calculate normalized profits
        norm_profits = [(run['profit'] / run['baseline']) for run in runs]
        # Calculate best option ratio
        total_best = sum(run['best_option_chosen'] for run in runs)
        total_investments = sum(run['investments_made'] for run in runs)
        best_ratio = total_best / total_investments if total_investments > 0 else 0
        return norm_profits, best_ratio
    
    no_dist_profits, no_dist_ratio = extract_metrics(no_dist_data)
    privacy_profits, privacy_ratio = extract_metrics(privacy_data)
    
    # Calculate means and confidence intervals for normalized profits
    def get_stats(data):
        mean = np.mean(data)
        ci = stats.t.interval(0.95, len(data)-1, loc=mean, scale=stats.sem(data))
        return mean, ci[0], ci[1]
    
    # Set up the plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Set width of bars and positions of the bars
    width = 0.35
    x = np.arange(2)  # the label locations
    
    # Calculate stats for normalized profits
    no_dist_mean, no_dist_ci_low, no_dist_ci_high = get_stats(no_dist_profits)
    privacy_mean, privacy_ci_low, privacy_ci_high = get_stats(privacy_profits)
    
    # Create the grouped bars
    no_nudge_bars = ax.bar(x - width/2, [no_dist_mean, no_dist_ratio], width, 
                          label='Without nudges')
    nudge_bars = ax.bar(x + width/2, [privacy_mean, privacy_ratio], width,
                       label='With nudges')
    
    # Add error bars for normalized profits (first bar in each group)
    ax.errorbar(x[0] - width/2, no_dist_mean, 
               yerr=[[no_dist_mean - no_dist_ci_low], [no_dist_ci_high - no_dist_mean]],
               fmt='none', color='black', capsize=5)
    ax.errorbar(x[0] + width/2, privacy_mean,
               yerr=[[privacy_mean - privacy_ci_low], [privacy_ci_high - privacy_mean]],
               fmt='none', color='black', capsize=5)
    
    # Customize the plot
    ax.set_ylabel('Percentage')
    ax.set_title('Comparison between runs where the model is nudged to change its goal\nand runs where it isn\'t (4o-mini, health-related trade-offs)')
    ax.set_xticks(x)
    ax.set_xticklabels(['Profit divided by baseline profit', 'Fraction of investments\nin the most profitable stock\nafter stating the goal'])
    ax.legend()
    
    # Add value labels on the bars
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.2f}',
                       xy=(rect.get_x() + rect.get_width()/2, height),
                       xytext=(0, 3),  # 3 points vertical offset
                       textcoords="offset points",
                       ha='center', va='bottom')
    
    autolabel(no_nudge_bars)
    autolabel(nudge_bars)
    
    plt.tight_layout()
    plt.show()

plot_metrics_comparison()
# %%
