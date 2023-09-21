import backtrader as bt
from TradeStrategies import *
import TradeStrategies.rsi_strategy01 as rsi_strategy01
from typing import Callable
from bclient import MyClient
from ..config import Strategies 



class bStrategy():
    def __init__(self, report_info: Callable[[str], None] , trade_action: Callable[[str, float, bool], None]):
        self.trade_action = trade_action
        self.report_info = report_info
    #     self.rsi = bt.talib.RSI(self.data, period=14)

    def calculate_order(self, closes):
        self.report_info("default calculate_order function of bStrategy.")
        

def get_strategy_bt(strategy_str: str) -> bt.Strategy:
    my_ts = rsi_strategy01.Backtest()
    if strategy_str == Strategies.B_STRATS[0]: #"rsi_strategy01"
        my_ts = rsi_strategy01.Backtest()
    #other strategies goes here with an if block
    return my_ts


def get_strategy_live(strategy_str: str, report_info: Callable[[str], None], trade_action: Callable[[str], None]) -> bStrategy:
    my_ts = rsi_strategy01.Live(report_info=report_info, trade_action=trade_action)
    if strategy_str == Strategies.B_STRATS[0]: #"rsi_strategy01"
        my_ts = rsi_strategy01.Live(report_info=report_info, trade_action=trade_action)
    #other strategies goes here with an if block    
    return my_ts