import random

import arrow
import numpy as np
from flask import request, jsonify

from prediction_engine.bayes import Bayes
from prediction_engine.svr_zhu import SupportVectorRegression
from prediction_server import app
from prediction_server.jsonp import jsonp
from prediction_server.models import checkParameters, getDailyData, checkSymbol, getRealtimeData


@app.route('/')
def index_page():
    return 'hello, world!'


@app.route('/api/v0.0.1/test/daily')
def daily_data():
    check_result = checkParameters(
        args=request.args,
        parametersList=['symbol', ],
    )
    if check_result:
        return jsonify(check_result)

    check_result = checkSymbol(request.args['symbol'])
    if check_result:
        return jsonify(check_result)

    return jsonify(getDailyData(request.args['symbol']))


@app.route('/api/v0.0.1/test/realtime')
def realtime_data():
    check_result = checkParameters(
        args=request.args,
        parametersList=['symbol', ],
    )
    if check_result:
        return jsonify(check_result)

    check_result = checkSymbol(request.args['symbol'])
    if check_result:
        return jsonify(check_result)

    return jsonify(getRealtimeData(request.args['symbol']))






@app.route('/api/v0.1.0/vr')
@jsonp
def indicator():
    check_result = checkParameters(
        args=request.args,
        parametersList=['timestamp', 'symbol'],
    )
    if check_result:
        return jsonify(check_result)

    check_result = checkSymbol(request.args['symbol'])
    if check_result:
        return jsonify(check_result)

    # timestamp = arrow.get(request.args.get('timestamp', 0))
    # data_list = []

    # TODO

    try:
        timestamp = arrow.get(request.args.get('timestamp', 0))
    except:
        return jsonify({
            'type': 'error',
            'time': arrow.utcnow().isoformat(),
            'error': {
                'errorCode': 103,
                'errorInfo': 'please use ISO8601 format'
            }
        })

    res = {
        'type': 'result',
        'time': arrow.utcnow().isoformat(),
        'result': {
            'symbol': request.args.get('symbol', 'ERROR'),
            'indicator': 'VR',
            'timestamp': timestamp.isoformat(),
            'data': int(random.random() * 100000) / 100
        }
    }

    return jsonify(res)


@app.route('/api/v0.1.0/predict')
@jsonp
def predict():
    # check parameters
    check_result = checkParameters(
        args=request.args,
        parametersList=['symbol', 'term', 'timestamp'],
        parameterOptions={
            'term': ['short', 'long']
        })

    if check_result:
        return jsonify(check_result)

    check_result = checkSymbol(request.args['symbol'])
    if check_result:
        return jsonify(check_result)

    # ------------------------------------
    if request.args['term'] == 'short':
        r = getRealtimeData(request.args['symbol'], request.args['timestamp'])
        time = np.array(r['timestamp']).reshape(-1, 1)
        price = np.array(r['price'])
    else:
        r = getDailyData(request.args['symbol'], request.args['timestamp'])
        time = np.array(r['timestamp']).reshape(-1, 1)
        price = np.array(r['open'])

    predict_time = arrow.get(request.args['timestamp']).timestamp

    bayes = Bayes.predict(time, price, np.array(predict_time).reshape(-1, 1))
    svr = SupportVectorRegression.predict(time, price, np.array(predict_time).reshape(-1, 1))




    res = {
        'type': 'result',
        'time': arrow.utcnow().isoformat(),
        'result': {
            'symbol': request.args.get('symbol'),
            'predictPrice': int(random.random() * 100000) / 100,
            'predictor': [
                {'name': 'bayes', 'price': bayes[0]},
                {'name': 'Support Vector Regression', 'price': svr[0]}
            ],
            'note': 'ONLY OFR TESTING!',
            'timestamp': arrow.get(request.args['timestamp']).isoformat()
        }
    }
    return jsonify(res)
