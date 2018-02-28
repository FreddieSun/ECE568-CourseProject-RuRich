# -*- coding:utf-8 -*-

import os
from typing import List, Union

import arrow
import requests
from bson.decimal128 import Decimal128
from bson.int64 import Int64


class GetStockData(object):
    URL = 'https://www.alphavantage.co/query'

    @staticmethod
    def get_api_key() -> str:
        api_key = os.getenv('ALPHAVANTAG_API_KEY')
        if api_key is None:
            raise EnvironmentError
        return api_key

    @staticmethod
    def get_daily_data(symbols: Union[str, List[str]]):
        if not symbols:
            raise ValueError

        if isinstance(symbols, str):
            symbols = [symbols, ]

        retList = []
        for s in symbols:
            res = requests.get(GetStockData.URL,
                               params={
                                   'function': 'TIME_SERIES_DAILY',
                                   'symbols': s,
                                   'outputsize': 'compact',  # full, compact
                                   'apikey': GetStockData.get_api_key()
                               })

            j = res.json()
            tz = j['Meta Data']['5. Time Zone']
            for d, info in j['Time Series (Daily)'].items():
                tmpDict = {}
                tmpDict['timestamp'] = arrow.get(d).replace(tzinfo=tz).datetime
                tmpDict['symbols'] = s
                tmpDict['open'] = Decimal128(info['1. open'])
                tmpDict['high'] = Decimal128(info['2. high'])
                tmpDict['low'] = Decimal128(info['3. low'])
                tmpDict['close'] = Decimal128(info['4. close'])
                tmpDict['volume'] = Int64(info['5. volume'])
                retList.append(tmpDict)
        return retList

    @staticmethod
    def get_real_time_price(symbols: Union[str, List[str]] = None):
        if symbols is None:
            return []
        if isinstance(symbols, str):
            symbols = [symbols, ]

        res = requests.get(GetStockData.URL,
                           params={
                               'function': 'BATCH_STOCK_QUOTES',
                               'symbols': ','.join(symbols),
                               'apikey': GetStockData.get_api_key()
                           })
        j = res.json()
        tz = j['Meta Data']['3. Time Zone']
        retList = []
        for info in j['Stock Quotes']:
            tmpDict = {}
            tmpDict['timestamp'] = arrow.get(info['4. timestamp']).replace(tzinfo=tz).datetime
            tmpDict['symbol'] = info['1. symbol']
            tmpDict['price'] = Decimal128(info['2. price'])
            try:
                tmpDict['volume'] = Int64(info['3. volume'])
            except:
                tmpDict['volume'] = Int64(0)
            retList.append(tmpDict)

        return retList


if __name__ == '__main__':
    print(GetStockData.get_real_time_price('GOOG'))
