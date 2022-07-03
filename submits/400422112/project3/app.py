from flask import Flask, request, jsonify
from utils.common import response_message, create_response
from utils.interpolation import miladi, shamsi
from utils.outlier import time_series, vanilla
from utils.imbalance import handle_imbalance
import json

app = Flask(__name__)

@app.route('/', methods=['GET'])
def isup():
    return response_message('API is active...')


@app.route('/service1', methods=['POST'])
def service1():
    req = request.get_json()
    data = req['data']

    config = req['config']
    config['service'] = 1

    if config['type'] == 'miladi':
        result = miladi(data, config)
        return jsonify(json.loads(create_response(result)))

    elif config['type'] == 'shamsi':
        result = shamsi(data, config)
        return jsonify(json.loads(create_response(result)))


@app.route('/service2', methods=['POST'])
def service2():
    req = request.get_json()
    data = req['data']

    config = req['config']
    config['service'] = 2

    result = shamsi(data, config)
    return jsonify(json.loads(create_response(result)))


@app.route('/service3', methods=['POST'])
def service3():
    req = request.get_json()
    data = req['data']

    is_time_series = req['config']['time_series']

    if 'z_score' in req['config'].keys():
        z_score = req['config']['z_score']
    else:
        z_score = 3

    if is_time_series:
        result = time_series(data)
    else:
        result = vanilla(data, z_score)
    return jsonify(json.loads(create_response(result)))


@app.route('/service4', methods=['POST'])
def service4():
    req = request.get_json()
    data = req['data']

    method = req['config']['method']
    result = handle_imbalance(data, method)
    return jsonify(json.loads(create_response(result)))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
