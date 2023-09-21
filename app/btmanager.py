import bclient, btrader
from .config import Strategies, Trade_Info


class BTManager():
    # python 3.9 enables to use list[str] instead of List[str] from typing module
    def __init__(self, myClient: bclient.MyClient) -> None:
        self.myClient = myClient
        self.next_trader_id = 0
        self.myTraders = list(btrader.bTrader)
        self.myTraders_info = dict()

        try:
            self.create_traders_from_env()
            self.start_all_traders()
        except Exception as e:
            print(e)



    def create_trader(self, TRADE_SYMBOL: str, TRADE_INTERVAL: str, TRADE_STRAT: str) -> int:
        try:
            self.myTraders.append(btrader.bTrader(trader_id=self.next_trader_id, myClient=self.myClient, TRADE_SYMBOL=TRADE_SYMBOL, TRADE_INTERVAL=TRADE_INTERVAL, strategy_str=TRADE_STRAT))
        
            index = self.next_trader_id #len(self.myTraders) - 1
            self.myTraders_info[str(index)] = dict({
                "TRADE_SYMBOL" : TRADE_SYMBOL,
                "TRADE_INTERVAL" : TRADE_INTERVAL,
                "TRADE_STRAT" : TRADE_STRAT,
                "Running" : False

            })
        except Exception as e:
            print(e)    
        self.next_trader_id += 1

        return index



    def start_trader(self, index: int):
        if self.myTraders[index] is not None:
            self.myTraders[index].start()
            self.myTraders_info[index]["Running"] = True



    def stop_trader(self, index: int):
        if self.myTraders[index] is not None:
            self.myTraders[index].stop()
            self.myTraders_info[index]["Running"] = False


    def create_traders_from_env(self):
        TRADE_SYMBOLS = Trade_Info.TRADE_SYMBOLS
        TRADE_INTERVALS = Trade_Info.TRADE_INTERVALS
        TRADE_STRATS = Trade_Info.TRADE_STRATS
        

        for index, TS in enumerate(TRADE_SYMBOLS):
            if (TRADE_INTERVALS[index] is not None) and (TRADE_STRATS[index] is not None):
                if TRADE_STRATS[index] in Strategies.B_STRATS: # check if trade strategy exists
                    self.create_trader(TRADE_SYMBOL=TS, TRADE_INTERVAL= TRADE_INTERVALS[index], TRADE_STRAT=TRADE_STRATS[index])
            

    def start_all_traders(self):
        #for btindex, btrader in enumerate(self.myTraders):
        #    self.start_trader(btindex)
        for index in range(len(self.myTraders)):
            self.start_trader(index=index)

    
#my_btrader1 = btrader.bTrader(myClient=myClient, TRADE_SYMBOL=config.Trade_Info.TRADE_SYMBOLS[0], TRADE_INTERVAL=config.Trade_Info.TRADE_INTERVALS[0])
#my_btrader2 = btrader.bTrader(myClient=myClient, TRADE_SYMBOL=config.Trade_Info.TRADE_SYMBOLS[1], TRADE_INTERVAL=config.Trade_Info.TRADE_INTERVALS[1])