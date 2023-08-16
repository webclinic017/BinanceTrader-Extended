from binance.client import Client
from binance.enums import *
import numpy, talib

import order_actions

RSI_PERIOD = 14
RSI_OVERBOUGHT = 60
RSI_OVERSOLD = 40
TRADE_SYMBOL = "LTCBUSD"
USE_TRADE_QUANTITY = "Y"
TRADE_QUANTITY = 0.2

in_position = False

def calculate_trade(client, closes):
    global in_position
    if len(closes) > RSI_PERIOD:
        np_closes = numpy.array(closes)
        rsi = talib.RSI(np_closes, RSI_PERIOD) #talib.RSI returns multiple RSI values 
        
        print("all rsis calculated so far")
        print(rsi)

        last_rsi = rsi[-1]
        print("the current rsi is {}".format(last_rsi))

        try:
            #sell current position
            if last_rsi > RSI_OVERBOUGHT:
                print("in overbought area.")
                print(in_position)
                if in_position:
                    print("Sell! Sell! Sell!")
                    
                    order_success =  order_actions.fill_order(client = client, calculated_order= cook_order(SIDE_SELL))
                    if order_success:
                        in_position = False
                    #Binance sell logic
                else:
                    print("It is overbough, but I am not in position to sell.")
                
            #buy new position
            if last_rsi < RSI_OVERSOLD:
                print("in oversold area.")
                print(in_position)
                if in_position:
                    print("it is oversold, but I am already in position.")
                else:
                    print("Buy! Buy! Buy!")
                    
                    order_success = order_actions.fill_order(client = client, calculated_order= cook_order(SIDE_BUY))
                    if order_success:
                        in_position = True
                    #Binance buy logic
        except Exception as e:
            print(e)
def cook_order(side_order):
    cooked_order = "+".join([str(TRADE_SYMBOL), str(side_order), str(USE_TRADE_QUANTITY), str(TRADE_QUANTITY)])
    print("cooked order = " + cooked_order)
    return(cooked_order)
 