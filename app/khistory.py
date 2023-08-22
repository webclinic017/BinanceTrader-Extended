from binance.client import Client
from binance.enums import *
import csv
from numpy import genfromtxt


def get_recent_klines(client, TRADE_SYMBOL, TRADE_INTERVAL, delimiter=","):
    recent_khistory = client.get_klines(TRADE_SYMBOL, TRADE_INTERVAL)
    return recent_khistory



def download_khistory(client, TRADE_SYMBOL, TRADE_INTERVAL, delimiter=","):

    filename = "klineHistory_{}_{}.csv".format(TRADE_SYMBOL, TRADE_INTERVAL)
  

    khistory = client.get_historical_klines(TRADE_SYMBOL, TRADE_INTERVAL, "1 Aug, 2023")


    # candles_csv = open(filename, "w", newline="")
    # khistory_writer = csv.writer(candles_csv, delimiter=",")
    # for candle in khistory:
    #     khistory_writer.writerow(candle)
    
    with open(filename, "w", newline="") as candles_csv:
        khistory_writer = csv.writer(candles_csv, delimiter=",")
        for candle in khistory:
            khistory_writer.writerow(candle)



def get_klineHistory_from_file(TRADE_SYMBOL, TRADE_INTERVAL, delimiter = ","):

    file_name = "klineHistory_{}_{}.csv".format(TRADE_SYMBOL, TRADE_INTERVAL)
    try:
        data = genfromtxt(file_name, delimiter = delimiter)
    except Exception as e:
        print(e)
        return False
    return data