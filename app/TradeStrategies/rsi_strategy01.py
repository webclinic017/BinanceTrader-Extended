from typing import Callable
from .bstrategy import bStrategy

import backtrader as bt

from binance.enums import *
import numpy, talib

class Backtest(bt.Strategy):
    def __init__(self):
        self.rsi = bt.talib.RSI(self.data, period=14)


    def next(self):
        if self.rsi < 30 and not self.position:
            self.buy(size=1)
        
        if self.rsi > 70 and self.position:
            self.close()


class Live(bStrategy):
    def __init__(self, report_info: Callable[[str], None], trade_action: Callable[[str, float, bool], None]):
        super().__init__(report_info, trade_action)

        self.RSI_PERIOD = 14
        self.RSI_OVERBOUGHT = 70
        self.RSI_OVERSOLD = 30

        self.in_position = False
        self.price_of_position = 10
        self.sell_if_up = True
        self.sell_if_up_ratio = 1.02

    

    def calculate_order(self, closes):
        self.in_position
        self.price_of_position
        
        self.report_info("Calculating The Market")
        if len(closes) > self.RSI_PERIOD:
            np_closes = numpy.array(closes)
            rsi = talib.RSI(np_closes, self.RSI_PERIOD) #talib.RSI returns multiple RSI values 
            
            self.report_info("all rsis calculated so far")
            self.report_info(rsi)

            last_rsi = rsi[-1]
            self.report_info("the current rsi is {}".format(last_rsi))
            self.report_info("in position: {}".format(self.in_position))
            last_close = closes[-1]

            try:
                #sell current position
                if last_rsi > self.RSI_OVERBOUGHT or (self.in_position and self.sell_if_up and (last_close > self.price_of_position *self.sell_if_up_ratio )):
                    if last_rsi > self.RSI_OVERBOUGHT:
                        self.report_info("in overbought area.")
                    if (last_close > self.price_of_position *self.sell_if_up_ratio and self.sell_if_up ):
                        self.report_info("current profit is above the percentage of {}".format(self.sell_if_up_ratio))
                    self.report_info(self.in_position)
                    if self.in_position:
                        self.report_info("Sell! Sell! Sell!")
                        
                        #order_success =  order_actions.fill_order(client = client, calculated_order= cook_order(SIDE_SELL))
                        order_success = self.trade_action(SIDE_SELL, 1.0, False)
                        if order_success:
                            self.in_position = False
                            self.price_of_position = 10
                        #Binance sell logic
                    else:
                        self.report_info("It is overbough, but I am not in position to sell.")
                    
                #buy new position
                if last_rsi < self.RSI_OVERSOLD:
                    self.report_info("in oversold area.")
                    self.report_info(self.in_position)
                    if self.in_position:
                        self.report_info("it is oversold, but I am already in position.")
                    else:
                        self.report_info("Buy! Buy! Buy!")
                        
                        #order_success = order_actions.fill_order(client = client, calculated_order= cook_order(SIDE_BUY))
                        order_success = self.trade_action(SIDE_BUY, 1.0, False)
                        if order_success:
                            self.in_position = True
                            self.price_of_position = last_close
                        #Binance buy logic
            except Exception as e:
                self.report_info(e)
