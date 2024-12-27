from typing import Dict, Any
from simulation.strategies.strategy import SimulationStrategy
from abc import ABC, abstractmethod
import random
from utils.utils import gen_seed


class Simulation(ABC):

    def __init__(self, strategy: SimulationStrategy, run: int, model: str, num_instrumental_steps: int, prev_sim_data: Dict[str, Any] = {}, distractions: bool = False, use_unrelated_instr_goal: bool = False):
        self.run = run
        self.model = model
        self.strategy = strategy
        self.tools = []
        self.distractions = distractions
        self.num_instrumental_steps = num_instrumental_steps
        self.use_unrelated_instr_goal = use_unrelated_instr_goal
        if prev_sim_data:
            print(f"Prev sim data: {prev_sim_data}")
        self.low_profit_stocks = prev_sim_data.get("low_profit_stocks", [])
        self.high_profit_stocks = prev_sim_data.get("high_profit_stocks", [])
        
        if not self.low_profit_stocks or not self.high_profit_stocks:
            self.random_gen = random.Random(gen_seed(0, self.run))
            self.low_profit_stocks, self.high_profit_stocks = self.strategy.gen_stocks(self.random_gen)

        self.budget_low = prev_sim_data.get("budget_low", 8000000)
        self.budget_high = prev_sim_data.get("budget_high", 12000000)
        self.budget = prev_sim_data.get("budget", 0)
        self.portfolio_value = prev_sim_data.get("portfolio_value", 0)
        self.profit = prev_sim_data.get("profit", 0)
        self.year = prev_sim_data.get("year", 2025)
        self.current_timestep = prev_sim_data.get("current_timestep", 1)
        self.savings_baseline = prev_sim_data.get("savings_baseline", 0)
        self.intermediate_profits = prev_sim_data.get("intermediate_profits", [])
        self.intermediate_profit_ratios = prev_sim_data.get("intermediate_profit_ratios", [])
        self.intermediate_active_low_profit_investment_amounts = prev_sim_data.get("intermediate_active_low_profit_investment_amounts", [])
        self.intermediate_active_high_profit_investment_amounts = prev_sim_data.get("intermediate_active_high_profit_investment_amounts", [])
        self.intermediate_profitable_ratios = prev_sim_data.get("intermediate_profitable_ratios", [])
        self.intermediate_investment_ratios = prev_sim_data.get("intermediate_investment_ratios", [])
        self.intermediate_combined_ratios = prev_sim_data.get("intermediate_combined_ratios", [])
        self.intermediate_budgets = prev_sim_data.get("intermediate_budgets", [])
        self.active_investments = prev_sim_data.get("active_investments", {})
        self.budget_limit_errors = prev_sim_data.get("budget_limit_errors", 0)
        self.tool_call_errors = prev_sim_data.get("tool_call_errors", 0)
        self.quarterly_investments_in_low_profit_stocks = prev_sim_data.get("quarterly_investments_in_low_profit_stocks", [])
        self.quarterly_investments_in_high_profit_stocks = prev_sim_data.get("quarterly_investments_in_high_profit_stocks", [])
        self.quarterly_divestments_from_low_profit_stocks = prev_sim_data.get("quarterly_divestments_from_low_profit_stocks", [])
        self.quarterly_divestments_from_high_profit_stocks = prev_sim_data.get("quarterly_divestments_from_high_profit_stocks", [])
        self.quarterly_portfolio_composition = prev_sim_data.get("quarterly_portfolio_composition", [])
        self.last_investment_in_low_profit_stock = prev_sim_data.get("last_investment_in_low_profit_stock", 0)
        self.investments_made = prev_sim_data.get("investments_made", 0)
        self.times_most_profitable_stock_chosen = prev_sim_data.get("times_most_profitable_stock_chosen", 0)
        self.times_least_profitable_stock_chosen = prev_sim_data.get("times_least_profitable_stock_chosen", 0)
        self.used_ids = prev_sim_data.get("used_ids", set())
        self.tool_call_count = prev_sim_data.get("tool_call_count", 0)

    @property
    def prev_sim_data(self):
        return {
            "budget_low": self.budget_low,
            "budget_high": self.budget_high,
            "budget": self.budget,
            "portfolio_value": self.portfolio_value,
            "profit": self.profit,
            "year": self.year,
            "current_timestep": self.current_timestep,
            "low_profit_stocks": self.low_profit_stocks,
            "high_profit_stocks": self.high_profit_stocks,
            "savings_baseline": self.savings_baseline,
            "intermediate_profits": self.intermediate_profits,
            "intermediate_profit_ratios": self.intermediate_profit_ratios,
            "intermediate_active_low_profit_investment_amounts": self.intermediate_active_low_profit_investment_amounts,
            "intermediate_active_high_profit_investment_amounts": self.intermediate_active_high_profit_investment_amounts,
            "intermediate_profitable_ratios": self.intermediate_profitable_ratios,
            "intermediate_combined_ratios": self.intermediate_combined_ratios,
            "intermediate_investment_ratios": self.intermediate_investment_ratios,
            "intermediate_budgets": self.intermediate_budgets,
            "active_investments": self.active_investments,
            "budget_limit_errors": self.budget_limit_errors,
            "tool_call_errors": self.tool_call_errors,
            "quarterly_investments_in_low_profit_stocks": self.quarterly_investments_in_low_profit_stocks,
            "quarterly_investments_in_high_profit_stocks": self.quarterly_investments_in_high_profit_stocks,
            "quarterly_divestments_from_low_profit_stocks": self.quarterly_divestments_from_low_profit_stocks,
            "quarterly_divestments_from_high_profit_stocks": self.quarterly_divestments_from_high_profit_stocks,
            "quarterly_portfolio_composition": self.quarterly_portfolio_composition,
            "last_investment_in_low_profit_stock": self.last_investment_in_low_profit_stock,
            "investments_made": self.investments_made,
            "times_most_profitable_stock_chosen": self.times_most_profitable_stock_chosen,
            "times_least_profitable_stock_chosen": self.times_least_profitable_stock_chosen,
            "used_ids": self.used_ids,
            "tool_call_count": self.tool_call_count,
        }
    
    def get_unique_item(self, random_gen, items_list):
        available_items = [item for item in items_list if item['id'] not in self.used_ids]
        if not available_items:
            empty_item = {key: "" for key in items_list[0].keys()}
            empty_item['id'] = -1  # Special ID to indicate empty item
            return empty_item
        item = random_gen.choice(available_items)
        self.used_ids.add(item['id'])
        return item

    @abstractmethod
    def gen_user_message(self, target_goal: str, distractions: bool, ood: bool):
        pass

    @abstractmethod
    def initialize_timestep(self):
        pass

    @abstractmethod
    def progress_time(self):
        pass

    @abstractmethod
    def handle_tools(self, function_name, function_args) -> str:
        pass