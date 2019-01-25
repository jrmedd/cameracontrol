import binascii

import os

from flask import Flask, render_template

from flask_socketio import SocketIO

import serial

APP = Flask(__name__)

SOCKETIO = SocketIO(APP)

APP.secret_key = os.environ.get('SECRET_KEY')

COMMANDS = {'up': '8101060psts10301ff',
            'down': '8101060psts10302ff',
            'left': '8101060psts10103ff',
            'right': '8101060psts10203ff',
            'zoom-in': '8101040725ff',
            'zoom-out': '8101040735ff',
            'p-stop': '8101060103030303ff',
            'z-stop': '8101040700ff'}

CAMERA = serial.Serial('/dev/ttyS0')

@APP.route('/')
def index():
    return render_template('index.html')

@SOCKETIO.on('control', namespace='/camera')
def translate_control(data):
    direction = data.get('command')
    command = COMMANDS.get(direction)
    if data.get('speed'):
        speed = "%X" % (data.get('speed'))
        speed = "0" + speed if len(speed) < 2 else speed
        command = command.replace('ps', speed).replace('ts', speed)
    CAMERA.write(binascii.unhexlify(command))

if __name__ == '__main__':
    SOCKETIO.run(APP)
