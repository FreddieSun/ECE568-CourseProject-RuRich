# -*- coding:utf-8 -*-

import argparse

from apscheduler.schedulers.blocking import BlockingScheduler

from get_stock_data import GetStockData

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('symbols', nargs='+')
    args = parser.parse_args()
    print(args.symbols)
    if args.symbols:
        GetStockData.get_real_time_price(args.symbols)

    scheduler = BlockingScheduler()
    scheduler.add_job(GetStockData.get_real_time_price, 'interval', seconds=5, args=[args.symbols, ])
    scheduler.add_job(GetStockData.get_daily_data, 'interval', days=1, args=[args.symbols, ])
    try:
        scheduler.start()
    except SystemExit:
        pass
