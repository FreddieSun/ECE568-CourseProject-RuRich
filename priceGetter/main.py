# -*- coding:utf-8 -*-
#!/usr/bin/python

import requests

URL = 'https://www.alphavantage.co/query'
with open('apikey', 'r') as f:
    apikey = f.read()


def get_real_time(symbol):
    func = 'TIME_SERIES_INTRADAY'
    interval = '1min'
    outputsize = 'compact'
    r = requests.get(URL,
                     params={
                        'function': func,
                        'symbol': symbol,
                        'interval': interval,
                        'outputsize': outputsize,
                        'apikey': apikey
                     })
    print(r.json())
    print(type(r.json()))


def get_history(symbol):
    func = 'TIME_SERIES_DAILY'
    outputsize = 'compact'
    r = requests.get(URL,
                     params={
                         'function': func,
                         'symbol': symbol,
                         'outputsize': outputsize,
                         'apikey': apikey
                     })
    print(r.json())


if __name__ == "__main__":
    get_real_time('GOOG')