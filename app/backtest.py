import backtrader as bt
import strategy_manager as sm
#import Matplotlib


class Backtester():
    def __init__(self) -> None:
        pass


    def run1(self, csv_name: str, TRADE_INTERVAL: str, strategy_str = "rsi_strategy01"):
        data_compression :int
        data_timeframestr :str
        data_timeframe = bt.TimeFrame.Minutes       # type: ignore
        for index, letter in enumerate(TRADE_INTERVAL, 0):
            if not letter.isdigit():
                data_compression = int(TRADE_INTERVAL[:index])
                data_timeframestr = str(TRADE_INTERVAL[index:])
        
        if data_timeframestr == "s":                    # type: ignore
            data_timeframe = bt.TimeFrame.Seconds       # type: ignore
        elif data_timeframestr == "m":                  # type: ignore
            data_timeframe = bt.TimeFrame.Minutes       # type: ignore
        elif data_timeframestr == "h":                  # type: ignore
            data_timeframe = bt.TimeFrame.Minutes       # type: ignore
            data_compression = data_compression * 60    # type: ignore
        elif data_timeframestr == "d":                  # type: ignore
            data_timeframe = bt.TimeFrame.Days          # type: ignore
        elif data_timeframestr == "w":                  # type: ignore
            data_timeframe = bt.TimeFrame.Weeks         # type: ignore
        elif data_timeframestr == "M":                  # type: ignore
            data_timeframe = bt.TimeFrame.Months        # type: ignore

        cerebro = bt.Cerebro()
        data = bt.feeds.GenericCSVData(dataname = csv_name, dtformat = 2, compression = data_compression, timeframe = data_timeframe) # type: ignore
        cerebro.adddata(data)
        #print(type(sm.get_strategy_bt(strategy_str=strategy_str)))
        cerebro.addstrategy(sm.get_strategy_bt(strategy_str=strategy_str))

        cerebro.run()
        cerebro.plot()


myBacktester = Backtester()