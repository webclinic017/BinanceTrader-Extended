from dotenv import load_dotenv, dotenv_values 
from pathlib import Path
import os, json

dotenv_path = Path(__file__).with_name('.env') #path to .env file

load_dotenv(dotenv_path = dotenv_path)
TRADE_SYMBOLS = json.loads(os.getenv("TRADE_SYMBOLS"))
TRADE_INTERVALS = json.loads(os.getenv("TRADE_INTERVALS"))

class Binance_Config:
    # Set Binance API Keys
    BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
    BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")


class Flask_Config:
    # Set Flask Environment Variables From .env
    DEBUG = os.getenv("FLASK_DEBUG")
    SERVER = os.getenv("FLASK_SERVER")
    SECRET_KEY = bytes(os.getenv("FLASK_SECRET_KEY"), encoding="utf-8")