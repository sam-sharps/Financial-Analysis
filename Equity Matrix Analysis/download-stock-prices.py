#!/usr/bin/env python3

import pandas as pd
import yfinance as yf
import datetime
import time
import requests
import io

start = datetime.datetime(2000,1,1)
end = datetime.datetime(2022,1,1)

with open("data/nasdaq-listed_csv.csv") as f:
    s = f.read()


companies = pd.read_csv(io.StringIO(s))
symbols = companies['Symbol'].tolist()

stock_final = pd.DataFrame()

# iterate over each symbol
for i in symbols:

    # print the symbol which is being downloaded
    print( str(symbols.index(i)) + str(' : ') + i, sep=',', end=',', flush=True)

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