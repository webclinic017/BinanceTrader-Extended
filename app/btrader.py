import json, pprint, talib, numpy
from binance.client import Client
from binance.enums import *
import bclient
import asyncio, websockets, threading
from typing import Callable


class bTrader():
    def __init__(self, myClient: bclient.MyClient, TRADE_SYMBOL: str, TRADE_INTERVAL: str) -> None:
        self.myClient = myClient
        self.TRADE_SYMBOL = TRADE_SYMBOL
        self.TRADE_INTERVAL = TRADE_INTERVAL
        
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
        print("this should only triggers only once for every message on this instance")
        #RSI_Trade01.calculate_trade(client = self.myClient.client, closes = self.closes)


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
