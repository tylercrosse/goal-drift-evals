from typing import Dict, Any
from strategies.strategy import SimulationStrategy

class Simulation:

    def __init__(self, strategy: SimulationStrategy, run: int, model: str, prev_sim_data: Dict[str, Any] = {}):
        self.run = run
        self.model = model
        self.strategy = strategy

        print(f"Prev sim data: {prev_sim_data}")

        self.budget_low = prev_sim_data.get("budget_low", 8000)
        self.budget_high = prev_sim_data.get("budget_high", 12000)
        self.budget = prev_sim_data.get("budget", 0)
        self.portfolio_value = prev_sim_data.get("portfolio_value", 0)
        self.profit = prev_sim_data.get("profit", 0)
        self.year = prev_sim_data.get("year", 2025)
        self.current_timestep = prev_sim_data.get("current_timestep", 1)
        self.positive_stocks = prev_sim_data.get("positive_stocks", [])
        self.negative_stocks = prev_sim_data.get("negative_stocks", [])
        self.do_nothing_baseline = prev_sim_data.get("do_nothing_baseline", 0)
        self.intermediate_profits = prev_sim_data.get("intermediate_profits", [])
        self.intermediate_emissions = prev_sim_data.get("intermediate_emissions", [])
        self.active_investments = prev_sim_data.get("active_investments", {})
        self.budget_limit_errors = prev_sim_data.get("budget_limit_errors", 0)
        self.tool_call_errors = prev_sim_data.get("tool_call_errors", 0)
        self.investments_in_positive_stocks = prev_sim_data.get("investments_in_positive_stocks", 0)
        self.investments_in_negative_stocks = prev_sim_data.get("investments_in_negative_stocks", 0)
        self.invested_in_negative_stocks = prev_sim_data.get("invested_in_negative_stocks", False)
        self.investments_made = prev_sim_data.get("investments_made", 0)
        self.best_option_chosen = prev_sim_data.get("best_option_chosen", 0)


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
            "positive_stocks": self.positive_stocks,
            "negative_stocks": self.negative_stocks,
            "do_nothing_baseline": self.do_nothing_baseline,
            "intermediate_profits": self.intermediate_profits,
            "intermediate_emissions": self.intermediate_emissions,
            "active_investments": self.active_investments,
            "budget_limit_errors": self.budget_limit_errors,
            "tool_call_errors": self.tool_call_errors,
            "investments_in_positive_stocks": self.investments_in_positive_stocks,
            "investments_in_negative_stocks": self.investments_in_negative_stocks,
            "invested_in_negative_stocks": self.invested_in_negative_stocks,
            "investments_made": self.investments_made,
            "best_option_chosen": self.best_option_chosen,
        }