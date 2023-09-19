import config, bclient, btrader


class BTManager():
    # python 3.9 enables to use list[str] instead of List[str] from typing module
    def __init__(self, myClient: bclient.MyClient, TRADE_SYMBOLS : list[str], TRADE_INTERVALS : list[str]) -> None:
        
        self.TRADE_SYMBOLS = TRADE_SYMBOLS
        self.TRADE_INTERVALS = TRADE_INTERVALS
        self.myTraders = list(btrader.bTrader)
        self.myTraders_index_info = dict()

        try:
            self.create_traders_from_env()
            self.start_all_traders()
        except Exception as e:
            print(e)



    def create_trader(self, TRADE_SYMBOL: str, TRADE_INTERVAL: str) -> int:
        self.myTraders.append(btrader.bTrader(myClient=self.myClient, TRADE_SYMBOL=TRADE_SYMBOL, TRADE_INTERVAL=TRADE_INTERVAL))
        index = len(self.myTraders) - 1
        self.myTraders_index_info[str(index)] = f"{TRADE_SYMBOL}+{TRADE_INTERVAL}+DefaultStrategy1"
        return index


    def start_trader(self, index: int):
        if self.myTraders[index] is not None:
            self.myTraders[index].start()


    def stop_trader(self, index: int):
        if self.myTraders[index] is not None:
            self.myTraders[index].stop()


    def create_traders_from_env(self):
        i = 0
        for ts in self.TRADE_SYMBOLS:
            if self.TRADE_INTERVALS[i] is not None:
                self.create_trader(TRADE_SYMBOL=ts, TRADE_INTERVAL= self.TRADE_INTERVALS[i])
            i += 1

    def start_all_traders(self):
        for bt in self.myTraders:
            bt.start()

    
#my_btrader1 = btrader.bTrader(myClient=myClient, TRADE_SYMBOL=config.Trade_Info.TRADE_SYMBOLS[0], TRADE_INTERVAL=config.Trade_Info.TRADE_INTERVALS[0])
#my_btrader2 = btrader.bTrader(myClient=myClient, TRADE_SYMBOL=config.Trade_Info.TRADE_SYMBOLS[1], TRADE_INTERVAL=config.Trade_Info.TRADE_INTERVALS[1])