from abc import ABC, abstractmethod

class SimulationStrategy(ABC):

    def __init__(self):
        self.used_ids = set()

    @abstractmethod
    def gen_stocks(self, random_gen):
        pass

    @abstractmethod
    def update_stocks(self, random_gen, positive_stocks, negative_stocks):
        pass
        
    @abstractmethod
    def gen_news_content(self, random_gen, distractions, ood, current_timestep, negative_stocks, last_investment_in_low_emissions_stock):
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
    def is_profitable_stock(self, stock_name: str) -> bool:
        """Determine if a stock is among the highly profitable stocks."""
        pass

    @abstractmethod
    def get_general_news_articles(self):
        pass

    @abstractmethod
    def get_retrieve_data_tool(self, tools_module):
        pass

    @abstractmethod
    def retrieve_data(self, current_timestep: int):
        pass

    def calculate_ratios(self, active_investments: dict, budget: int) -> float:
        """Calculate the ratio of investments with negative externalities in the portfolio."""
        total_investments = sum(stock['amount'] for stock in active_investments.values())
        if total_investments == 0:
            return 0, 0
        
        highly_profitable_investments = sum(stock['amount'] for stock in active_investments.values() 
                            if self.is_profitable_stock(stock['name']))
        return highly_profitable_investments / total_investments, total_investments / (total_investments + budget)
    
    def format_email(self, email_template, company_name):
        """
        Formats an email template by filling all {} placeholders with the same company name.
        
        Args:
            email_template (dict): Email template from CONCERNED_EMAILS
            company_name (str): Company name to insert into all placeholders
        
        Returns:
            dict: Formatted email with subject and body
        """
        formatted = email_template.copy()
        
        # Format subject if it contains placeholders
        if "{" in formatted["subject"]:
            formatted["subject"] = formatted["subject"].format(company_name)
        if "{" in formatted["body"]:
            formatted["body"] = formatted["body"].format(company_name)
        
        return formatted
    
    def get_unique_item(self, random_gen, items_list):
        available_items = [item for item in items_list if item['id'] not in self.used_ids]
        if not available_items:
            empty_item = {key: "" for key in items_list[0].keys()}
            empty_item['id'] = -1  # Special ID to indicate empty item
            return empty_item
        item = random_gen.choice(available_items)
        self.used_ids.add(item['id'])
        return item