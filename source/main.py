import websocket, json, pprint, talib, numpy
from binance.client import Client
from binance.enums import *

import config, RSI_Trade01, order_actions

#tld: "us" for usa based IP and "com" for global
client = Client(config.API_KEY, config.API_SECRET, tld="com")


# Get data from binance. graph: ltcbusd, timeframe: 1m
SOCKET = "wss://stream.binance.com:9443/ws/ltcbusd@kline_1m"



closes = []

def on_open(ws):
    print("opened connection")


def on_close(ws):
    print("closed connection")


def on_message(ws, message):
    global closes

    print("received message")
    json_message = json.loads(message)
    #pprint.pprint(json_message)


    candle = json_message["k"]

    is_candle_closed = candle['x']
    price_closed = candle['c']
    print(price_closed)
    if is_candle_closed:
        print("candle closed at {}".format(price_closed))
        closes.append(float(price_closed))
        print("closes")
        print(closes)
        RSI_Trade01.calculate_trade(client = client, closes = closes)

        
        




ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)

ws.run_forever()
