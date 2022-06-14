#!/usr/bin/env python3

import requests

api_key = "b3ec31681231c0cdab3aef404a622223"

def getpricetobook(stock):
    #BS = requests.get(f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/AAPL?period=quarter&limit=400&apikey={api_key}")
    BS = requests.get(f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/AAPL?limit=400&apikey={api_key}")
    BS = BS.json()
    print(BS)

getpricetobook('AAPL')
