import websocket, json, pprint, talib, numpy
from binance.client import Client
from binance.enums import *
import csv

import config, RSI_Trade01, order_actions, khistory

import asyncio, websockets


#async def create_and_start_btrader(myClient, TRADE_SYMBOL, TRADE_INTERVAL):
#    btrader = bTrader(myClient, TRADE_SYMBOL, TRADE_INTERVAL)
#    asyncio.create_task(btrader.start_websocket())


class bTrader():

    async def the_task(self):
        asyncio.create_task(self.start_websocket())


    def __init__(self, myClient, TRADE_SYMBOL, TRADE_INTERVAL):
        self.myClient = myClient
        self.TRADE_SYMBOL = TRADE_SYMBOL
        self.TRADE_INTERVAL = TRADE_INTERVAL
        
        self.SOCKET = "wss://stream.binance.com:9443/ws/{}@kline_{}".format(TRADE_SYMBOL.lower(), TRADE_INTERVAL)
        self.init_closes()
        asyncio.run(self.the_task())
        
        

    def init_closes(self):
        kdata = self.myClient.client.get_klines(symbol= self.TRADE_SYMBOL, interval = self.TRADE_INTERVAL)

        self.closes = []

        for kline in kdata:
            price_closed = float(kline[4])
            self.closes.append(price_closed)

        self.print(self.closes) 
        self.print("a bTrader instance is initiated with {} starting values.".format(len(self.closes)))

    def print(self, msg : str):
        print(str(self.TRADE_SYMBOL) + str(self.TRADE_INTERVAL) + str(msg))


    async def start_websocket(self):
        

        def on_open(ws):
            print("opened connection")


        def on_close(ws):
            print("closed connection")


        def on_message(ws, message):
            
            #global np_closes

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
                print("closes")
                self.print(self.closes)
                print(len(self.closes))

                self.new_candle_closed()

        #Get updates from socket.
        #ws = websocket.WebSocketApp(self.SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
        #ws.run_forever()

        # https://betterprogramming.pub/websockets-and-asyncio-beyond-5-line-samples-part-1-ddf8699a18ce
        conn = websockets.connect(uri= self.SOCKET)

        async with conn as ws: 
            while True:
                message = await ws.recv()
                self.print(message)


    def new_candle_closed(self):

        pass
        #RSI_Trade01.calculate_trade(client = self.myClient.client, closes = self.closes)