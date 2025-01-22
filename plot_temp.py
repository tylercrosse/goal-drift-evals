# %%
import matplotlib.pyplot as plt
import numpy as np

def plot_ratios():
    # Define colors (same as plot_profits.py)
    colors = {
        'baseline': '#2c7bb6',
        'adv_pressure': '#d7191c',
        'igc': '#FDAE61'
    }

    # Data
    labels = ['Adversarial Pressure', 'Instrumental Goal Conditioning']
    values = [0.8, 1.0]

    # Set up figure with grey styling
    fig, ax = plt.subplots(figsize=(6, 5))
    grey_color = '#606060'
    for spine in ax.spines.values():
        spine.set_color(grey_color)
        spine.set_linewidth(1.5)

    # Remove ticks but keep labels
    ax.tick_params(axis='both', length=0, colors=grey_color, pad=5)

    # Create bars
    x = np.arange(len(labels))
    width = 0.6

    bars = ax.bar(x, values, width, 
                color=[colors['adv_pressure'], colors['igc']])

    # Style labels and title
    ax.set_xlabel('Setting', color=grey_color, labelpad=10)
    ax.set_ylabel('Score', color=grey_color, labelpad=10)
    ax.set_title('Goal Drift Score', 
                color='black', pad=15, fontsize=14)

    # Configure grid and limits
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_ylim(0, 1.1)  # Add some padding above 1.0
    ax.set_xticks([])

    # Add legend (same order as plot_profits.py)
    legend_elements = [
        plt.Rectangle((0,0),1,1, color=colors['adv_pressure'], label='Adversarial Pressure'),
        plt.Rectangle((0,0),1,1, color=colors['igc'], label='Instrumental Goal Conditioning')
    ]
    ax.legend(handles=legend_elements, loc='upper left', frameon=False)

    plt.tight_layout()
    plt.savefig('plots/ratio_comparison.png', bbox_inches='tight')
    plt.savefig('plots/ratio_comparison.svg', bbox_inches='tight')


plot_ratios()
# %%
