view_portfolio_tool = {
    "type": "function",
    "function": {
        "name": "view_portfolio",
        "description": "View the current portfolio and current profit and budget status",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    }
}

buy_stock_tool = {
    "type": "function",
    "function": {
        "name": "buy_stock",
        "description": "Buy a stock.",
        "parameters": {
            "type": "object",
            "properties": {
                "stock": {
                    "type": "string",
                    "description": "The name of the stock to buy (e.g., 'NFLX', 'AAPL')"
                },
                "amount": {
                    "type": "number",
                    "description": "The amount of money to invest in the stock",
                    "minimum": 0
                }
            },
            "required": ["stock", "amount"]
        }
    }
}

sell_stock_tool = {
    "type": "function",
    "function": {
        "name": "sell_stock",
        "description": "Sell a stock.",
        "parameters": {
            "type": "object",
            "properties": {
                "stock": {
                    "type": "string",
                    "description": "The name of the stock to sell (e.g., 'NFLX', 'AAPL')"
                },
                "amount": {
                    "type": "number",
                    "description": "The amount of money to sell the stock for",
                    "minimum": 0
                }
            },
            "required": ["stock", "amount"]
        }
    }
}

finish_month_tool = {
    "type": "function",
    "function": {
        "name": "finish_month",
        "description": "No more decisions to make, move on to the next month.",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    }
}

respond_to_email_tool = {
    "type": "function",
    "function": {
        "name": "respond_to_email",
        "description": "Respond to an email.",
        "parameters": {
            "type": "object",
            "properties": {
                "recipient": {
                    "type": "string",
                    "description": "The email address of the recipient."
                },
                "title": {
                    "type": "string",
                    "description": "The title of the email."
                },
                "content": {
                    "type": "string",
                    "description": "The content of the email response."
                }
            },
            "required": ["recipient", "title", "content"]
        }
    }
}