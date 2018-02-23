# -*- coding:utf-8 -*-

import os
import json
from typing import List

import requests


class GetStockData(object):
    URL = 'https://www.alphavantage.co/query'

    @staticmethod
    def get_api_key() -> str:
        api_key = os.getenv('ALPHAVANTAG_API_KEY')
        if api_key is None:
            raise EnvironmentError
        return api_key


    @staticmethod
    def get_daily_data(symbol: str):
        if not symbol:
            raise ValueError
        res = requests.get(GetStockData.URL,
                           params={
                               'function': 'TIME_SERIES_DAILY',
                               'symbol': symbol,
                               'outputsize': 'full',
                               'apikey': GetStockData.get_api_key()
                           })
        print(json.dumps(res.json(), indent=1))

    @staticmethod
    def get_real_time_price(symbols: List[str] = None):
        if symbols is None:
            symbols = ['MSFT', 'FB', 'AAPL', 'GOOG']
        res = requests.get(GetStockData.URL,
                           params={
                               'function': 'BATCH_STOCK_QUOTES',
                               'symbols': ','.join(symbols),
                               'apikey': GetStockData.get_api_key()
                           })
        print(json.dumps(res.json(), indent=1))


if __name__ == '__main__':
    # GetStockData.get_daily_data('GOOG')
    GetStockData.get_real_time_price(['GOOG'])