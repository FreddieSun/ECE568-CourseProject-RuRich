# -*- coding:utf-8 -*-

import argparse
from typing import Union, List

from apscheduler.schedulers.blocking import BlockingScheduler

from database_utils import DatabaseUtils
from get_stock_data import GetStockData
from initdb import init_db


def updateRealtime(symbols: Union[str, List[str]]):
    DatabaseUtils.save_realtime(GetStockData.get_real_time_price(symbols))


def updateDaily(symbols: Union[str, List[str]]):
    DatabaseUtils.save_daily_history(GetStockData.get_daily_data(symbols))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('symbols', nargs='+')
    args = parser.parse_args()
    print(args.symbols)

    init_db(args.symbols)


    scheduler = BlockingScheduler()
    scheduler.add_job(updateRealtime, 'interval', seconds=5, args=[args.symbols, ])
    scheduler.add_job(updateDaily, 'interval', days=1, args=[args.symbols, ])
    try:
        scheduler.start()
    except SystemExit:
        pass
