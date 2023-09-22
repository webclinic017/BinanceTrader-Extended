from flask import Flask, render_template, redirect, request, flash, jsonify, Response, url_for, session
from datetime import datetime

import config, bclient, khistory, backtest, btrader, chart_actions, asyncio, btmanager

bconnection = False
try:
    myClient = bclient.MyClient(config.Binance_Config())
    bconnection = True
    my_btmanager = btmanager.BTManager(myClient=myClient)
except Exception as e:
    print(e)


#flask app 
app = Flask(__name__)   ###app = Flask(__name__, template_folder='template') #fix for not being able to find templates folder
app.secret_key = config.Flask_Config.SECRET_KEY


@app.route("/")
def index():
    global my_btmanager
    title = "Binance Trader"
    

    #display 1
    if "display1_trade_symbol" not in session:
        session["display1_trade_symbol"] = str(config.Trade_Info.DEFAULT_SYMBOL)
    if "display1_trade_interval" not in session:
        session["display1_trade_interval"] = str(config.Trade_Info.DEFAULT_INTERVAL)
    if "display1_trade_strat" not in session:
        session["display1_trade_strat"] = str(config.Trade_Info.DEFAULT_STRAT)

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
    
    btraders_info = my_btmanager.myTraders_info

    session["btrader_id"] = "0"

    if "btrader_id" not in session:
        session["btrader_id"] = "-1"
    btrader_id = int(session["btrader_id"])
    
    #if btrader_id != -1:
    try:
        btrader_logs = my_btmanager.myTraders[btrader_id].get_logs()
    except:
        btrader_logs = []
    print(f"app bt_logs: {btrader_logs}")


    return render_template("index.html", 
                           title = title, 
                           acc_balances= acc_balances, 
                           exc_trade_symbols = exc_trade_symbols, 
                           display1_trade_symbol=display1_trade_symbol,
                           display1_trade_interval = display1_trade_interval,
                           url_history = url_for("history"),
                           backtest_message = backtest_message,
                           btraders_info = btraders_info,
                           btrader_logs = btrader_logs
                           )


@app.route("/quicktrade/", methods = ["POST"])
def quicktrade():
    print(request.form)

    #Quick Trade
    if request.form['trade_action'] == "buy":
        t_action = "BUY"
    if request.form['trade_action'] == "sell":
        t_action = "SELL"

    q_trade_result = myClient.fill_order( request.form['trade_symbol'], t_action, False, request.form["trade_quantity"])
    
    if q_trade_result != True:
        flash("Quick Trade Failed: " + q_trade_result.message, "error")
    else:
        flash("Quick Trade Successful", "message")
    
    return redirect("/")


@app.route("/debug/")
def debug1():
    global my_btmanager
    
    my_btmanager.create_traders_from_env()
    my_btmanager.start_all_traders()


    return "debug01"


@app.route("/debug2/")
def debug2():
    global my_btmanager
    
    #ti = my_btmanager.create_trader("BTCUSDT", "5m", 0.00003, config.Trade_Info.DEFAULT_STRAT)
    #my_btmanager.start_trader(ti)

    
    #my_btmanager.start_trader(0)
    return "debug02"


@app.route("/debug3/")
def debug3():
    global my_btmanager
    
    #ti = my_btmanager.create_trader("BTCUSDT", "5m", 0.00003, config.Trade_Info.DEFAULT_STRAT)
    #my_btmanager.start_trader(ti)

    #my_btmanager.start_all_traders()
    #my_btmanager.start_trader(1)
    return "debug03"


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

    __TRADE_SYMBOL = request.args.get("TRADE_SYMBOL", default=config.Trade_Info.DEFAULT_SYMBOL, type=str)
    __TRADE_INTERVAL = request.args.get("TRADE_INTERVAL", default=config.Trade_Info.DEFAULT_INTERVAL, type=str)

    #candlesticks = myClient.client.get_historical_klines(config.Trade_Info.TRADE_SYMBOLS[0], config.Trade_Info.TRADE_INTERVALS[0], "15 days")
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
    

    #set up symbol and interval
    if "display1_trade_symbol" not in session:
        session["display1_trade_symbol"] = str(config.Trade_Info.DEFAULT_SYMBOL)
    if "display1_trade_interval" not in session:
        session["display1_trade_interval"] = str(config.Trade_Info.DEFAULT_INTERVAL)
    if "display1_trade_strat" not in session:
        session["display1_trade_strat"] = str(config.Trade_Info.DEFAULT_STRAT)

    display1_trade_symbol = session["display1_trade_symbol"]
    display1_trade_interval = session["display1_trade_interval"]
    display1_trade_strat = session["display1_trade_strat"]
    #download and save kline history as a csv file
    if(True): 
        asyncio.run(khistory.download_khistory(myClient.client, display1_trade_symbol, display1_trade_interval, DATE_PROMPT_START= date_start, DATE_PROMPT_END= date_end)) 

    csv_name = khistory.get_csv_name(display1_trade_symbol, display1_trade_interval)
    backtest.run1(csv_name, display1_trade_interval, strategy_str=display1_trade_strat)

    session["backtest_message"] = "Success"
    return redirect(url_for("index"))
