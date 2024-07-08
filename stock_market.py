""" Super Simple Stock Market """

from datetime import datetime, timedelta
from env import stock_dict, stock_price, trade_dict

class Stock:
    def __init__(self, data):
        self.symbol = data["symbol"]
        self.type = data["stock_type"] # Can be "common" or "preferred"
        self.last_dividend = data["last_dividend"]
        self.par_value = data["par_value"]
        self.trades = []  # List of past trades
        self.fixed_dividend = data.get("fixed_dividend", 0) # For preferred stocks only

    def dividend_yield(self, price):
        """
            calculate the dividend yield
        """
        if self.type == "common":
            if self.last_dividend is None:
                return None # Handle case where last_dividend is not set
            return self.last_dividend / price
        elif self.type == "preferred":
            if self.par_value is None:
                return None  # Handle case where par_value is not set
            return (self.fixed_dividend * self.par_value) / price  # Assuming fixed_dividend attribute exists
        else:
            raise ValueError("Invalid stock type")  # Handle unexpected stock types

    def pe_ratio(self, price):
        """ 
            calculate the P/E Ratio 
        """
        if self.last_dividend is None or self.last_dividend == 0:
            return None  # Handle cases where last_dividend is zero
        return price / self.last_dividend

    def record_trade(self, data):
        """ 
            Record a trade, with timestamp, quantity, buy or sell indicator and price 
        """
        for each_data in data:
            self.trades.append(
                (
                    each_data["timestamp"],
                    each_data["quantity"],
                    each_data["buy_sell"],
                    each_data["price"])
            )

    def volume_weighted_price(self):
        """ 
            Calculate Volume Weighted Stock Price based on trades in past 5 minutes 
        """
        total_quantity = 0
        total_price = 0
        
        for timestamp, quantity, _, price in self.trades:
            if (datetime.now() - timestamp).total_seconds() <= 300:  # Past 5 minutes
                total_quantity += quantity
                total_price += quantity * price
        if total_quantity == 0:
            return 0
        return total_price / total_quantity


class Market:
    def __init__(self):
        self.stocks = {}

    def add_stock(self, stock):
        self.stocks[stock.symbol] = stock

    def get_stock(self, symbol):
        return self.stocks.get(symbol)

    def all_share_index(self):
        """ 
            Calculate the GBCE All Share Index using the geometric mean 
            of the Volume Weighted Stock Price for all stocks
        """
        prices = []
        for stock in self.stocks.values():
            vw_price = stock.volume_weighted_price()
            if vw_price is not None:
                prices.append(vw_price)
        if not prices:
            return None
        product = 1
        for price in prices:
            product *= price
        return pow(product, 1.0 / len(prices))


# Example Usage
market = Market()

for data in stock_dict:
    stock_obj = Stock(data)
    market.add_stock(stock_obj)

    # Record some trades
    try:
        trade_details = trade_dict[data["symbol"]]
        if trade_details:
            stock_obj.record_trade(trade_details)  # Record a trade, with timestamp, quantity, buy or sell indicator and price
    except KeyError:
        pass

    # Calculate data
    price = stock_price[data["symbol"]]
    dividend_yield = stock_obj.dividend_yield(price)  # Set last_dividend for accurate calculation
    pe_ratio = stock_obj.pe_ratio(price)  # P/E ratio calculation
    vw_price = stock_obj.volume_weighted_price()  # Calculate Volume Weighted Stock Price
    

    print(f"Stock: {stock_obj.symbol}")
    print("*********************")
    print(f"Dividend Yield: {dividend_yield:.2f}")
    print(f"P/E Ratio: {pe_ratio}")
    print(f"Volume Weighted Price: {vw_price:.2f}")
    
all_share_index = market.all_share_index()  # Calculate the GBCE All Share Index
print(f"GBCE All Share Index: {all_share_index:.2f}")
