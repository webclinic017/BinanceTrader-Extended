from binance.client import Client
import binance.enums as b_enums
import csv, asyncio
from numpy import genfromtxt



def get_recent_klines(client, TRADE_SYMBOL, TRADE_INTERVAL, delimiter=","):
    recent_khistory = client.get_klines(TRADE_SYMBOL, TRADE_INTERVAL)
    return recent_khistory


#other modules are able to get the name of a csv file 
def get_csv_name(TRADE_SYMBOL, TRADE_INTERVAL):
    return "klineHistory_{}_{}.csv".format(TRADE_SYMBOL, TRADE_INTERVAL)


async def download_khistory(client, TRADE_SYMBOL, TRADE_INTERVAL, DATE_PROMPT_START = "1 Aug, 2023", DATE_PROMPT_END = "now", delimiter=","):

    filename = get_csv_name(TRADE_SYMBOL, TRADE_INTERVAL)
  
    khistory = client.get_historical_klines(TRADE_SYMBOL, TRADE_INTERVAL, DATE_PROMPT_START, DATE_PROMPT_END)


    # candles_csv = open(filename, "w", newline="")
    # khistory_writer = csv.writer(candles_csv, delimiter=",")
    # for candle in khistory:
    #     khistory_writer.writerow(candle)
    
    with open(filename, "w", newline="") as candles_csv:
        khistory_writer = csv.writer(candles_csv, delimiter=",")
        for candle in khistory:
            candle[0] = candle[0] / 1000
            khistory_writer.writerow(candle)
    
    print(filename + " - download completed")
    return True


def get_klineHistory_from_file(TRADE_SYMBOL, TRADE_INTERVAL, delimiter = ","):

    file_name = get_csv_name(TRADE_SYMBOL, TRADE_INTERVAL)
    try:
        data = genfromtxt(file_name, delimiter = delimiter)
    except Exception as e:
        print(e)
        return False
    return data