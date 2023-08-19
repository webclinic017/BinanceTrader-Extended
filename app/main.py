import websocket, json, pprint, talib, numpy
from binance.client import Client
from binance.enums import *
import csv

import config, RSI_Trade01, order_actions, khistory

#tld: "us" for usa based IP and "com" for global.
client = Client(config.API_KEY, config.API_SECRET, tld="com")

TRADE_SYMBOL = config.TRADE_SYMBOL.upper()
TRADE_INTERVAL = KLINE_INTERVAL_1MINUTE

# Get data from binance. graph: "ltcbusd"(change this in config.), timeframe: 1m
SOCKET = "wss://stream.binance.com:9443/ws/{}@kline_{}".format(TRADE_SYMBOL.lower(), TRADE_INTERVAL)

#candles_recent = client.get_klines(symbol = TRADE_SYMBOL, interval = TRADE_INTERVAL)

# candles_csv = open("{}_{}_recent".format(TRADE_SYMBOL, TRADE_INTERVAL), "w", newline="")

# candles_writer = csv.writer(candles_csv, delimiter=",")
# for candle in candles_recent:
#     candles_writer.writerow(candle)

khistory.get_khistory(client, TRADE_SYMBOL, TRADE_INTERVAL)

#this is the array for storing closed candle values gathered from socket.
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

    #look-up the payload of the websocket stream on here https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md  
    candle = json_message["k"]

    is_candle_closed = candle['x']
    price_closed = candle['c']
    print(price_closed)
    #initiate logic upon new candle information.
    if is_candle_closed:
        print("candle closed at {}".format(price_closed))
        closes.append(float(price_closed))
        print("closes")
        print(closes)
        RSI_Trade01.calculate_trade(client = client, closes = closes)






#Get updates from socket.
ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)

ws.run_forever()
