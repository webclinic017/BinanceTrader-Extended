# BinanceTrader-Extended

## Overview

This project uses Binance API to trade crypto in real-time using technical analysis. And gives the option to backtest the strategies using [backtrader](https://github.com/mementum/backtrader). Any amount of traders can be deployed with any pair/interval/strategy. It also supports the development of new trading strategies.
The Program is running a Flask application with user-friendly UI and has a quick trading option with [lightweight-charts](https://www.tradingview.com/lightweight-charts/) implemented

## Features

1. **Trade With Multiple Trade Bots At The Same Time Using Different Strategies.**

2. **Backtest The Strategies On Whichever Trading Pair and Trade Interval You Want.**

3. **Quick Trade Your Assets On All Trading Pairs.**

4. **Do It All In A User-Friendly Interface.**

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/BeratDM/BinanceTrader-Extended.git
   cd BinanceTrader-Extended
   ```

2. Set up a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Environment Setup:** Create your `.env` file at `./app/.env` with your API keys using `./app/.env.template`.

2. **Run The Program:** Go to the `./app` folder and run `main.py`. Make sure you are using the virtual environment if you set it up. A flask application will start and you can visit the url in your browser.

3. **Strategy Development:** New trading strategies can be developed inside the `app/TradeStrategies/` folder by making a new Python file for your strategy and creating two classes, one for backtesting subclassing the `backtrader.Strategy` class, and the other for live trading subclassing the `bStrategy` class. After that, edit the `app/strategy_manager.py` and your `.env` files similarly to the examples to reference your classes.

---

*Disclaimer: This project is developed for personal purposes. Trading and investing involve significant risks, and using this software does not guarantee any profits. Please conduct thorough testing and research before deploying any trading strategy.*
