#!/usr/bin/env python3
import json

from numpy.linalg import inv
import numpy
import pandas as pd
import io


"""
a = 5, 8, 7
b = 2, 3, 2
c = 1, 2, 3

a = 2b + c

5 = 2x + 1y
8 = 3x + 2y
7 = 2x + 3y

"""


def test2():
    stock_prices = dict()
    stock_prices["a"] = [5, 8, 7]
    stock_prices["b"] = [2, 3, 2]
    stock_prices["c"] = [1, 2, 3]

    #     -1
    # 2 1       5
    # 3 2   *   8
    # 2 3       7

    arrays = []
    arrays.append(stock_prices["b"])
    arrays.append(stock_prices["c"])
    print(numpy.matrix.transpose(numpy.array(arrays)))

    a = numpy.array([[2, 1],
                     [3, 2],
                     [2, 3]])

    b = numpy.array([[5],
                     [8],
                     [7]])

    a_transpose = numpy.matrix.transpose(a)

    at_a = numpy.matmul(a_transpose, a)
    at_b = numpy.matmul(a_transpose, b)

    a_at_inv = inv(at_a)

    print(numpy.matmul(a_at_inv, at_b))


def test1():
    a = numpy.array([[1, 8],
                     [2, -8]])
    b = numpy.array([[7],
                     [-3]])
    ainv = inv(a)

    result = numpy.matmul(ainv, b)

    print(result)


def doit(stocks, ticker):

    arrays = []
    tickers = []
    for current_ticker, price_list in stocks.items():
        if current_ticker == ticker:
            continue
        arrays.append(price_list)
        tickers.append(current_ticker)

    a = numpy.matrix.transpose(numpy.array(arrays))

    b = numpy.matrix.transpose(numpy.array([stocks[ticker]]))
    a_transpose = numpy.matrix.transpose(a)

    at_a = numpy.matmul(a_transpose, a)
    at_b = numpy.matmul(a_transpose, b)

    a_at_inv = inv(at_a)

    solution = numpy.matmul(a_at_inv, at_b)

    formula = f"{ticker} = "
    for i in range(0, len(tickers)):
        num = solution[i][0]
        current_ticker = tickers[i]
        formula += f"{num:.2f}*P({current_ticker}) + "
    print(formula)


def filter_prices():
    with open("nasdaq-2000-2022-prices.csv") as f:
        prices = f.read()
    companies = pd.read_csv(io.StringIO(prices))
    #print(companies.head(5))
    #print(companies["Name"][0])

    stock_prices = dict()

    for row in companies.iterrows():
        name = row[1]["Name"]

        if not name in stock_prices:
            stock_prices[name] = dict()

        date = row[1]["Date"]
        year = date.split("-")[0]

        if not year in stock_prices[name]:
            stock_prices[name][year] = row[1]["Adj Close"]

    open("out2.json", "w").write(json.dumps(stock_prices))


def compare():
    with open("out.json") as f:
        close_prices = json.loads(f.read())

    with open("out2.json") as f:
        adj_close_prices = json.loads(f.read())

    print(close_prices["AAPL"]["2021"])
    print(adj_close_prices["AAPL"]["2021"])

    print(close_prices["AAPL"]["2019"])
    print(adj_close_prices["AAPL"]["2019"])


def do_analysis():
    stock_prices = dict()

    with open("out.json") as f:
        close_prices = json.loads(f.read())

    for ticker, prices in close_prices.items():

        fail = False
        price_list = []
        for year in range(2000, 2021):
            if str(year) not in prices:
                fail = True
                break
            price_list.append(prices[str(year)])

        if fail:
            continue

        #print(ticker)
        #print(price_list)
        stock_prices[ticker] = price_list

    doit(stock_prices, "AAPL")



def main():
    #filter_prices()
    #compare()
    do_analysis()
    #test4()


def test4():
    stock_prices = dict()
    stock_prices["a"] = [5, 8, 7]
    stock_prices["b"] = [2, 3, 2]
    stock_prices["c"] = [1, 2, 3]

    doit(stock_prices, "a")
    return


def test3():

    stock_prices = dict()
    stock_prices["a"] = [5, 8, 7]
    stock_prices["b"] = [2, 3, 2]
    stock_prices["c"] = [1, 2, 3]

    arrays = []
    arrays.append(stock_prices["b"])
    arrays.append(stock_prices["c"])
    a = numpy.matrix.transpose(numpy.array(arrays))

    b = numpy.matrix.transpose(numpy.array([stock_prices["a"]]))

    a_transpose = numpy.matrix.transpose(a)

    at_a = numpy.matmul(a_transpose, a)
    at_b = numpy.matmul(a_transpose, b)

    a_at_inv = inv(at_a)

    print(numpy.matmul(a_at_inv, at_b))


if __name__ == "__main__":
    main()