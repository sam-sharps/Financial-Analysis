import requests
import json
import pprint
from tda.auth import easy_client
from selenium import webdriver


def get_instruments():
    td_consumer_key = "GGMUX8J8AAA8JSOXXDGBCTGRBQO3SO5R"
    url = "https://api.tdameritrade.com/v1/instruments"
    page = requests.get(url=url,
                        params={'apikey': td_consumer_key,
                                'symbol': "/BTC",
                                "projection": "symbol-regex"})
    content = json.loads(page.content)
    pprint.pprint(content)


def test_tda():
    td_consumer_key = "GGMUX8J8AAA8JSOXXDGBCTGRBQO3SO5R"
    c = easy_client(
        webdriver_func=lambda: webdriver.Chrome(),
        api_key=td_consumer_key,
        redirect_uri='https://localhost',
        token_path='/tmp/token.json')
    #    resp = c.get_price_history('/BTC',
    #                               period_type=Client.PriceHistory.PeriodType.YEAR,
    #                               period=Client.PriceHistory.Period.TWENTY_YEARS,
    #                               frequency_type=Client.PriceHistory.FrequencyType.DAILY,
    #                               frequency=Client.PriceHistory.Frequency.DAILY)
    #resp = c.get_quotes("/BTC")
    resp = c.get_watchlists_for_single_account(275218956)
    if resp.status_code != 200:
        print(resp)
    history = resp.json()
    print(history)


    #calculate_apy(100, 200, 1)
    #test_tda()
    #get_instruments()
    #return

    #td_consumer_key = "GGMUX8J8AAA8JSOXXDGBCTGRBQO3SO5R"
#    endpoint = 'https://api.tdameritrade.com/v1/marketdata/quotes'
#    page = requests.get(url=endpoint,
#                        params={'apikey': td_consumer_key,
#                                'symbol': "/BTC"})
#    content = json.loads(page.content)
#    pprint.pprint(content)
