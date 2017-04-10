from flask import Flask, jsonify, abort
from flask import make_response, request
import json, codecs
from flask.ext.httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

try:
    with open('devices.txt') as file:
        devices = json.load(file)
except ValueError:
    devices = {}
    devices['devices'] = []

@auth.get_password
def get_password(username):
    if username == 'rohan':
        return 'iot'
    return None

@app.route('/')
def index():
    return "IOT Project Home"

@app.route('/devices', methods=['GET'])
@auth.login_required
def get_devices():
    return jsonify({'devices': devices })

@app.route('/devices/<int:device_id>', methods=['GET'])
def get_device(device_id):
    device = [device for device in devices['devices']
            if device['ID'] == device_id]
    if len(device) == 0:
        abort(404)
    return jsonify({'device': device[0]})

@app.route('/devices/', methods = ['POST'])
def create_device():
    if not request.json or not 'Title' in request.json or not 'Location' in request.json:
        abort(400)
    new_device = {
            'ID': len(devices['devices'])+1,
            'Title': request.json['Title'],
            'Location': request.json['Location'],
            'Status': False
            }
    devices['devices'].append(new_device)
    with open('devices.txt', 'wb') as file:
        json.dump(devices, codecs.getwriter('utf-8')(file), ensure_ascii = False)
    return jsonify({'New Device': new_device}), 201

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/devices/<int:device_id>', methods = ['PUT'])
def update_device(device_id):
    device = [device for device in devices['devices'] if device['ID'] == device_id]
    if len(device) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'Title' in request.json and type(request.json['Title']) is not str:
        abort(400)
    if 'Location' in request.json and type(request.json['Location']) is not str:
        abort(400)
    device[0]['Title'] = request.json.get('Title', device[0]['Title'])
    device[0]['Location'] = request.json.get('Location', device[0]['Location'])
    with open('devices.txt', 'wb') as file:
        json.dump(devices, codecs.getwriter('utf-8')(file), ensure_ascii = False)
    return jsonify({'Modified Device': device[0]})

@app.route('/devices/<int:device_id>', methods=['DELETE'])
def delete_device(device_id):
    device = [device for device in devices['devices'] if device['ID'] == device_id]
    if len(device) == 0:
        abort(404)
    devices['devices'].remove(device[0])
    with open('devices.txt', 'wb') as file:
        json.dump(devices, codecs.getwriter('utf-8')(file),ensure_ascii = False)
    return jsonify({'result':True})

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Incomplete Parameter'}), 400)

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 80, debug=True)