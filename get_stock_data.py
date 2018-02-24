# -*- coding:utf-8 -*-

import json
import os
from typing import List, Union

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
    def get_daily_data(symbol: Union[str, List[str]]):
        if not symbol:
            raise ValueError

        if isinstance(symbol, str):
            symbol = list(symbol)

        for s in symbol:
            res = requests.get(GetStockData.URL,
                               params={
                                   'function': 'TIME_SERIES_DAILY',
                                   'symbol': s,
                                   'outputsize': 'full',
                                   'apikey': GetStockData.get_api_key()
                               })
            print(json.dumps(res.json(), indent=1))

    @staticmethod
    def get_real_time_price(symbols: List[str] = None):
        if symbols is None:
            # symbols = ['MSFT', 'FB', 'AAPL', 'GOOG']
            return

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