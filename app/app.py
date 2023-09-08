from flask import Flask, render_template

import config, bclient

bconnection = False
try:
    myClient = bclient.MyClient(config.Binance_Config())
    bconnection = True
except Exception as e:
    print(e)



#flask app 
app = Flask(__name__)   ###app = Flask(__name__, template_folder='template') #fix for not being able to find templates folder

@app.route("/")
def index():
    title = "Binance Trader"

    if bconnection:
        acc_info = myClient.client.get_account()
        acc_balances = acc_info["balances"]    

    print()
    return render_template("index.html", title = title, acc_balances= acc_balances)

@app.route("/buy/")
def buy():
    return "buy"


@app.route("/sell/")
def sell():
    return "sell"


@app.route("/settings/")
def settings():
    return "settings"


