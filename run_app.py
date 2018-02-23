# -*- coding:utf-8 -*-

import argparse

import get_stock_data

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('symbols', nargs='+')
    args = parser.parse_args()
    if args.symbols:
        get_stock_data.GetStockData.get_real_time_price(args.symbols)
