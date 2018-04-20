import arrow
import numpy as np
from flask import request, jsonify

from prediction_engine.bayes import Bayes
from prediction_engine.svr_zhu import SupportVectorRegression
from prediction_engine.vr import VolatilityRatio
from prediction_server import app
from prediction_server.jsonp import jsonp
from prediction_server.models import checkParameters, getDailyData, \
    checkSymbol, getRealtimeData, checkDate, checkTimestamp


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

    return jsonify(getDailyData(request.args['symbol'], request.args.get('timestamp', None)))


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

    check_result = checkTimestamp(request.args['timestamp'])
    if check_result:
        return jsonify(check_result)

    check_result = checkDate(request.args['symbol'], request.args['timestamp'])
    if check_result:
        return jsonify(check_result)

    # timestamp = arrow.get(request.args.get('timestamp', 0))
    # data_list = []

    period = int(request.args.get('period', 24))

    r = getDailyData(request.args['symbol'], request.args['timestamp'], period + 1)

    res = {
        'type': 'result',
        'time': arrow.utcnow().isoformat(),
        'result': {
            'symbol': request.args.get('symbol', 'ERROR'),
            'indicator': 'VR',
            'timestamp': arrow.get(request.args['timestamp']).isoformat(),
            'data': VolatilityRatio.indicator(
                price=np.float_(r['close'][-1]),
                historical_price=np.array(r['close'][:-1]),
                historical_volume=np.array(r['volume'][:-1])
            )
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

    check_result = checkTimestamp(request.args['timestamp'])
    if check_result:
        return jsonify(check_result)

    # request.args.get('timestamp')

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
            'predictPrice': (bayes[0] + svr[0]) / 2,
            'predictor': [
                {'name': 'bayes', 'price': bayes[0]},
                {'name': 'Support Vector Regression', 'price': svr[0]}
            ],
            'note': 'ONLY OFR TESTING!',
            'timestamp': arrow.get(request.args['timestamp']).isoformat()
        }
    }
    return jsonify(res)
