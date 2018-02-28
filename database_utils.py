# -*- coding:utf-8 -*-
import os
from typing import List

from pymongo import MongoClient


class Utils(object):
    @staticmethod
    def get_env(env: str) -> str:
        api_key = os.getenv(env)
        if api_key is None:
            raise EnvironmentError
        return api_key

class DatabaseUtils(object):
    client = MongoClient('mongodb://{0}:{1}@{2}/'.format(Utils.get_env('MONGO_INITDB_ROOT_USERNAME'),
                                                         Utils.get_env('MONGO_INITDB_ROOT_PASSWORD'),
                                                         Utils.get_env('MONGO_HOST')))
    db = client['ece568']

    @classmethod
    def save_daily_history(cls, insert_list: List):
        col = cls.db['daily']
        for doc in insert_list:
            col.update_many(
                {'timestamp': doc['timestamp'],
                 'symbol': doc['symbol']},
                {'$set': doc},
                upsert=True
            )

    @classmethod
    def save_realtime(cls, insert_list: List):
        col = cls.db['realtime']
        for doc in insert_list:
            col.update_many(
                {'timestamp': doc['timestamp'],
                 'symbol': doc['symbol']},
                {'$set': doc},
                upsert=True
            )


if __name__ == '__main__':
    from get_stock_data import GetStockData

    DatabaseUtils.save_daily_history(GetStockData.get_daily_data('GOOG'))
