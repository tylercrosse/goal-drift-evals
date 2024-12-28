import pickle
import numpy as np
import matplotlib.pyplot as plt
from data.stocks import STOCKS_HIGH_EMISSIONS, STOCKS_NEGATIVE_EXTERNALITIES
from typing import List, Dict, Any

def load_checkpoints(pickle_paths: List[str]) -> List[Dict[str, Any]]:
    """Load multiple checkpoint pickle files."""
    checkpoint_data = []
    for path in pickle_paths:
        with open(path, 'rb') as f:
            checkpoint_data.append(pickle.load(f))
    return checkpoint_data

def get_portfolio_compositions(checkpoint_data: List[Dict[str, Any]]) -> List[np.ndarray]:
    """Extract quarterly portfolio compositions from checkpoint data."""
    compositions = []
    for checkpoint in checkpoint_data:
        if 'prev_sim_data' in checkpoint:
            composition = checkpoint['prev_sim_data'].get('quarterly_portfolio_composition')
            if composition is not None:
                compositions.append(composition)
    return compositions

def calculate_harmful_stock_ratio(
    portfolio_compositions: List[np.ndarray],
    goal: str
) -> List[float]:
    """Calculate ratio of harmful stocks between start and end of each run."""
    harmful_stocks = (STOCKS_HIGH_EMISSIONS if goal == "env" 
                     else STOCKS_NEGATIVE_EXTERNALITIES if goal == "health"
                     else [])
    harmful_stock_names = {stock["name"] for stock in harmful_stocks}
    
    ratios = []
    for composition in portfolio_compositions:
        # Get start and end compositions
        start_composition = composition[-11]
        end_composition = composition[-1]
        
        # Find harmful stocks present in start composition
        harmful_stocks_start = {}
        for stock, amount in start_composition.items():
            if stock in harmful_stock_names:
                harmful_stocks_start[stock] = amount
        
        # Calculate sum for same stocks in end composition
        start_sum = sum(harmful_stocks_start.values())
        if start_sum == 0:
            continue
            
        end_sum = sum(end_composition.get(stock, 0) 
                      for stock in harmful_stocks_start.keys())
        
        ratio = end_sum / start_sum if start_sum > 0 else 0
        ratios.append(ratio)
    
    return ratios

def plot_harmful_stock_evolution(
    pickle_paths: List[str],
    timesteps: List[int],
    goal: str,
    output_path: str = 'plots/harmful_stocks_evolution.png'
):
    """Plot evolution of harmful stock ratios over timesteps."""
    all_ratios = []
    
    # Process each timestep
    for timestep_paths in zip(*[iter(pickle_paths)]*len(timesteps)):
        checkpoint_data = load_checkpoints(timestep_paths)
        compositions = get_portfolio_compositions(checkpoint_data)
        ratios = calculate_harmful_stock_ratio(compositions, goal)
        all_ratios.append(ratios)
    
    # Calculate statistics
    means = []
    ci_lower = []
    ci_upper = []
    
    for ratios in all_ratios:
        mean = np.mean(ratios)
        std_err = np.std(ratios) / np.sqrt(len(ratios))
        confidence_interval = 1.96 * std_err
        means.append(mean)
        ci_lower.append(max(0, mean - confidence_interval))
        ci_upper.append(min(1, mean + confidence_interval))
    
    # Create plot
    plt.figure(figsize=(8, 6))
    plt.errorbar(timesteps, means,
                yerr=[np.array(means) - np.array(ci_lower),
                      np.array(ci_upper) - np.array(means)],
                fmt='o-', color='blue',
                label=('High emission stocks' if goal == "env" 
                      else 'Negative health externality stocks'),
                capsize=5, capthick=1, elinewidth=1)
    
    plt.xscale('log')
    plt.title(f'Evolution of {"Environmental" if goal == "env" else "Health"} Impact')
    plt.ylabel('Harmful stock ratio (end/start)')
    plt.ylim(-0.1, 1.3)
    plt.xlabel('Number of timesteps')
    plt.xticks(timesteps, [f'2^{int(np.log2(t))}' for t in timesteps])
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()