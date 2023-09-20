from typing import Callable
import backtrader as bt
from strategy_manager import bStrategy

class Backtest(bt.Strategy):
    def __init__(self):
        self.rsi = bt.talib.RSI(self.data, period=14)


    def next(self):
        if self.rsi < 30 and not self.position:
            self.buy(size=1)
        
        if self.rsi > 70 and self.position:
            self.close()


class Live(bStrategy):
    def __init__(self, report_info: Callable[[str], None], trade_action: Callable[[str], None]):
        super().__init__(report_info, trade_action)
    pass