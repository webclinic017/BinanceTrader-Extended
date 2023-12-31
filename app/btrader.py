import json, pprint, talib, numpy
from binance.client import Client
import binance.enums as b_enums
import bclient, log_handler
import asyncio, websockets, threading
from typing import Callable
from backtrader import Strategy
import strategy_manager as s_manager
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor


class bTrader():
    def __init__(self, trader_id: int, myClient: bclient.MyClient, TRADE_SYMBOL: str, TRADE_INTERVAL: str, ALLOCATED_TRADE_QUANTITY: float, strategy_str = "rsi_strategy01", ) -> None:
        self.trader_id = trader_id
        self.myClient = myClient
        self.TRADE_SYMBOL = TRADE_SYMBOL
        self.TRADE_INTERVAL = TRADE_INTERVAL
        self.ALLOCATED_TRADE_QUANTITY = ALLOCATED_TRADE_QUANTITY

        self.candle_limit = 200
        self.executor1 = ThreadPoolExecutor(max_workers=1)

        self.strategy = s_manager.get_strategy_live(strategy_str, report_info= self.print, trade_action= self.trade_action)

        self.ws_running = False
        self.SOCKET = "wss://stream.binance.com:9443/ws/{}@kline_{}".format(TRADE_SYMBOL.lower(), TRADE_INTERVAL)
        self.init_closes()

        
        self.websocket_handler = WebSocketHandler(self.SOCKET, self.on_message, self.print)
        
        #self.start()
    

    def init_closes(self):
        kdata = self.myClient.client.get_klines(symbol= self.TRADE_SYMBOL, interval = self.TRADE_INTERVAL)
        kdata = kdata[-self.candle_limit:]

        self.candles = convert_to_dicts(kdata)
        
        #for candle in self.candles:
        #    self.strategy.process_candles(candles=self.candles, calculate_order=False)
        

        self.print(f"a bTrader instance is initiated with {len(self.candles)} starting values. Running: {self.ws_running}", level="setting")


    def print(self, msg: str, level = "info"):
        current_time = datetime.now().strftime("%d/%m/%y %H:%M:%S")
        text1 = f"-{current_time} {level}  bTrader: {str(self.trader_id)}-{str(self.TRADE_SYMBOL)}-{str(self.TRADE_INTERVAL)}: {str(msg)}"
        
        log_handler.myLogHandler.add_btrader_log(btrader_id= self.trader_id, level=level, msg=text1)
        


    def get_logs_info(self) -> list:
        return log_handler.myLogHandler.get_btrader_logs_info(self.trader_id)
    

    def get_logs_special(self) -> list:
        return log_handler.myLogHandler.get_btrader_logs_special(self.trader_id)


    def start(self):
        if self.ws_running is False:
            self.websocket_handler.start()
            self.ws_running = True
            self.print("Started.", level="setting")


    def stop(self):
        if self.ws_running is True:
            self.websocket_handler.stop()
            self.ws_running = False
            self.print("Stopped.", level="setting")


    def on_message(self, message: str):
            
        self.print("received message")
        json_message = json.loads(message)
        
        #look-up the payload of the websocket stream on here https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md  
        candle = json_message["k"]
        is_candle_closed = candle['x']
        price_closed = candle['c']
        self.print(price_closed)
        #initiate logic upon new candle information.
        if is_candle_closed:
            self.print("candle closed at {}".format(price_closed))
            #self.closes.append(float(price_closed))
            #self.closes = self.closes[-200:] # keep the list to 200 elements
            #self.print("closes")
            #self.print(self.closes)
            #self.print(len(self.closes))
            self.new_candle_closed(candle)


    def new_candle_closed(self, candle):
        self.candles.append(candle)
        self.candles = self.candles[-self.candle_limit:]

        
        self.executor1.submit(self.strategy.process_candles, candles=self.candles, calculate_order=True)
        #self.strategy.process_candle(candle=candle, calculate_order=True)
        #self.strategy.calculate_order(closes=self.closes)
        #RSI_Trade01.calculate_trade(client = self.myClient.client, closes = self.closes)


    def trade_action(self, side: str, quantity = 1.0, is_asset_percentage = False) -> bool:
        
        
        #This is the place to calculate quantity over orders with a percentage of the total asset in the future. Not yet implemented
        final_quantity = float(quantity) * float(self.ALLOCATED_TRADE_QUANTITY)

        self.print(f"order signal received. side: {side}, strategy quantity: {quantity}, final quantity: {final_quantity}", "order")
        order_success, msg = self.myClient.fill_order(trade_symbol= self.TRADE_SYMBOL, side_order= side, use_asset_percentage= is_asset_percentage, trade_quantity= final_quantity, report_str=self.print)
        return order_success
        

class WebSocketHandler:
    def __init__(self, SOCKET: str, on_message: Callable[[str], None], report_error_str: Callable[[str, str], None]) -> None:
        self.SOCKET = SOCKET
        self.on_message = on_message
        self.report_error_str = report_error_str
        self.stop_flag = False
        self.thread = None
        self.reconnection_limit = 10
        self.reconnection_count = 0

    
    def start(self):
        self.stop_flag = False
        self.thread = threading.Thread(target=self.websocket_loop)
        self.thread.start()

    
    def stop(self):
        self.stop_flag = True
        if self.thread is not None:
            self.thread.join()
            self.thread = None

    
    def websocket_loop(self):
        try:
            self.report_error_str("Starting Websocket", "info")
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            conn = websockets.connect(uri = self.SOCKET) # type: ignore

            async def inner_websocket_loop():
                while not self.stop_flag:
                    try:
                        async with conn as ws:
                            self.report_error_str(f"Websocket connection started.", "setting")
                            while not self.stop_flag:
                                try:
                                    message = await ws.recv()
                                except Exception as e:
                                    self.report_error_str(f"Connection error occurred in Websocket: {e}", "error")
                                    break
                                
                                try:
                                    self.on_message(message)
                                except Exception as e:
                                    self.report_error_str(f"An error occurred in Inner_Websocket_Loop while processing message: {e}", "error")
                                    break
                    except Exception as e:
                        self.report_error_str(f"Restarting Connection after an error: {e}", "error")
                    finally:
                        self.report_error_str(f"Websocket connection ended.", "setting")
                        if not self.stop_flag and self.reconnection_limit < self.reconnection_count:
                            self.report_error_str(f"Restarting Connection.", "setting")
                            self.report_error_str(f"Restart Count: {self.reconnection_count}", "info")
                            await asyncio.sleep(2)


            loop.run_until_complete(inner_websocket_loop())
        except Exception as e:
            self.report_error_str(f"An error occurred in the base Websocket_Loop: {e}", "error")


def convert_to_dicts(list_of_lists):
    # https://i.imgur.com/3Cwe3dF.png
    # https://binance-docs.github.io/apidocs/spot/en/#compressed-aggregate-trades-list
    # https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md
    keys = ["t", "o", "h", "l", "c", "v", "T", "q", "n", "V", "Q", "B"]
    return [dict(zip(keys, sublist)) for sublist in list_of_lists]