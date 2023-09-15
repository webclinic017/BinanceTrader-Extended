from binance.client import Client
from binance.enums import *

import config, RSI_Trade01, order_actions, khistory, backtest


class MyClient():

    def __init__(self, BinanceConfig :config.Binance_Config):
        self.BinanceConfig = BinanceConfig
        #tld: "us" for usa based IP and "com" for global.
        self.client = Client(BinanceConfig.BINANCE_API_KEY, BinanceConfig.BINANCE_API_SECRET, tld="com")


    def printAPI(self):
        print(self.BinanceConfig.BINANCE_API_KEY)


    def fill_order(self, trade_symbol : str, side_order : str, use_trade_percentage : str, trade_quantity : float, order_type=ORDER_TYPE_MARKET):
        
        
        try:
            print("use custom trade percentage: {}.".format(use_trade_percentage))
            if use_trade_percentage == "N":
                print("sending order. {}, {}, {}, {}, {}".format(trade_symbol, side_order, use_trade_percentage, trade_quantity, order_type))
                order = self.client.create_order(symbol = trade_symbol, side=side_order, type=order_type, quantity = trade_quantity)
                print(order)

            if use_trade_percentage == "Y":
                print("custom trade percentage is not defined yet")
                pass #get total amount of currency and make %90 quantity
        except Exception as e:
            print(e)
            return e
        
        return True