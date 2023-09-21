from typing import Callable


class bStrategy():
    def __init__(self, report_info: Callable[[str], None] , trade_action: Callable[[str, float, bool], None]):
        self.trade_action = trade_action
        self.report_info = report_info
    #     self.rsi = bt.talib.RSI(self.data, period=14)

    def calculate_order(self, closes):
        self.report_info("default calculate_order function of bStrategy.")
        
