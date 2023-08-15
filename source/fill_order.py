from binance.client import Client
from binance.enums import *



def fill_order(client, calculated_order, order_type=ORDER_TYPE_MARKET):
    trade_symbol, side_order, use_trade_quantity, trade_quantity = split_order(calculated_order)
    
    try:
        print("use custom trade quantity: {}.".format(use_trade_quantity))
        if use_trade_quantity == "Y":
            print("sending order.")
            order = client.create_order(symbol = trade_symbol, side=side_order, type=order_type, quantity = trade_quantity)
            print(order)

        if use_trade_quantity == "N":
            pass #get total amount of currency and make %90 quantity
    except Exception as e:
        print(e)
        return False
    
    return True



def split_order(calculated_order):
    splitted_order = calculated_order.split("+")

    trade_symbol = splitted_order[0]
    buy_or_sell = splitted_order[1]
    use_trade_quantity = splitted_order[2]
    trade_quantity = splitted_order[3]

    return trade_symbol, buy_or_sell, use_trade_quantity,trade_quantity

