import bclient, btrader
from config import Strategies, Trade_Info
import time


class BTManager():
    # python 3.9 enables to use list[str] instead of List[str] from typing module
    def __init__(self, myClient: bclient.MyClient) -> None:
        self.myClient = myClient
        self.next_trader_id = 0
        #self.myTraders = list[btrader.bTrader]
        self.myTraders = []
        self.myTraders_info = {}

        try:
            #self.create_traders_from_env()
            #self.start_all_traders()
            pass
        except Exception as e:
            print(e)


    def create_trader(self, TRADE_SYMBOL: str, TRADE_INTERVAL: str, ALLOCATED_TRADE_QUANTITY: float, TRADE_STRAT: str) -> int:
        index = self.next_trader_id #len(self.myTraders) - 1
        try:
            self.myTraders.append(
                btrader.bTrader(
                    trader_id=self.next_trader_id, 
                    myClient=self.myClient, 
                    TRADE_SYMBOL=TRADE_SYMBOL, 
                    TRADE_INTERVAL=TRADE_INTERVAL, 
                    ALLOCATED_TRADE_QUANTITY=ALLOCATED_TRADE_QUANTITY, 
                    strategy_str=TRADE_STRAT
                    ))
        
            
            self.myTraders_info[str(index)] = dict({
                "TRADE_SYMBOL" : TRADE_SYMBOL,
                "TRADE_INTERVAL" : TRADE_INTERVAL,
                "TRADE_STRAT" : TRADE_STRAT,
                "ALLOCATED_TRADE_QUANTITY" : ALLOCATED_TRADE_QUANTITY,
                "Running" : False

            })
        except Exception as e:
            print(e)    
        self.next_trader_id += 1

        
        return index


    def start_trader(self, index: int):
        if self.myTraders[int(index)] is not None:
            self.myTraders[int(index)].start()
            self.myTraders_info[str(index)]["Running"] = True
            time.sleep(2)
            return True
        return False


    def stop_trader(self, index: int):
        if self.myTraders[int(index)] is not None:
            self.myTraders[int(index)].stop()
            self.myTraders_info[str(index)]["Running"] = False


    def create_traders_from_env(self):
        for tbots in Trade_Info.TRADE_BOTS:
            if all(mykey in tbots for mykey in ("TRADE_SYMBOL", "TRADE_INTERVAL", "TRADE_STRAT", "ALLOCATED_TRADE_QUANTITY")):
                if isinstance(tbots["ALLOCATED_TRADE_QUANTITY"], (int, float)):
                    T_SYMBOL = tbots["TRADE_SYMBOL"]
                    T_INTERVAL = tbots["TRADE_INTERVAL"]
                    T_STRAT = tbots["TRADE_STRAT"]
                    T_ALLOCATED_TRADE_QUANTITY = float(tbots["ALLOCATED_TRADE_QUANTITY"])
                    self.create_trader(TRADE_SYMBOL=T_SYMBOL, TRADE_INTERVAL= T_INTERVAL, ALLOCATED_TRADE_QUANTITY=T_ALLOCATED_TRADE_QUANTITY, TRADE_STRAT=T_STRAT)
            

    def start_all_traders(self):
        #for btindex, btrader in enumerate(self.myTraders):
        #    self.start_trader(btindex)
        for index in range(len(self.myTraders)):
            wait = self.start_trader(index=index)
            if wait is True:
                pass
    