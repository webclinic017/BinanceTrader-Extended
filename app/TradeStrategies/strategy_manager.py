import backtrader as bt
#from TradeStrategies import *
from TradeStrategies.bstrategy import bStrategy
import TradeStrategies.rsi_strategy01 as rsi_strategy01

from typing import Callable
#from bclient import MyClient
from config import Strategies 




def get_strategy_bt(strategy_str: str) -> bt.Strategy:
    sclass = rsi_strategy01.Backtest
    if strategy_str == Strategies.B_STRATS[0]: #"rsi_strategy01"
        sclass = rsi_strategy01.Backtest
    #other strategies will go here with an if block
    return sclass


def get_strategy_live(strategy_str: str, report_info: Callable[[str, str], None], trade_action: Callable[[str], None]) -> bStrategy:
    my_ts = rsi_strategy01.Live(report_info=report_info, trade_action=trade_action)
    if strategy_str == Strategies.B_STRATS[0]: #"rsi_strategy01"
        my_ts = rsi_strategy01.Live(report_info=report_info, trade_action=trade_action)
    #other strategies will go here with an if block    
    return my_ts