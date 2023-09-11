from flask import Flask, render_template, redirect, request, flash, jsonify

import config, bclient, chart_actions

bconnection = False
try:
    myClient = bclient.MyClient(config.Binance_Config())
    bconnection = True
except Exception as e:
    print(e)



#flask app 
app = Flask(__name__)   ###app = Flask(__name__, template_folder='template') #fix for not being able to find templates folder
app.secret_key = config.Flask_Config.SECRET_KEY


@app.route("/")
def index():
    title = "Binance Trader"
    display1_trade_symbol = config.TRADE_SYMBOLS[0]
    display1_trade_interval = config.TRADE_INTERVALS[0]
    if bconnection:
        acc_info = myClient.client.get_account()
        acc_balances = acc_info["balances"]

        exc_info = myClient.client.get_exchange_info()
        exc_trade_symbols = exc_info["symbols"]

    print()
    return render_template("index.html", 
                           title = title, 
                           acc_balances= acc_balances, 
                           exc_trade_symbols = exc_trade_symbols, 
                           display1_trade_symbol=display1_trade_symbol,
                           display1_trade_interval = display1_trade_interval
                           )


@app.route("/quicktrade/", methods = ["POST"])
def quicktrade():
    print(request.form)
    if request.form['trade_action'] == "buy":
        t_action = "BUY"
    if request.form['trade_action'] == "sell":
        t_action = "SELL"

    result = myClient.fill_order( request.form['trade_symbol'], t_action, "N", request.form["trade_quantity"])
    
    if result != True:
        flash("Quick Trade Failed: " + result.message, "error")
    else:
        flash("Quick Trade Successful", "message")
    return redirect("/")


@app.route("/buy/", methods = ["POST"])
def buy():
    
    return "buy"


@app.route("/sell/", methods = ["POST"])
def sell():
    return "sell"


@app.route("/settings/")
def settings():
    return "settings"


@app.route("/history")
def history():

    candlesticks = myClient.client.get_historical_klines(config.TRADE_SYMBOLS[0], config.TRADE_INTERVALS[0], "15 days")
    p_klines = chart_actions.process_klineslist_to_chartdictformat(candlesticks)
    return(jsonify(p_klines))

