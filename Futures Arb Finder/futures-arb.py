#!/usr/bin/env python3

import datetime
import json
import math
import pprint
import sys
import traceback

from tda.auth import easy_client
from tda.streaming import StreamClient
from selenium import webdriver
import asyncio
import pickle
import requests


class FuturesDetails:
    btc_tickers = ["/BTCG22",
                   "/BTCH22",
                   "/BTCJ22",
                   "/BTCK22",
                   "/BTCM22",
                   "/BTCN22",
                   "/BTCQ22",
                   "/BTCZ22",
                   "/BTCZ23",
                   ]
    eth_tickers = ["/ETHG22",
                   "/ETHH22",
                   "/ETHJ22",
                   "/ETHK22",
                   "/ETHM22",
                   "/ETHN22",
                   "/ETHQ22",
                   "/ETHZ22",
                   "/ETHZ23",
                   ]
    all_tickers = btc_tickers + eth_tickers


class CoinbaseAPI:

    @staticmethod
    def get_btc_spot():
        page = requests.get(url="https://api.coinbase.com/v2/prices/spot?currency=USD")
        response = json.loads(page.content)
        return response["data"]["amount"]

    @staticmethod
    def get_eth_spot():
        page = requests.get(url="https://api.coinbase.com/v2/prices/ETH-USD/spot")
        response = json.loads(page.content)
        return response["data"]["amount"]


class TDAuthInfo:
    td_consumer_key = "GGMUX8J8AAA8JSOXXDGBCTGRBQO3SO5R"
    redirect_uri = "https://localhost"
    token_path = "/tmp/token.json"
    account_id = 275218956
    stream_client: StreamClient = None
    client = None

    def get_client(self):
        if not self.client:
            self.client = easy_client(
                webdriver_func=lambda: webdriver.Chrome(),
                api_key=TDAuthInfo.td_consumer_key,
                redirect_uri=TDAuthInfo.redirect_uri,
                token_path=TDAuthInfo.token_path)
        return self.client

    def get_stream_client(self):
        if not self.stream_client:
            self.stream_client = StreamClient(self.get_client(), account_id=self.account_id)
        return self.stream_client


class FinMath:

    @staticmethod
    def calculate_apy(current_price, future_price, days_until_maturity):
        profit = future_price - current_price
        annualized_profit = (profit / days_until_maturity) * 365
        return annualized_profit / current_price


class FutureInfo:
    ticker: str
    bid: int
    ask: int
    last: int
    mark: int
    future_settlement_price: int
    expiration_date: datetime.date
    description: str


def get_value_or_none(dictionary, key):
    if not key in dictionary:
        return None
    else:
        return dictionary[key]


class FuturesArb:
    td: TDAuthInfo
    future_info = dict()
    pickle_file = "future_info.pickle"

    def __init__(self, td: TDAuthInfo):
        self.td = td

    def serialize_info(self):
        pickle.dump(self.future_info, open(self.pickle_file, "wb"))

    def deserialize_info(self):
        self.future_info = pickle.load(open(self.pickle_file, "rb"))

    def test(self):
        btc_spot_price = int(math.floor(float(self.future_info["BTC_SPOT"])))
        eth_spot_price = int(math.floor(float(self.future_info["ETH_SPOT"])))
        print(f"BTC Spot: {btc_spot_price}")
        print(f"ETH Spot: {eth_spot_price}")
        print("")
        print("Long Spot Short Future")
        for ticker in FuturesDetails.all_tickers:
            info: FutureInfo = self.future_info[ticker]
            bid = info.bid
            ask = info.ask
            expiration_string = info.expiration_date.strftime("%m/%d")
            if not bid or not ask:
                continue
            if ticker in FuturesDetails.btc_tickers:
                spot_price = btc_spot_price
            elif ticker in FuturesDetails.eth_tickers:
                spot_price = eth_spot_price
            else:
                raise Exception(f"Unexpected ticker: {ticker}")
            days_until_expiration = (info.expiration_date - datetime.datetime.now()).days
            apy = FinMath.calculate_apy(spot_price, bid, days_until_expiration)
            print(f"{ticker} {expiration_string} bid: {bid}, apy %.02f%%" % (apy * 100))
        print("")
        print("Short Spot Long Future")
        for ticker in FuturesDetails.all_tickers:
            info: FutureInfo = self.future_info[ticker]
            bid = info.bid
            ask = info.ask
            expiration_string = info.expiration_date.strftime("%m/%d")
            if not bid or not ask:
                continue
            if ticker in FuturesDetails.btc_tickers:
                spot_price = btc_spot_price
            elif ticker in FuturesDetails.eth_tickers:
                spot_price = eth_spot_price
            else:
                raise Exception(f"Unexpected ticker: {ticker}")
            days_until_expiration = (info.expiration_date - datetime.datetime.now()).days
            apy = FinMath.calculate_apy(ask, spot_price, days_until_expiration)
            print(f"{ticker} {expiration_string} ask: {ask}, apy %.02f%%" % (apy * 100))

    def get_spot_prices(self):
        self.future_info["BTC_SPOT"] = CoinbaseAPI.get_btc_spot()
        self.future_info["ETH_SPOT"] = CoinbaseAPI.get_eth_spot()

    def download_futures_prices(self):
        stream_client = self.td.get_stream_client()

        async def read_stream():
            await stream_client.login()
            await stream_client.quality_of_service(StreamClient.QOSLevel.DELAYED)

            def handle_streaming_message(message):
                assert message["service"] == "LEVELONE_FUTURES"
                contents = message["content"]
                for content in contents:
                    try:
                        assert content["key"] in FuturesDetails.all_tickers
                        print(f'downloading {content["key"]}')
                        info = FutureInfo()
                        info.ticker = content["key"]

                        info.bid = get_value_or_none(content, "BID_PRICE")
                        info.ask = get_value_or_none(content, "ASK_PRICE")
                        info.last = get_value_or_none(content, "LAST_PRICE")
                        info.mark = get_value_or_none(content, "MARK")

                        info.expiration_date = datetime.datetime.utcfromtimestamp(
                            content["FUTURE_EXPIRATION_DATE"] / 1000)
                        info.description = content["DESCRIPTION"]
                        self.future_info[content["key"]] = info
                    except KeyError:
                        pprint.pprint(content)
                        traceback.print_exc()
                        sys.exit(1)

            stream_client.add_level_one_futures_handler(handle_streaming_message)
            await stream_client.level_one_futures_subs(FuturesDetails.all_tickers)

            while True:
                await stream_client.handle_message()
                keep_going = False
                for ticker in FuturesDetails.all_tickers:
                    if ticker not in self.future_info:
                        # We're missing one, so continue.
                        keep_going = True
                if keep_going:
                    continue
                else:
                    break

            await stream_client.level_one_futures_unsubs(FuturesDetails.all_tickers)

        asyncio.run(read_stream())


def do_sync(arb):
    arb.download_futures_prices()
    arb.get_spot_prices()
    arb.serialize_info()


def main():
    td = TDAuthInfo()
    arb = FuturesArb(td)
    #do_sync(arb)
    arb.deserialize_info()
    arb.test()


if __name__ == "__main__":
    main()
