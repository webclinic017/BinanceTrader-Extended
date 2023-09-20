import backtrader as bt
from TradeStrategies import *
import TradeStrategies.rsi_strategy01 as rsi_strategy01
from typing import Callable


class bStrategy(bt.Strategy):
    def __init__(self, b_buy_signal: Callable[[], None], b_close_signal: Callable[[], None], b_backtest = False):
        self.b_backtest = b_backtest
        self.b_buy_signal = b_buy_signal
        self.b_close_signal = b_close_signal
    #     self.rsi = bt.talib.RSI(self.data, period=14)


    # def next(self):
    #     if self.rsi < 30 and not self.position:
    #         self.buy(size=1)
        
    #     if self.rsi > 70 and self.position:
    #         self.close()


    def b_update_data(self, new_close):
        self.data.append(new_close)
        #trigger next

    
    def b_set_data(self, data):
        self.data = data
        

def get_strategy(strategy_str: str, b_backtest = False) -> bStrategy:
    if strategy_str == "rsi_strategy01":
        my_ts = rsi_strategy01.RSIStrategy01(b_backtest = b_backtest)
    #other strategies goes here with an elif block
    else:
        my_ts = rsi_strategy01.RSIStrategy01(b_backtest = b_backtest)

    return my_ts

