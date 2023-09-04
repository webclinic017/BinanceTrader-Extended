from flask import Flask, render_template

import config, bclient

try:
    myClient = bclient.MyClient(config.Binance_Config())
    
except Exception as e:
    print(e)



#flask app 
app = Flask(__name__)   ###app = Flask(__name__, template_folder='template') #fix for not being able to find templates folder

@app.route("/")
def index():
    title = "Binance Trader"
    if myClient:
        accInfo = myClient.client.get_account()

    print(accInfo)
    return render_template("index.html", title = title)

@app.route("/buy/")
def buy():
    return "buy"


@app.route("/sell/")
def sell():
    return "sell"


@app.route("/settings/")
def settings():
    return "settings"


