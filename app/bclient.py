from binance.client import Client
from binance.enums import *

import config, RSI_Trade01, order_actions, khistory


class MyClient():

    def __init__(self, BinanceConfig :config.Binance_Config):
        self.BinanceConfig = BinanceConfig
        #tld: "us" for usa based IP and "com" for global.
        self.client = Client(BinanceConfig.BINANCE_API_KEY, BinanceConfig.BINANCE_API_SECRET, tld="com")

    def printAPI(self):
        print(self.BinanceConfig.BINANCE_API_KEY)