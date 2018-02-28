# -*- coding:utf-8 -*-
from typing import Union, List

import arrow
import requests
from bson.decimal128 import Decimal128
from bson.int64 import Int64
from pymongo import MongoClient, DESCENDING

from utils import Utils


def get_daily_data(symbol: Union[str, List[str]]):
    if not symbol:
        raise ValueError

    if isinstance(symbol, str):
        symbol = [symbol, ]

    url = 'https://www.alphavantage.co/query'
    if not symbol:
        raise ValueError

    if isinstance(symbol, str):
        symbol = [symbol, ]

    ret_list = []
    for s in symbol:
        res = requests.get(url,
                           params={
                               'function': 'TIME_SERIES_DAILY',
                               'symbol': s,
                               'outputsize': 'full',  # full, compact
                               'apikey': Utils.get_env('ALPHAVANTAG_API_KEY')
                           })

        j = res.json()
        tz = j['Meta Data']['5. Time Zone']
        for d, info in j['Time Series (Daily)'].items():
            tmp_dict = {'timestamp': arrow.get(d).replace(tzinfo=tz).datetime,
                        'symbol': s,
                        'open': Decimal128(info['1. open']),
                        'high': Decimal128(info['2. high']),
                        'low': Decimal128(info['3. low']),
                        'close': Decimal128(info['4. close']),
                        'volume': Int64(info['5. volume'])}
            ret_list.append(tmp_dict)
    return ret_list


def init_db(symbols: Union[str, List[str]]):
    client = MongoClient(
        'mongodb://{0}:{1}@{2}/'.format(Utils.get_env('MONGO_INITDB_ROOT_USERNAME'),
                                        Utils.get_env('MONGO_INITDB_ROOT_PASSWORD'), Utils.get_env('MONGO_HOST')))
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

    db['daily'].create_index([('timestamp', DESCENDING), ('symbol', DESCENDING)], unique=True, background=True)
    db['daily'].create_index([('symbol', DESCENDING), ('timestamp', DESCENDING)], unique=True, background=True)
    db['realtime'].create_index([('timestamp', DESCENDING), ('symbol', DESCENDING)], unique=True, background=True)
    db['realtime'].create_index([('symbol', DESCENDING), ('timestamp', DESCENDING)], unique=True, background=True)

    for stock in symbols:
        db['daily'].insert_many(get_daily_data(stock))
    db['flag'].insert_one({'init': True})


if __name__ == '__main__':
    init_db(['GOOG', 'AABA', 'FB', 'MSFT', 'TWTR', 'AAPL', 'JPM', 'AMZN', 'JNJ', 'BAC'])
