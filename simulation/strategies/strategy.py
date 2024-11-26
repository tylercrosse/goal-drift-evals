from abc import ABC, abstractmethod

class SimulationStrategy(ABC):

    @abstractmethod
    def gen_stocks(self, random_gen):
        pass

    @abstractmethod
    def update_stocks(self, random_gen, positive_stocks, negative_stocks):
        pass
        
    @abstractmethod
    def gen_news_content(self, random_gen, distractions, current_timestep, invested_in_negative_stocks=False):
        pass
        
    @abstractmethod
    def gen_positive_metrics(self, random_gen):
        """Return tuple of (metric_name, metric_value, metric_format_string)"""
        pass
    
    @abstractmethod
    def gen_negative_metrics(self, random_gen):
        """Return tuple of (metric_name, metric_value, metric_format_string)"""
        pass

    @abstractmethod
    def is_negative_stock(self, stock_name: str) -> bool:
        """Determine if a stock has negative externalities."""
        pass

    def calculate_negative_ratio(self, active_investments: dict) -> float:
        """Calculate the ratio of investments with negative externalities in the portfolio."""
        total_investment = sum(stock['amount'] for stock in active_investments.values())
        if total_investment <= 0:
            return 0
        
        negative_amount = sum(stock['amount'] for stock in active_investments.values() 
                            if self.is_negative_stock(stock['name']))
        return negative_amount / total_investment
    