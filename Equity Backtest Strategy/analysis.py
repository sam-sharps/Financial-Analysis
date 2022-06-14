#!/usr/bin/env python3


import pandas as pd
import io
import dateutil.parser
import datetime
import argparse
from collections import defaultdict
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
import sys


class Arguments:
    start_date: datetime
    end_date: datetime


global_args = Arguments()


def parse_csv():
    #
    # Read CPI CSV.
    #
    with open("spx.csv") as f:
        cpi = f.read()

    cpi = pd.read_csv(io.StringIO(cpi))

    #
    # Parse out values to get an array of date and value pairs
    #
    spx = []
    spx2 = []
    year = []
    month = []
    prev_date = None
    for row in cpi.iterrows():
        date = row[1]["Date"]
        value = row[1]["Adj Close"]

        dt = dateutil.parser.parse(date)

        if not dt > global_args.start_date:
            continue
        if not global_args.end_date > dt:
            continue

        if prev_date:
            difference = dt - prev_date
            if difference.days <= 0:
                raise Exception("Unexpected date")

            if prev_date.year != dt.year:
                year = []
                spx2.append(year)

            if prev_date.month != dt.month :
                month = []
                year.append(month)

        month.append((dt, value))

        #spx.append((dt, value))

        prev_date = dt

    #pprint(spx2)
    return spx2
    #return spx


def fatal(error_string):
    print(error_string)
    sys.exit(1)


def parse_date(date_string):
    try:
        year, month, day = date_string.split("-")
        return datetime.datetime(int(year), int(month), int(day))
    except ValueError as ve:
        fatal(f"Failed to parse date: {date_string}\n" +
              str(ve))


def parse_arguments():
    parser = argparse.ArgumentParser(description='Backtest SPX trades.')
    parser.add_argument("--start-date", required=True, help="Date to start backtesting from. E.g 2000-01-01.")
    parser.add_argument("--end-date", required=True, help="Date to start backtesting from. E.g 2005-05-05.")
    arguments = parser.parse_args()

    start_date_string = vars(arguments)["start_date"]
    global_args.start_date = parse_date(start_date_string)

    end_date_string = vars(arguments)["end_date"]
    global_args.end_date = parse_date(end_date_string)


def run_simulation(spx, montly_income, strategy):
    balance = montly_income
    shares = 0
    prev_date = None
    prev_value = None

    for year in spx:
        for month in year:
            days_left_in_month = len(month)
            for date, value in month:
                if prev_date:

                    if prev_date.month != date.month:
                        balance += 10000

                    if strategy == "always-buy":
                        if balance > 0:
                            can_buy = float(balance)/float(value)
                            balance -= float(can_buy) * float(value)
                            shares += can_buy
                    elif strategy == "cost-average":
                        if balance > 0:
                            to_spend = balance / days_left_in_month
                            to_buy = float(to_spend) / float(value)
                            balance -= float(to_buy) * float(value)
                            shares += to_buy
                    elif strategy == "down-day":
                        if balance > 0:
                            if days_left_in_month == 10:
                                print("end of month")
                            if days_left_in_month == 1 or value < prev_value:
                                can_buy = float(balance) / float(value)
                                balance -= float(can_buy) * float(value)
                                shares += can_buy

                prev_date = date
                prev_value = value
                days_left_in_month -= 1

    print(strategy)
    print(f"Portfolio value: %.02f" % (balance + shares * prev_value))


def longest_green(spx):
    prev = None
    counter = 0
    biggest_counter = 0
    for year in spx:
        for month in year:
            for date, value in month:
                if prev:
                    if value > prev:
                        counter += 1
                    else:
                        if counter > biggest_counter:
                            biggest_counter = counter
                        counter = 0
                prev = value

    print(biggest_counter)


def main():
    parse_arguments()
    spx = parse_csv()

    longest_green(spx)
    return
    run_simulation(spx, 10000, "nothing")
    run_simulation(spx, 10000, "always-buy")
    run_simulation(spx, 10000, "cost-average")
    run_simulation(spx, 10000, "down-day")


if __name__ == "__main__":
    main()
