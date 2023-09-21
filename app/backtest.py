import backtrader as bt
import TradeStrategies.strategy_manager as sm
#import Matplotlib



def run1(csv_name: str, TRADE_INTERVAL: str, strategy_str = "rsi_strategy01"):
    data_compression :int
    data_timeframestr :str
    data_timeframe = bt.TimeFrame.Minutes
    for index, letter in enumerate(TRADE_INTERVAL, 0):
        if not letter.isdigit():
            data_compression = int(TRADE_INTERVAL[:index])
            data_timeframestr = str(TRADE_INTERVAL[index:])
    
    if data_timeframestr == "s":
        data_timeframe = bt.TimeFrame.Seconds
    elif data_timeframestr == "m":
        data_timeframe = bt.TimeFrame.Minutes
    elif data_timeframestr == "d":
        data_timeframe = bt.TimeFrame.Days
    elif data_timeframestr == "w":
        data_timeframe = bt.TimeFrame.Weeks
    elif data_timeframestr == "M":
        data_timeframe = bt.TimeFrame.Months

    cerebro = bt.Cerebro()
    data = bt.feeds.GenericCSVData(dataname = csv_name, dtformat = 2, compression = data_compression, timeframe = data_timeframe)
    cerebro.adddata(data)
    #print(type(sm.get_strategy_bt(strategy_str=strategy_str)))
    cerebro.addstrategy(sm.get_strategy_bt(strategy_str=strategy_str))

    cerebro.run()
    cerebro.plot()