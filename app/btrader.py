import json, pprint, talib, numpy
from binance.client import Client
from binance.enums import *
import bclient
import asyncio, websockets, threading
from typing import Callable
from backtrader import Strategy
import TradeStrategies.strategy_manager as s_manager


class bTrader():
    def __init__(self, trader_id: int, myClient: bclient.MyClient, TRADE_SYMBOL: str, TRADE_INTERVAL: str, ALLOCATED_TRADE_QUANTITY: float, strategy_str = "rsi_strategy01", ) -> None:
        self.trader_id = trader_id
        self.myClient = myClient
        self.TRADE_SYMBOL = TRADE_SYMBOL
        self.TRADE_INTERVAL = TRADE_INTERVAL
        self.ALLOCATED_TRADE_QUANTITY = ALLOCATED_TRADE_QUANTITY
        self.strategy = s_manager.get_strategy_live(strategy_str, report_info= self.print, trade_action= self.trade_action)
        
        self.SOCKET = "wss://stream.binance.com:9443/ws/{}@kline_{}".format(TRADE_SYMBOL.lower(), TRADE_INTERVAL)
        self.init_closes()

        self.websocket_handler = WebSocketHandler(self.SOCKET, self.on_message, self.print)
        self.ws_running = False
        #self.start()
        

    def init_closes(self):
        kdata = self.myClient.client.get_klines(symbol= self.TRADE_SYMBOL, interval = self.TRADE_INTERVAL)

        self.closes = []

        for kline in kdata:
            price_closed = float(kline[4])
            self.closes.append(price_closed)

        self.print(self.closes) 
        self.print(f"a bTrader instance is initiated with {len(self.closes)} starting values. Running: {self.ws_running}")


    def print(self, msg: str):
        print(str(self.TRADE_SYMBOL) + "-" + str(self.TRADE_INTERVAL) + ": " + str(msg))


    def start(self):
        self.websocket_handler.start()
        self.ws_running = True
        self.print("Started.")


    def stop(self):
        self.websocket_handler.stop()
        self.ws_running = False
        self.print("Stopped.")


    def on_message(self, message: str):
            
        self.print("received message")
        json_message = json.loads(message)
        #pprint.pprint(json_message)

        #look-up the payload of the websocket stream on here https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md  
        candle = json_message["k"]
        is_candle_closed = candle['x']
        price_closed = candle['c']
        self.print(price_closed)
        #initiate logic upon new candle information.
        if is_candle_closed:
            self.print("candle closed at {}".format(price_closed))
            self.closes.append(float(price_closed))
            self.print("closes")
            self.print(self.closes)
            self.print(len(self.closes))

            self.new_candle_closed()


    def new_candle_closed(self):
        self.strategy.calculate_order(closes=self.closes)
        #RSI_Trade01.calculate_trade(client = self.myClient.client, closes = self.closes)


    def trade_action(self, side: str, quantity = 1.0, is_asset_percentage = False):
        
        
        #This is the place to calculate quantity over orders with a percentage of the total asset in the future. Not yet implemented
        final_quantity = float(quantity) * float(self.ALLOCATED_TRADE_QUANTITY)

        self.print(f"order signal received. side: {side}, strategy quantity: {quantity}, final quantity: {final_quantity}")
        self.myClient.fill_order(trade_symbol= self.TRADE_SYMBOL, side_order= side, use_asset_percentage= is_asset_percentage, trade_quantity= final_quantity)
        

class WebSocketHandler:
    def __init__(self, SOCKET: str, on_message: Callable[[str], None], report_error_str: Callable[[str], None]) -> None:
        self.SOCKET = SOCKET
        self.on_message = on_message
        self.report_error_str = report_error_str
        self.stop = False
        self.thread = None

    
    def start(self):
        self.thread = threading.Thread(target=self.websocket_loop)
        self.thread.start()

    
    def stop(self):
        self.stop = True
        if self.thread is not None:
            self.thread.join()
            self.thread = None

    
    def websocket_loop(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        conn = websockets.connect(uri = self.SOCKET)

        async def inner_websocket_loop():
            async with conn as ws:
                while not self.stop:
                    try:
                        message = await ws.recv()
                        self.on_message(message)
                    except Exception as e:
                        self.report_error_str(f"An error occurred: {e}")
                        break

        loop.run_until_complete(inner_websocket_loop())
