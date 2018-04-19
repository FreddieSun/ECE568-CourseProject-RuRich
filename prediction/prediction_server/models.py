from typing import List, Dict, Union

import arrow
from pymongo import MongoClient, DESCENDING
from werkzeug.datastructures import ImmutableMultiDict

from prediction_server import app
from prediction_server import error_code


def checkParameters(
        args: ImmutableMultiDict,
        parametersList: List[str],
        parameterType: Dict[str, List[type]] = None,
        parameterOptions: Dict[str, List[str]] = None):
    if parameterOptions is None:
        parameterOptions = {}

    missing_parameter = []
    for parameter in parametersList:
        if parameter not in args:
            missing_parameter.append(parameter)
    if missing_parameter:
        return {
            'type': 'error',
            'time': arrow.utcnow().isoformat(),
            'error': {
                'errorCode': error_code.ERROR_CODE_MISSING_PARAMETERS,
                'errorInfo': 'Missing parameters',
                'missingParameters': missing_parameter
            }
        }

    invalid_type_parameters = []
    for k, v in parameterType.items():
        if type(args.get(k)) not in v:
            invalid_type_parameters.append(k)
    if invalid_type_parameters:
        return {
            'type': 'error',
            'time': arrow.utcnow().isoformat(),
            'error': {
                'errorCode': error_code.ERROR_CODE_INVALID_PARAMETERS_TYPE,
                'errorInfo': 'Invalid parameter type',
                'invalidParametersType': [{'parameter': ele, 'types': [e.__name__ for e in parameterType[ele]]} for ele
                                          in invalid_type_parameters]
            }
        }

    invalid_parameter = []
    for k, v in parameterOptions.items():
        if args.get(k) not in v:
            invalid_parameter.append(k)
    if invalid_parameter:
        return {
            'type': 'error',
            'time': arrow.utcnow().isoformat(),
            'error': {
                'errorCode': error_code.ERROR_CODE_INVALID_PARAMETERS,
                'errorInfo': 'Invalid parameter value',
                'invalidParameters': invalid_parameter
            }
        }

    return None


def checkSymbol(symbol: str):
    url = 'mongodb://{username}:{password}@{host}:{port}'.format(
        username=app.config.get('MONGODB_USERNAME'),
        password=app.config.get('MONGODB_PASSWORD'),
        host=app.config.get('MONGODB_HOST'),
        port=app.config.get('MONGODB_PORT')
    )

    client = MongoClient(url)
    daily = client['ece568']['daily']

    if symbol not in [ele['_id'] for ele in daily.aggregate([{"$group": {"_id": "$symbol"}}])]:
        return {
            'type': 'error',
            'time': arrow.utcnow().isoformat(),
            'error': {
                'errorCode': error_code.ERROR_CODE_INVALID_SYMBOL,
                'errorInfo': 'Invalid symbol'
            }
        }
    return None


def getDailyData(symbol: str, n: int = 50) -> Dict[str, List[Union[float, int]]]:
    url = 'mongodb://{username}:{password}@{host}:{port}'.format(
        username=app.config.get('MONGODB_USERNAME'),
        password=app.config.get('MONGODB_PASSWORD'),
        host=app.config.get('MONGODB_HOST'),
        port=app.config.get('MONGODB_PORT')
    )

    client = MongoClient(url)
    daily = client['ece568']['daily']

    timestamp = []
    open_ = []
    close = []
    high = []
    low = []
    volume = []

    for row in daily.find({'symbol': symbol}, {'_id': 0.0}).sort(
            [('timestamp', DESCENDING), ]).limit(n):
        timestamp.append(row['timestamp'].timestamp())
        open_.append(float(row['open'].to_decimal()))
        close.append(float(row['close'].to_decimal()))
        high.append(float(row['high'].to_decimal()))
        low.append(float(row['low'].to_decimal()))
        volume.append(row['volume'])

    return {
        'timestamp': timestamp[::-1],
        'open': open_[::-1],
        'close': close[::-1],
        'high': high[::-1],
        'low': low[::-1],
        'volume': volume[::-1]
    }


def getRealtimeData(symbol: str, n: int = 50) -> Dict[str, List[Union[float, int]]]:
    url = 'mongodb://{username}:{password}@{host}:{port}'.format(
        username=app.config.get('MONGODB_USERNAME'),
        password=app.config.get('MONGODB_PASSWORD'),
        host=app.config.get('MONGODB_HOST'),
        port=app.config.get('MONGODB_PORT')
    )

    client = MongoClient(url)
    realtime = client['ece568']['realtime']

    timestamp = []
    price = []
    volume = []

    for row in realtime.find({'symbol': symbol}, {'_id': 0.0}).sort(
            [('timestamp', DESCENDING), ]).limit(n):
        timestamp.append(row['timestamp'].timestamp())
        price.append(float(row['price'].to_decimal()))
        volume.append(row['volume'])

    return {
        'timestamp': timestamp[::-1],
        'price': price[::-1],
        'volume': volume[::-1]
    }
