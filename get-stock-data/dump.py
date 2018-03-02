# -*- coding:utf-8 -*-
import csv
import datetime
from typing import List, Dict, Union

import arrow
from bson import Decimal128, Int64

from database_utils import DatabaseUtils


def save_to_csv(symbol: str, suffix: str, l: List[Dict[str, Union[datetime.datetime, str, Decimal128, Int64]]]):
    if l is None:
        return
    with open('dump_{}_{}_{}Z.csv'.format(symbol, suffix, arrow.get().format('YYYYMMDDTHHmmss')), 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=l[0].keys(), extrasaction='ignore')

        writer.writeheader()
        writer.writerows(l)


if __name__ == '__main__':

    for symbol in DatabaseUtils.get_daily_history_symbols():
        save_to_csv(symbol, 'daily', DatabaseUtils.get_daily_history_by_symbol(symbol))
    for symbol in DatabaseUtils.get_realtime_symbols():
        save_to_csv(symbol, 'realtime', DatabaseUtils.get_realtime_by_symbol(symbol))
