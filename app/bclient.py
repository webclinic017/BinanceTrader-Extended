from binance.client import Client
from binance.enums import ORDER_TYPE_MARKET
from typing import Tuple
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
           self.myLogHandler.add_bclient_log(msg= f"Binance Client Error: {e}", level="critical")
           #self.logs.append(f"API Error: {e}")
           raise ValueError('Manually thrown exception.')

    def printAPI(self):
        print(self.BinanceConfig.BINANCE_API_KEY)


    def fill_order(self, trade_symbol : str, side_order : str, use_asset_percentage : bool, trade_quantity : float, order_type=ORDER_TYPE_MARKET, report_str = log_handler.myLogHandler.add_bclient_log) -> Tuple[bool,str]:
        
        try:
            report_str("use custom trade percentage: {}.".format(use_asset_percentage), level= "order")
            if use_asset_percentage == False:
                report_str("sending order. {}, {}, {}, {}, {}".format(trade_symbol, side_order, use_asset_percentage, trade_quantity, order_type), level= "order")
                order = self.client.create_order(symbol = trade_symbol, side=side_order, type=order_type, quantity = trade_quantity)
                report_str(f"Order: {str(order)}", level= "order")

            if use_asset_percentage == True:
                report_str("custom trade percentage is not defined yet", level= "order")
                pass #get total amount of currency and make %90 quantity
        except Exception as e:
            report_str(f"Client.fill_order error: {str(e)}", level= "critical")
            return (False, str(e))
        
        return (True, "")