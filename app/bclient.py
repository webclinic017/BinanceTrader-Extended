from binance.client import Client
from binance.enums import ORDER_TYPE_MARKET
from binance.exceptions import BinanceAPIException
from typing import Tuple
import config, log_handler
from decimal import Decimal, getcontext, ROUND_DOWN



class MyClient():

    def __init__(self, BinanceConfig :config.Binance_Config):
        self.BinanceConfig = BinanceConfig
        self.myLogHandler = log_handler.myLogHandler

        self.client = Client(BinanceConfig.BINANCE_API_KEY, BinanceConfig.BINANCE_API_SECRET, tld=BinanceConfig.BINANCE_CLIENT_TLD)
        
        #self.client.get_account()

        #self.logs = []
        try:
           self.client.get_account()
        except Exception as e:
           self.myLogHandler.add_bclient_log(msg= f"Binance Client Error: {e}", level="critical")
           #self.logs.append(f"API Error: {e}")
           raise ValueError('Manually thrown exception.')

    def printAPI(self):
        print(self.BinanceConfig.BINANCE_API_KEY)


    def fill_order(self, trade_symbol : str, side_order : str, use_asset_percentage : bool, trade_quantity : float, order_type=ORDER_TYPE_MARKET, report_str = log_handler.myLogHandler.add_bclient_log) -> Tuple[bool,str]:
        
        try:
            # Fetch trading rules for the symbol
            info = self.client.get_exchange_info()

            # Default values
            minQty = Decimal('0')
            maxQty = Decimal('0')
            stepSize = Decimal('0')


            for symbol_info in info['symbols']:
                if symbol_info['symbol'] == trade_symbol:
                    for filter in symbol_info['filters']:
                        if filter['filterType'] == 'LOT_SIZE':
                            minQty = Decimal(filter['minQty'])
                            maxQty = Decimal(filter['maxQty'])
                            stepSize = Decimal(filter['stepSize'])

            # Convert trade_quantity to Decimal and adjust it to conform to the trading rules
            d_trade_quantity = Decimal(trade_quantity).quantize(Decimal('.000000000000000001'), rounding=ROUND_DOWN)
            d_trade_quantity = (d_trade_quantity // stepSize) * stepSize
            d_trade_quantity = max(min(d_trade_quantity, maxQty), minQty)

            report_str("use custom trade percentage: {}.".format(use_asset_percentage), level= "order")
            if use_asset_percentage == False:
                report_str("sending order. {}, {}, {}, {}, {}".format(trade_symbol, side_order, use_asset_percentage, d_trade_quantity, order_type), level= "order")
                order = self.client.create_order(symbol = trade_symbol, side=side_order, type=order_type, quantity = d_trade_quantity)
                order_report = calculate_order_report(order=order)
                report_str(f"Order Report: {str(order_report)}", level= "order")

            if use_asset_percentage == True:
                report_str("custom trade percentage is not defined yet", level= "order")
                pass #get total amount of currency and make %90 quantity
        except BinanceAPIException as e:
            if e.code == -1013:  # Filter failure: NOTIONAL
                report_str(f"Notional value of the order is too small. Please increase the order quantity: {str(e)}", level= "critical")
            else:
                report_str(f"Client.fill_order error: {str(e)}", level= "critical")
            return (False, str(e))
        except Exception as e:
            report_str(f"Client.fill_order error: {str(e)}", level= "critical")
            return (False, str(e))
        
        return (True, "")
    
def calculate_order_report(order:dict) -> str:
    #Order: 
    # {'symbol': 'LTCUSDT', 
    # 'orderId': 3758###, 
    # 'orderListId': -1, 
    # 'clientOrderId': 'cO6f3Fczqsl###', 
    # 'transactTime': 169611##, 
    # 'price': '0.00000000', 
    # 'origQty': '0.20000000', 
    # 'executedQty': '0.20000000', 
    # cummulativeQuoteQty': '13.25000000', 
    # 'status': 'FILLED', 
    # 'timeInForce': 'GTC', 
    # 'type': 'MARKET', 
    # 'side': 'BUY', 
    # 'workingTime': 1696110120746, 
    # 'fills': [
    #   {'price': '66.25000000', 
    #   'qty': '0.20000000', 
    #   'commission': '0.00004614', 
    #   'commissionAsset': 'BNB', 
    #   'tradeId': 3079###}
    # ], 
    # 'selfTradePreventionMode': 'NONE'}
    # Assuming 'order' is your dictionary
    symbol = order['symbol']
    status = order['status']

    fills = order['fills']
    total_price = 0
    total_qty = 0

    for fill in fills:
        total_price += float(fill['price'])
        total_qty += float(fill['qty'])

    average_price = total_price / len(fills)
    average_qty = total_qty / len(fills)

    side = order['side']
    if side == "BUY":
        side = "Bought"
    elif side == "SELL":
        side = "Sold"

    final_str = f"ORDER {status}. {side} {total_qty} {symbol} with the average price of {average_price}"

    return final_str