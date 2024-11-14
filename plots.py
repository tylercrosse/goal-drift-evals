# %%
import json
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def plot_metrics_comparison():
    # Load the data
    with open('logs_env_no_nudge/results.json', 'r') as f:
        no_dist_data = json.load(f)
    with open('logs_env/results.json', 'r') as f:
        privacy_data = json.load(f)
    
    # Extract metrics for both conditions
    def extract_metrics(data):
        runs = data['Task 1']['gpt-4o-mini']
        # Calculate normalized profits
        norm_profits = [(run['profit'] / run['baseline']) for run in runs]
        # Calculate best option ratio for each run
        best_ratios = [run['best_option_chosen'] / run['investments_made'] 
                    if run['investments_made'] > 0 else 0 
                    for run in runs]
        return norm_profits, best_ratios
    
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
    
    no_dist_profit_mean, no_dist_profit_ci_low, no_dist_profit_ci_high = get_stats(no_dist_profits)
    privacy_profit_mean, privacy_profit_ci_low, privacy_profit_ci_high = get_stats(privacy_profits)
    no_dist_ratio_mean, no_dist_ratio_ci_low, no_dist_ratio_ci_high = get_stats(no_dist_ratio)
    privacy_ratio_mean, privacy_ratio_ci_low, privacy_ratio_ci_high = get_stats(privacy_ratio)

    # Create the grouped bars
    no_nudge_bars = ax.bar(x - width/2, [no_dist_profit_mean, no_dist_ratio_mean], width, 
                        label='Without nudges')
    nudge_bars = ax.bar(x + width/2, [privacy_profit_mean, privacy_ratio_mean], width,
                    label='With nudges')

    # Add error bars for both metrics
    ax.errorbar(x[0] - width/2, no_dist_profit_mean, 
            yerr=[[no_dist_profit_mean - no_dist_profit_ci_low], 
                    [no_dist_profit_ci_high - no_dist_profit_mean]],
            fmt='none', color='black', capsize=5)
    ax.errorbar(x[0] + width/2, privacy_profit_mean,
            yerr=[[privacy_profit_mean - privacy_profit_ci_low], 
                    [privacy_profit_ci_high - privacy_profit_mean]],
            fmt='none', color='black', capsize=5)
    ax.errorbar(x[1] - width/2, no_dist_ratio_mean,
            yerr=[[no_dist_ratio_mean - no_dist_ratio_ci_low], 
                    [no_dist_ratio_ci_high - no_dist_ratio_mean]],
            fmt='none', color='black', capsize=5)
    ax.errorbar(x[1] + width/2, privacy_ratio_mean,
            yerr=[[privacy_ratio_mean - privacy_ratio_ci_low], 
                    [privacy_ratio_ci_high - privacy_ratio_mean]],
            fmt='none', color='black', capsize=5)
    
    # Customize the plot
    ax.set_ylabel('Percentage')
    ax.set_title('Comparison between runs where the model is nudged to change its goal\nand runs where it isn\'t (4o-mini, environment-related trade-offs)')
    ax.set_xticks(x)
    ax.set_xticklabels(['Profit divided by baseline profit', 'Fraction of investments\nin the most profitable stock\nafter stating the goal\non timestep 40'])
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
with open('logs_emissions/results.json', 'r') as f:
    data = json.load(f)

with open('logs_emissions_no_nudge/results.json', 'r') as f:
    data_no_nudge = json.load(f)

def plot_investment_distribution(data, data_no_nudge):
    # Extract data for both conditions
    def get_investments(data):
        runs = data['Task 1']['gpt-4o-mini']
        positive = [run['investments_in_positive_stocks'] for run in runs]
        negative = [run['investments_in_negative_stocks'] for run in runs]
        return positive, negative
    
    pos_nudge, neg_nudge = get_investments(data)
    pos_no_nudge, neg_no_nudge = get_investments(data_no_nudge)
    
    # Calculate means and confidence intervals
    def get_stats(data):
        mean = np.mean(data)
        ci = stats.t.interval(0.95, len(data)-1, loc=mean, scale=stats.sem(data))
        return mean, ci[0], ci[1]
    
    # Set up the plot
    fig, ax = plt.subplots(figsize=(10, 6))
    width = 0.35
    x = np.arange(2)
    
    # Calculate statistics
    pos_nudge_mean, pos_nudge_ci_low, pos_nudge_ci_high = get_stats(pos_nudge)
    neg_nudge_mean, neg_nudge_ci_low, neg_nudge_ci_high = get_stats(neg_nudge)
    pos_no_nudge_mean, pos_no_nudge_ci_low, pos_no_nudge_ci_high = get_stats(pos_no_nudge)
    neg_no_nudge_mean, neg_no_nudge_ci_low, neg_no_nudge_ci_high = get_stats(neg_no_nudge)
    
    # Create grouped bars
    no_nudge_bars = ax.bar(x - width/2, [pos_no_nudge_mean, neg_no_nudge_mean], width, 
                          label='Model is not nudged')
    nudge_bars = ax.bar(x + width/2, [pos_nudge_mean, neg_nudge_mean], width,
                       label='Model is nudged to make more profit')
    
    # Add error bars
    ax.errorbar(x[0] - width/2, pos_no_nudge_mean,
                yerr=[[pos_no_nudge_mean - pos_no_nudge_ci_low], 
                      [pos_no_nudge_ci_high - pos_no_nudge_mean]],
                fmt='none', color='black', capsize=5)
    ax.errorbar(x[0] + width/2, pos_nudge_mean,
                yerr=[[pos_nudge_mean - pos_nudge_ci_low], 
                      [pos_nudge_ci_high - pos_nudge_mean]],
                fmt='none', color='black', capsize=5)
    ax.errorbar(x[1] - width/2, neg_no_nudge_mean,
                yerr=[[neg_no_nudge_mean - neg_no_nudge_ci_low], 
                      [neg_no_nudge_ci_high - neg_no_nudge_mean]],
                fmt='none', color='black', capsize=5)
    ax.errorbar(x[1] + width/2, neg_nudge_mean,
                yerr=[[neg_nudge_mean - neg_nudge_ci_low], 
                      [neg_nudge_ci_high - neg_nudge_mean]],
                fmt='none', color='black', capsize=5)
    
    # Customize plot
    ax.set_ylabel('Average investment amount over the whole run', fontsize=12)
    ax.set_title('Investments in carbon-negative and carbon-positive stocks (4o-mini)', fontsize=16, pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(['Carbon-negative,\nless profitable stocks', 'Carbon-positive,\nmore profitable stocks'], fontsize=12)
    ax.legend(fontsize=12)
    ax.tick_params(axis='both', which='major', labelsize=11)
    
    # Add value labels
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'${height:,.0f}',
                       xy=(rect.get_x() + rect.get_width()/2, height),
                       xytext=(0, 3),
                       textcoords="offset points",
                       ha='center', va='bottom')
    
    autolabel(no_nudge_bars)
    autolabel(nudge_bars)
    
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    filename = 'plot.png'
    plt.tight_layout()
    plt.savefig(filename, dpi=300)  # Increased DPI for better quality
    plt.close()

plot_investment_distribution(data, data_no_nudge)
# %%
