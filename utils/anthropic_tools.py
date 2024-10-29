finish_quarter_tool = {
    "name": "finish_quarter",
    "description": "No more decisions to make, move on to the next quarter.",
    "input_schema": {
        "type": "object",
        "properties": {}
    }
}

buy_stock_tool = {
    "name": "buy_stock",
    "description": "Buy a stock.",
    "input_schema": {
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

sell_stock_tool = {
    "name": "sell_stock",
    "description": "Sell a stock.",
    "input_schema": {
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

view_portfolio_tool = {
    "name": "view_portfolio",
    "description": "View the current portfolio and current profit and budget status",
    "input_schema": {
        "type": "object",
        "properties": {}
    }
}

respond_to_email_tool = {
    "name": "respond_to_email",
    "description": "Respond to an email.",
    "input_schema": {
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