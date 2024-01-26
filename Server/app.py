from flask import Flask, request, jsonify
from flask_socketio import SocketIO
import os

import pt_autofill

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

pt_autofill.set_socketio_instance(socketio)


@socketio.on('connect')
def handle_connect():
    print('Client connected')


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


@app.route('/run_script', methods=['POST'])
def run_script():
    data = request.json
    clinic_name = data['clinicName']
    username = data['username']
    password = data['password']
    num_of_pts = data['numOfPts']

    if pt_autofill.run(clinic_name, username, password, num_of_pts):
        return jsonify({"status": "Successfully Completed"})
    else:
        return jsonify({"Error": "Oops"})


if __name__ == '__main__':
    # Updated to use PORT environment variable
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port)
