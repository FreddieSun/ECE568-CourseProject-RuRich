# -*- coding:utf-8 -*-
import psycopg2


class DatabaseUtils(object):
    pass


conn = psycopg2.connect(dbname='ECE568', host='localhost', user='postgres', password='zhuzzc2008zzczhu')

cur = conn.cursor()


class databaseUtil(object):

    @staticmethod
    def save_price(time_stamp, symbol, open_price, high_price, low_price, close_price, volume):
        pass


if __name__ == '__main__':
    # databaseUtil.save_price()
    pass
