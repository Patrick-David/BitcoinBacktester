
# Bit(cointegration) BackTester

![alt-text](https://github.com/Patrick-David/BitcoinBacktester/blob/master/ezgif.com-add-text(1).gif)

[Code to accompany Medium post](https://medium.com/@pdquant/build-a-bitcoin-tegration-backtester-83e2b19125fd)

Contains .py version for running in terminal with no charting
and full jupyter notebbook .ipynb version with full analysis

## This tutorial is in 2 parts - (you can run the backtester as a separate standalone module) :
### Learn the Statistical technique of Cointegration.
### Build a Bitcoin Backtesting engine using Python to analyze the performance of a Cointegration based trading strategy.

What are we building

![alt-text](https://github.com/Patrick-David/BitcoinBacktester/blob/master/IMG_0988.JPG)

##### We are going to build a python based event-driven backtester that pulls 2 crypto securities Bitcoin (BTC)and Bitcoin Cash (BCH) from an API, passes it through a trading strategy that uses the mean reverting cointegration spread between the 2 securities and generates buy/sell signals when the spread hits ± 1 stdev. We then send these signals to the Portfolio class which handles the logic of the backtester. One time stamp will be pulled and processed at a time, allowing us to see what would have happened in tick-by-tick. Finally we print the results to console (or jupyter notebook) and print out the PnL (profit and loss).

#### To run the .py version simply clone the repo, and run: python bitcoin_backtester.py
#### To run the ipynb version, cd into the repo folder after downloading it and run: jupyter notebook
