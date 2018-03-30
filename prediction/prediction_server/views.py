import arrow
from flask import request, jsonify

from prediction_server import app
from prediction_server.models import checkParameters


@app.route('/')
def index_page():
    return 'hello, world!'


@app.route('/api/v0.1.0/predict')
def predict():
    # check parameters
    check_result = checkParameters(
        request.args,
        ['symbol', 'term'],
        {
            'term': ['short', 'long']
        })
    if check_result:
        return jsonify(check_result)

    res = {
        'type': 'result',
        'result': {
            'symbol': request.args.get('symbol'),
            'predictPrice': 123.45,
            'predictTime': arrow.utcnow().isoformat(),
            'note': 'ONLY OFR TESTING!'
        }
    }

    return jsonify(res)
