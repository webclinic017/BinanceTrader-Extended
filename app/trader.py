import websocket, json, pprint, talib, numpy
from binance.client import Client
from binance.enums import *
import csv
import backtrader as bt

import config, RSI_Trade01, order_actions, khistory

#tld: "us" for usa based IP and "com" for global.
client = Client(config.Binance_Config.BINANCE_API_KEY, config.Binance_Config.BINANCE_API_SECRET, tld="com")

TRADE_SYMBOL = config.TRADE_SYMBOLS[0].upper()
TRADE_INTERVAL = KLINE_INTERVAL_1MINUTE

# Get data from binance. graph: "ltcbusd"(change this in config.), timeframe: 1m
SOCKET = "wss://stream.binance.com:9443/ws/{}@kline_{}".format(TRADE_SYMBOL.lower(), TRADE_INTERVAL)


use_only_recent = True
#candles_recent = client.get_klines(symbol = TRADE_SYMBOL, interval = TRADE_INTERVAL)

# candles_csv = open("{}_{}_recent".format(TRADE_SYMBOL, TRADE_INTERVAL), "w", newline="")

# candles_writer = csv.writer(candles_csv, delimiter=",")
# for candle in candles_recent:
#     candles_writer.writerow(candle)


if not use_only_recent:

    khistory.download_khistory(client, TRADE_SYMBOL, TRADE_INTERVAL)

    kdata = khistory.get_klineHistory_from_file(TRADE_SYMBOL, TRADE_INTERVAL)

    try:
        kcloses = kdata[:,4]
        kcloses = kcloses.tolist()
    except Exception as e:
        print(e)
        kcloses = []

else:

    kdata = client.get_klines(symbol= TRADE_SYMBOL, interval = TRADE_INTERVAL)

    kcloses = []

    for kline in kdata:
        price_closed = float(kline[4])
        kcloses.append(price_closed)
    

print(kcloses)


#this is the array for storing closed candle values gathered from socket and file.
closes = []
closes = kcloses
print(len(closes))



def on_open(ws):
    print("opened connection")


def on_close(ws):
    print("closed connection")


def on_message(ws, message):
    global closes
    global np_closes

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
        print(len(closes))
        RSI_Trade01.calculate_trade(client = client, closes = closes)






#Get updates from socket.
ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)

ws.run_forever()
