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

#https://www.phind.com/agent?cache=cln24mifl0000jr08lmp3skqr
class Live(bStrategy):
    def __init__(self, report_info: Callable[[str, str], None], trade_action: Callable[[str, float, bool], bool]):
        super().__init__(report_info, trade_action)

        self.RSI_PERIOD = 14
        self.RSI_OVERBOUGHT = 70
        self.SMA_SHORT = 8
        self.SMA_LONG = 21
        self.VOLUME_PERIOD = 45

        self.in_position = False
        self.price_of_position = 10
        self.sell_if_up = True
        self.sell_if_up_ratio = 1.02

    def calculate_order(self, closes, volumes):
        self.in_position
        self.price_of_position
        
        self.report_info("Calculating The Market")
        if len(closes) > self.RSI_PERIOD:
            np_closes = numpy.array(closes)
            np_volumes = numpy.array(volumes)
            rsi = talib.RSI(np_closes, self.RSI_PERIOD)
            sma_short = talib.SMA(np_closes, self.SMA_SHORT)
            sma_long = talib.SMA(np_closes, self.SMA_LONG)
            avg_volume = talib.SMA(np_volumes, self.VOLUME_PERIOD)

            last_rsi = rsi[-1]
            last_sma_short = sma_short[-1]
            last_sma_long = sma_long[-1]
            last_volume = volumes[-1]
            last_avg_volume = avg_volume[-1]
            last_close = closes[-1]

            try:
                #sell current position
                if last_sma_short < last_sma_long:
                    self.report_info("SMA 8 crossed SMA 21 downwards.")
                    if self.in_position:
                        self.report_info("Sell! Sell! Sell!")
                        order_success = self.trade_action(SIDE_SELL, 1.0, False)
                        if order_success:
                            self.in_position = False
                            self.price_of_position = 10
                    else:
                        self.report_info("SMA 8 crossed SMA 21 downwards, but I am not in position to sell.")
                    
                #buy new position
                if last_rsi > self.RSI_OVERBOUGHT and last_sma_short > last_sma_long and last_volume > last_avg_volume:
                    self.report_info("RSI is over 70, SMA 8 crossed SMA 21 upwards, and volume is above average.")
                    if self.in_position:
                        self.report_info("Conditions met, but I am already in position.")
                    else:
                        self.report_info("Buy! Buy! Buy!")
                        order_success = self.trade_action(SIDE_BUY, 1.0, False)
                        if order_success:
                            self.in_position = True
                            self.price_of_position = last_close
            except Exception as e:
                self.report_info(e)

