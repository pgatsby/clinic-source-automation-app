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
    # pt_autofill.driver.quit()


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    clinic_name = data['clinicName']
    username = data['username']
    password = data['password']

    login_successful = pt_autofill.login(clinic_name, username, password)
    if login_successful:
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "failure"})


@app.route('/get_patient_names', methods=['GET'])
def get_patient_names():
    patient_names = pt_autofill.get_pt_names()

    if patient_names is not None:
        return jsonify({"patientNames": patient_names})
    else:
        return jsonify({"error": "Failed to retrieve patient names"}), 500


@app.route('/run_script', methods=['POST'])
def run_script():
    data = request.json
    pt_name = data['ptName']
    num_of_notes = data['numOfNotes']

    if pt_autofill.run(num_of_notes, pt_name):
        return jsonify({"status": "Successfully Completed"})
    else:
        return jsonify({"Error": "Failed to run"})


if __name__ == '__main__':
    # Updated to use PORT environment variable
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port)
