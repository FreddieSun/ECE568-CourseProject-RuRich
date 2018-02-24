# -*- coding:utf-8 -*-
from sqlalchemy import Column, BIGINT, TEXT, NUMERIC
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class RealTimePrice(Base):
    __tablename__ = 'real_time'
    time_stamp = Column(BIGINT, primary_key=True, nullable=True)
    symbol = Column(TEXT, primary_key=True, nullable=True)
    price = Column(NUMERIC(1000, 4), nullable=True)
    volume = Column(BIGINT, nullable=True)



class DatabaseUtils(object):
    pass




class databaseUtil(object):

    @staticmethod
    def save_price(time_stamp, symbol, open_price, high_price, low_price, close_price, volume):
        pass


if __name__ == '__main__':
    # databaseUtil.save_price()
    pass
