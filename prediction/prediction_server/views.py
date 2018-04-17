import arrow
from flask import request, jsonify

from prediction_server import app
from prediction_server.jsonp import jsonp
from prediction_server.models import checkParameters


@app.route('/')
def index_page():
    return 'hello, world!'


@app.route('/api/v0.1.0/predict')
@jsonp
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
        'time': arrow.utcnow().isoformat(),
        'result': {
            'symbol': request.args.get('symbol'),
            'predictPrice': 123.45,
            'note': 'ONLY OFR TESTING!'
        }
    }
    return jsonify(res)
