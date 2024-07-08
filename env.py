""" Environment variable for Stock Market """

from datetime import datetime, timedelta

# Sample data from the Global Beverage Corporation Exchange
stock_dict = [
    {"symbol": "TEA", "stock_type": "common", "last_dividend": 0, "par_value": 100},
    {"symbol": "POP", "stock_type": "common", "last_dividend": 8, "par_value": 100},
    {"symbol": "ALE", "stock_type": "common", "last_dividend": 23, "par_value": 60},
    {"symbol": "GIN", "stock_type": "preferred", "last_dividend": 0, "par_value": 100, "fixed_dividend":2} # Preferred stock example
]

# Declare stock price
stock_price = {
    "TEA": 40,
    "POP": 10,
    "ALE": 20,
    "GIN": 30
}

# stock trade details
trade_dict = {
    "TEA":
    [
        {"timestamp": datetime.now(), "quantity": 100, "buy_sell": "buy", "price": 100},
        {"timestamp": (datetime.now() - timedelta(minutes=4)), "quantity": 80, "buy_sell": "sell", "price": 120}
    ],
    "POP":
    [
        {"timestamp": datetime.now(), "quantity": 100, "buy_sell": "buy", "price": 90},
    ],
    "ALE":
    [
        {"timestamp": datetime.now(), "quantity": 100, "buy_sell": "buy", "price": 60},
    ],
    "GIN":
    [
        {"timestamp": datetime.now(), "quantity": 100, "buy_sell": "buy", "price": 80}
    ]
}
