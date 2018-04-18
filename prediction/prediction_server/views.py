import random

import arrow
from flask import request, jsonify

from prediction_server import app
from prediction_server.jsonp import jsonp
from prediction_server.models import checkParameters


@app.route('/')
def index_page():
    return 'hello, world!'


@app.route('/api/v0.1.0/vr')
@jsonp
def indicator():
    check_result = checkParameters(
        args=request.args,
        parametersList=['timestamp', 'symbol'],
        parameterType={
            'timestamp': [str, ],
            'symbol': [str, ]
        }
    )
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
        parametersList=['symbol', 'term'],
        parameterType={
            'symbol': [str, ],
            'term': [str, ]
        },
        parameterOptions={
            'term': ['short', 'long']
        })

    if check_result:
        return jsonify(check_result)

    res = {
        'type': 'result',
        'time': arrow.utcnow().isoformat(),
        'result': {
            'symbol': request.args.get('symbol'),
            'predictPrice': int(random.random() * 100000) / 100,
            'note': 'ONLY OFR TESTING!'
        }
    }
    return jsonify(res)
