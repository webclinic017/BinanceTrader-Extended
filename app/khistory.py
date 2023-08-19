from binance.client import Client
from binance.enums import *
import csv



def get_khistory(client, TRADE_SYMBOL, TRADE_INTERVAL):

    khistory = client.get_historical_klines(TRADE_SYMBOL, TRADE_INTERVAL, "1 Jan, 2022")

    candles_csv = open("{}_{}_history01".format(TRADE_SYMBOL, TRADE_INTERVAL), "w", newline="")
    khistory_writer = csv.writer(candles_csv, delimiter=",")
    for candle in khistory:
        khistory_writer.writerow(candle)

