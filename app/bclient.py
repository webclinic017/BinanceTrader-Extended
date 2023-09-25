from binance.client import Client
from binance.enums import *

import config, log_handler



class MyClient():

    def __init__(self, BinanceConfig :config.Binance_Config):
        self.BinanceConfig = BinanceConfig
        self.myLogHandler = log_handler.myLogHandler

        self.client = Client(BinanceConfig.BINANCE_API_KEY, BinanceConfig.BINANCE_API_SECRET, tld=BinanceConfig.BINANCE_CLIENT_TLD)
        
        #self.client.get_account()

        #self.logs = []
        try:
           self.client.get_account()
        except Exception as e:
           self.myLogHandler.add_bclient_log(f"Binance Client Error: {e}")
           #self.logs.append(f"API Error: {e}")
           raise ValueError('Manually thrown exception.')

    def printAPI(self):
        print(self.BinanceConfig.BINANCE_API_KEY)


    def fill_order(self, trade_symbol : str, side_order : str, use_asset_percentage : bool, trade_quantity : float, order_type=ORDER_TYPE_MARKET):
        
        try:
            print("use custom trade percentage: {}.".format(use_asset_percentage))
            if use_asset_percentage == False:
                print("sending order. {}, {}, {}, {}, {}".format(trade_symbol, side_order, use_asset_percentage, trade_quantity, order_type))
                order = self.client.create_order(symbol = trade_symbol, side=side_order, type=order_type, quantity = trade_quantity)
                print(order)

            if use_asset_percentage == True:
                print("custom trade percentage is not defined yet")
                pass #get total amount of currency and make %90 quantity
        except Exception as e:
            print(e)
            return e
        
        return True