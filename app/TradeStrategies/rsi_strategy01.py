import backtrader as bt
from strategy_manager import bStrategy

class RSIStrategy01(bStrategy):
    def __init__(self):
        super.__init__(self)
        self.rsi = bt.talib.RSI(self.data, period=14)


    def next(self):
        if self.rsi < 30 and not self.position:
            self.buy(size=1)
        
        if self.rsi > 70 and self.position:
            self.close()


    def update_data(self, new_close):
        self.data.append(new_close)
        #trigger next

    
    def set_data(self, data):
        self.data = data