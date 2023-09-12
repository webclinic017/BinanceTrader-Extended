import backtrader as bt
#import Matplotlib

class RSIStrategy(bt.Strategy):

    def __init__(self):
        self.rsi = bt.talib.RSI(self.data, period=14)

    def next(self):
        if self.rsi < 30 and not self.position:
            self.buy(size=1)
        
        if self.rsi > 70 and self.position:
            self.close()

def run1(csv_name):
    cerebro = bt.Cerebro()
    data = bt.feeds.GenericCSVData(dataname = csv_name, dtformat = 2)
    cerebro.adddata(data)

    cerebro.addstrategy(RSIStrategy)

    cerebro.run()
    cerebro.plot()