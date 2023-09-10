

def process_klineslist_to_chartdictformat(klines_list):
    processed_klines = []
    for kline in klines_list:
        #input kline format [
        # 1691700600000,
        # "82.90000000",
        # "82.95000000",
        # "82.87000000",
        # "82.94000000",
        # "870.92400000",
        # 1691700899999,
        # "72212.66620000",
        # 163,
        # "687.88300000",
        # "57039.32777000",
        # "0"
        # ],
        # lightweight charts format
        #{ time: '2018-10-19', open: 180.34, high: 180.99, low: 178.57, close: 179.85 },
        #{ time: '2018-10-22', open: 180.82, high: 181.40, low: 177.56, close: 178.75 },
        new_kline = { "time": kline[0] / 1000, #remove miliseconds in unix timestamp sent from binance stream
                     "open": kline[1], 
                     "high": kline[2], 
                     "low": kline[3], 
                     "close": kline[4] 
                     }
        processed_klines.append(new_kline)

    return processed_klines