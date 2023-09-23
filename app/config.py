from dotenv import load_dotenv, dotenv_values 
from pathlib import Path
import os, json
import ast
from binance.enums import *

dotenv_path = Path(__file__).with_name('.env') #path to .env file

load_dotenv(dotenv_path = dotenv_path)

class Strategies:
    B_STRATS = json.loads(os.getenv("B_STRATEGIES"))

    ALL_INTERVALS = [KLINE_INTERVAL_1SECOND,
                     KLINE_INTERVAL_1MINUTE,
                     KLINE_INTERVAL_3MINUTE,
                     KLINE_INTERVAL_5MINUTE,
                     KLINE_INTERVAL_15MINUTE,
                     KLINE_INTERVAL_30MINUTE,
                     KLINE_INTERVAL_1HOUR,
                     KLINE_INTERVAL_2HOUR,
                     KLINE_INTERVAL_4HOUR,
                     KLINE_INTERVAL_6HOUR,
                     KLINE_INTERVAL_8HOUR,
                     KLINE_INTERVAL_12HOUR,
                     KLINE_INTERVAL_1DAY,
                     KLINE_INTERVAL_3DAY,
                     KLINE_INTERVAL_1WEEK,
                     KLINE_INTERVAL_1MONTH]

class Trade_Info:
    #Set Trade Informations    
    TRADE_SYMBOLS = json.loads(os.getenv("TRADE_SYMBOLS"))
    TRADE_INTERVALS = json.loads(os.getenv("TRADE_INTERVALS"))
    TRADE_STRATS = json.loads(os.getenv("TRADE_STRATS"))
    
    DEFAULT_SYMBOL = "LTCUSDT"
    DEFAULT_INTERVAL = "15m"
    DEFAULT_STRAT = "rsi_strategy01"

    TRADE_BOTS = ast.literal_eval(os.getenv("TRADE_BOTS"))

class Binance_Config:
    # Set Binance API Keys
    BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
    BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")
    #tld: "us" for usa based IP and "com" for global.
    BINANCE_CLIENT_TLD = "com"


class Flask_Config:
    # Set Flask Environment Variables From .env
    DEBUG = os.getenv("FLASK_DEBUG")
    SERVER = os.getenv("FLASK_SERVER")
    SECRET_KEY = bytes(os.getenv("FLASK_SECRET_KEY"), encoding="utf-8")