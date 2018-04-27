from pymongo import DESCENDING

from prediction_server import realtime, daily


# url = 'mongodb://{username}:{password}@{host}:{port}'.format(
#         username=app.config.get('MONGODB_USERNAME'),
#         password=app.config.get('MONGODB_PASSWORD'),
#         host=app.config.get('MONGODB_HOST'),
#         port=app.config.get('MONGODB_PORT')
#     )
#
# client = MongoClient(url)
# daily = client['ece568']['daily']
# realtime = client['ece568']['realtime']

def get_recent_price(symbol: str, n: int = 30):
    # url = 'mongodb://{username}:{password}@{host}:{port}'.format(
    #     username=app.config.get('MONGODB_USERNAME'),
    #     password=app.config.get('MONGODB_PASSWORD'),
    #     host=app.config.get('MONGODB_HOST'),
    #     port=app.config.get('MONGODB_PORT')
    # )
    #
    # client = MongoClient(url)
    # daily = client['ece568']['daily']

    ret = []
    for row in daily.find({'symbol': symbol}, {'_id': 0, 'symbol': 0}).sort([('timestamp', DESCENDING)]).limit(n):
        ret.append(row)
    return ret


def get_realtime_price(symbol: str, n: int = 30):
    # url = 'mongodb://{username}:{password}@{host}:{port}'.format(
    #     username=app.config.get('MONGODB_USERNAME'),
    #     password=app.config.get('MONGODB_PASSWORD'),
    #     host=app.config.get('MONGODB_HOST'),
    #     port=app.config.get('MONGODB_PORT')
    # )
    #
    # client = MongoClient(url)
    # realtime = client['ece568']['realtime']

    ret = []
    for row in realtime.find({'symbol': symbol}, {'_id': 0, 'symbol': 0}).sort([('timestamp', DESCENDING)]).limit(n):
        ret.append(row)
    return ret


def get_least_price(symbol: str):
    # url = 'mongodb://{username}:{password}@{host}:{port}'.format(
    #     username=app.config.get('MONGODB_USERNAME'),
    #     password=app.config.get('MONGODB_PASSWORD'),
    #     host=app.config.get('MONGODB_HOST'),
    #     port=app.config.get('MONGODB_PORT')
    # )
    #
    # client = MongoClient(url)
    # realtime = client['ece568']['realtime']

    return realtime.find({'symbol': symbol}, {'price': 1, '_id': 0}).sort([('timestamp', DESCENDING)]).limit(1)[0][
        'price']


def get_all_symbol():
    # url = 'mongodb://{username}:{password}@{host}:{port}'.format(
    #     username=app.config.get('MONGODB_USERNAME'),
    #     password=app.config.get('MONGODB_PASSWORD'),
    #     host=app.config.get('MONGODB_HOST'),
    #     port=app.config.get('MONGODB_PORT')
    # )
    #
    # client = MongoClient(url)
    # daily = client['ece568']['daily']

    ret = []

    for row in daily.aggregate([{'$group': {'_id': '$symbol'}}, {'$sort': {'_id': 1}}]):
        ret.append(row['_id'])

    return ret


def get_max(symbol: str):
    ret = []

    for row in daily.aggregate([
        {'$match': {'symbol': symbol}},
        {'$sort': {'timestamp': -1}},
        {'$limit': 10},
        {'$group': {'_id': 0, 'max': {'$max': '$high'}}}
    ]):
        ret.append(row['max'].to_decimal())

    return ret[0]


def get_min(symbol: str):
    ret = []

    for row in daily.aggregate([
        {'$match': {'symbol': symbol}},
        {'$sort': {'timestamp': -1}},
        {'$limit': 252},
        {'$group': {'_id': 0, 'min': {'$min': '$low'}}}
    ]):
        ret.append(row['min'].to_decimal())

    return ret[0]


def get_avg(symbol: str):
    ret = []

    for row in daily.aggregate([
        {'$match': {'symbol': symbol}},
        {'$sort': {'timestamp': -1}},
        {'$limit': 252},
        {'$group': {'_id': 0, 'avg': {'$avg': '$close'}}}
    ]):
        ret.append(row['avg'].to_decimal())

    return ret[0]


def get_lower_avg(symbol: str):
    symbols = get_all_symbol()
    min = get_min(symbol)

    ret = []
    for s in symbols:
        if get_avg(s) < min:
            ret.append(s)

    return ret
