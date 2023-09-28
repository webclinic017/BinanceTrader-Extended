from typing import Callable


class bStrategy():
    def __init__(self, report_info: Callable[[str, str], None] , trade_action: Callable[[str, float, bool], None]):
        self.trade_action = trade_action
        self.report_info = report_info
    #     self.rsi = bt.talib.RSI(self.data, period=14)


    def process_candles(self, candles, calculate_order: bool):
        # look-up the payload of the websocket stream on here https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md 
        # Payload: 
        # {
        #     "t": 1672515780000, // Kline start time
        #     "T": 1672515839999, // Kline close time
        #     "s": "BNBBTC",      // Symbol
        #     "i": "1m",          // Interval
        #     "f": 100,           // First trade ID
        #     "L": 200,           // Last trade ID
        #     "o": "0.0010",      // Open price
        #     "c": "0.0020",      // Close price
        #     "h": "0.0025",      // High price
        #     "l": "0.0015",      // Low price
        #     "v": "1000",        // Base asset volume
        #     "n": 100,           // Number of trades
        #     "x": false,         // Is this kline closed?
        #     "q": "1.0000",      // Quote asset volume
        #     "V": "500",         // Taker buy base asset volume
        #     "Q": "0.500",       // Taker buy quote asset volume
        #     "B": "123456"       // Ignore
        # }
    
        # BE CAREFUL OF HOW THESE DATA TYPES ARE STRINGS
        self.report_info("default process_candles function of bStrategy.")
        if calculate_order:
            self.calculate_order()


    def calculate_order(self):
        self.report_info("default calculate_order function of bStrategy.")
        
