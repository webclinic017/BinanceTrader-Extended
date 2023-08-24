from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "hello world"

@app.route("/buy/")
def buy():
    return "buy"


@app.route("/sell/")
def sell():
    return "sell"


@app.route("/settings/")
def settings():
    return "settings"


