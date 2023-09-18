from flask import Flask, render_template, redirect, request, flash, jsonify, Response, url_for, session
from datetime import datetime

import config, bclient, btrader, chart_actions, asyncio

bconnection = False
try:
    myClient = bclient.MyClient(config.Binance_Config())
    bconnection = True
except Exception as e:
    print(e)


my_btrader1 = btrader.bTrader(myClient=myClient, TRADE_SYMBOL=config.TRADE_SYMBOLS[0], TRADE_INTERVAL=config.TRADE_INTERVALS[0])
my_btrader2 = btrader.bTrader(myClient=myClient, TRADE_SYMBOL=config.TRADE_SYMBOLS[1], TRADE_INTERVAL=config.TRADE_INTERVALS[1])

#flask app 
app = Flask(__name__)   ###app = Flask(__name__, template_folder='template') #fix for not being able to find templates folder
app.secret_key = config.Flask_Config.SECRET_KEY


@app.route("/")
def index():
    title = "Binance Trader"


    #display 1
    if "display1_trade_symbol" not in session:
        session["display1_trade_symbol"] = str(config.TRADE_SYMBOLS[1])
    if "display1_trade_interval" not in session:
        session["display1_trade_interval"] = str(config.TRADE_INTERVALS[1])

    display1_trade_symbol = session["display1_trade_symbol"]
    display1_trade_interval = session["display1_trade_interval"]


    #quick trade
    if bconnection:
        acc_info = myClient.client.get_account()
        acc_balances = acc_info["balances"]

        exc_info = myClient.client.get_exchange_info()
        exc_trade_symbols = exc_info["symbols"]


    #Backtest Message
    backtest_message = ""
    if "backtest_message" in session:
        backtest_message = session["backtest_message"]
        session.pop("backtest_message", None)
    
    print(backtest_message)

    return render_template("index.html", 
                           title = title, 
                           acc_balances= acc_balances, 
                           exc_trade_symbols = exc_trade_symbols, 
                           display1_trade_symbol=display1_trade_symbol,
                           display1_trade_interval = display1_trade_interval,
                           backtest_message = backtest_message
                           )


@app.route("/quicktrade/", methods = ["POST"])
def quicktrade():
    print(request.form)

    #Quick Trade
    if request.form['trade_action'] == "buy":
        t_action = "BUY"
    if request.form['trade_action'] == "sell":
        t_action = "SELL"

    q_trade_result = myClient.fill_order( request.form['trade_symbol'], t_action, "N", request.form["trade_quantity"])
    
    if q_trade_result != True:
        flash("Quick Trade Failed: " + q_trade_result.message, "error")
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

    __TRADE_SYMBOL = request.args.get("TRADE_SYMBOL", default=config.TRADE_SYMBOLS[0], type=str)
    __TRADE_INTERVAL = request.args.get("TRADE_INTERVAL", default=config.TRADE_INTERVALS[0], type=str)

    #candlesticks = myClient.client.get_historical_klines(config.TRADE_SYMBOLS[0], config.TRADE_INTERVALS[0], "15 days")
    candlesticks = myClient.client.get_klines(symbol = __TRADE_SYMBOL, interval = __TRADE_INTERVAL)
    p_klines = chart_actions.process_klineslist_to_chartdictformat(candlesticks)
    return(jsonify(p_klines))


@app.route("/bg-run-backtest/", methods = ["POST"])
def bg_run_backtest():
    print(request.form)
    date_start = request.form["date_start"]
    date_end = request.form["date_end"]
    
    if date_end =="" or date_start == "":
        session["backtest_message"] = "backtest Failed - Enter Dates"
        return redirect(url_for("index"))
    
    datetime_start = datetime.strptime(date_start, '%Y-%m-%d')
    datetime_end = datetime.strptime(date_end, '%Y-%m-%d')

    if datetime_end <= datetime_start:
        session["backtest_message"] = "backtest Failed - Wrong Dates"
        return redirect(url_for("index"))
    
    #download and save kline history as a csv file
    if(True): 
        asyncio.run(bclient.khistory.download_khistory(myClient.client, config.TRADE_SYMBOLS[0], config.TRADE_INTERVALS[0], DATE_PROMPT_START= date_start, DATE_PROMPT_END= date_end)) 

    csv_name = bclient.khistory.get_csv_name(config.TRADE_SYMBOLS[0], config.TRADE_INTERVALS[0])
    bclient.backtest.run1(csv_name, config.TRADE_INTERVALS[0])

    session["backtest_message"] = "Success"
    return redirect(url_for("index"))
