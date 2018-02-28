# -*- coding:utf-8 -*-
import os
from typing import Union, List

import arrow
import requests
from bson.decimal128 import Decimal128
from bson.int64 import Int64
from pymongo import MongoClient, DESCENDING, TEXT


def get_env(env: str) -> str:
    api_key = os.getenv(env)
    if api_key is None:
        raise EnvironmentError
    return api_key


def get_daily_data(symbol: Union[str, List[str]]):
    if isinstance(symbol, str):
        symbol = [symbol, ]

    URL = 'https://www.alphavantage.co/query'
    if not symbol:
        raise ValueError

    if isinstance(symbol, str):
        symbol = [symbol, ]

    retList = []
    for s in symbol:
        res = requests.get(URL,
                           params={
                               'function': 'TIME_SERIES_DAILY',
                               'symbol': s,
                               'outputsize': 'full',  # full, compact
                               'apikey': get_env('ALPHAVANTAG_API_KEY')
                           })

        j = res.json()
        tz = j['Meta Data']['5. Time Zone']
        for d, info in j['Time Series (Daily)'].items():
            tmpDict = {}
            tmpDict['timestamp'] = arrow.get(d).replace(tzinfo=tz).datetime
            tmpDict['symbol'] = s
            tmpDict['open'] = Decimal128(info['1. open'])
            tmpDict['high'] = Decimal128(info['2. high'])
            tmpDict['low'] = Decimal128(info['3. low'])
            tmpDict['close'] = Decimal128(info['4. close'])
            tmpDict['volume'] = Int64(info['5. volume'])
            retList.append(tmpDict)
    return retList


def init_db(symbols: Union[str, List[str]]):
    client = MongoClient(
        'mongodb://{0}:{1}@{2}/'.format(get_env('MONGO_INITDB_ROOT_USERNAME'), get_env('MONGO_INITDB_ROOT_PASSWORD'),
                                        get_env('MONGO_HOST')))
    db = client['ece568']

    if db['flag'].find({'init': True}).count() != 0:
        return

    db['daily'].drop()
    db['realtime'].drop()
    db['flag'].drop()

    db.create_collection('daily', validator={'$jsonSchema': {
        'bsonType': 'object',
        'required': ['timestamp', 'symbol', 'open', 'high', 'low', 'close', 'volume'],
        'properties': {
            'timestamp': {
                'bsonType': 'date',
                'description': 'all time points are in UTC, please convert to local timezone before use'
            },
            'symbol': {
                'bsonType': 'string'
            },
            'open': {
                'bsonType': 'decimal'
            },
            'high': {
                'bsonType': 'decimal'
            },
            'low': {
                'bsonType': 'decimal'
            },
            'close': {
                'bsonType': 'decimal'
            },
            'volume': {
                'bsonType': 'long'
            }
        }
    }})
    db.create_collection('realtime', validator={'$jsonSchema': {
        'bsonType': 'object',
        'required': ['timestamp', 'symbol', 'price', 'volume'],
        'properties': {
            'timestamp': {
                'bsonType': 'date',
                'description': 'all time points are in UTC, please convert to local timezone before use'
            },
            'symbol': {
                'bsonType': 'string'
            },
            'price': {
                'bsonType': 'decimal'
            },
            'volume': {
                'bsonType': 'long'
            }
        }
    }})

    db['daily'].create_index([('timestamp', DESCENDING), ('symbol', TEXT)], unique=True, background=True)
    db['realtime'].create_index([('timestamp', DESCENDING), ('symbol', TEXT)], unique=True, background=True)

    for stock in symbols:
        db['daily'].insert_many(get_daily_data(stock))
    db['flag'].insert_one({'init': True})


if __name__ == '__main__':
    init_db(['GOOG', 'AABA', 'FB', 'MSFT', 'TWTR', 'AAPL', 'JPM', 'AMZN', 'JNJ', 'BAC'])
