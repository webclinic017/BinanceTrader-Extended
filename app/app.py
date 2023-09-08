from flask import Flask, render_template, redirect, request, flash

import config, bclient

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

    if bconnection:
        acc_info = myClient.client.get_account()
        acc_balances = acc_info["balances"]

        exc_info = myClient.client.get_exchange_info()
        exc_trade_symbols = exc_info["symbols"]

    print()
    return render_template("index.html", title = title, acc_balances= acc_balances, exc_trade_symbols = exc_trade_symbols)

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


