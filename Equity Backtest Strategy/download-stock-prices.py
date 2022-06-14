#!/usr/bin/env python3

import pandas as pd
import yfinance as yf
import datetime
import time
import requests
import io

start = datetime.datetime(1900,1,1)
end = datetime.datetime(2025,3,1)

stock_final = pd.DataFrame()

i = "SPY"
try:
    # download the stock price
    stock = yf.download(i,start=start, end=end, progress=False)

    # append the individual stock prices
    if len(stock) == 0:
        pass
    else:
        stock['Name']=i
        stock_final = stock_final.append(stock,sort=False)
except Exception:
    pass

stock_final.to_csv(path_or_buf="out.csv")
