#!/usr/bin/python
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import atexit
from flask import Flask, request, redirect, render_template

# create object and set address for I2C
motorhat = Adafruit_MotorHAT(addr=0x60)

# create DC motor objects for driving and steering
frontDriveMotor = motorhat.getMotor(3)
rearDriveMotor = motorhat.getMotor(2)
turnMotor = motorhat.getMotor(1)

# set speed of motors
rearDriveMotor.setSpeed(255)
frontDriveMotor.setSpeed(200)
turnMotor.setSpeed(255)

# stop motors
def turnOffMotors():
    motorhat.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    motorhat.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    motorhat.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    motorhat.getMotor(4).run(Adafruit_MotorHAT.RELEASE)
atexit.register(turnOffMotors)

# move forward
def goForward():
    frontDriveMotor.run(Adafruit_MotorHAT.FORWARD)
    turnMotor.run(Adafruit_MotorHAT.RELEASE)
    rearDriveMotor.run(Adafruit_MotorHAT.FORWARD)

# move backward
def goReverse():
    frontDriveMotor.run(Adafruit_MotorHAT.BACKWARD)
    turnMotor.run(Adafruit_MotorHAT.RELEASE)
    rearDriveMotor.run(Adafruit_MotorHAT.BACKWARD)

# move forward left
def goForwardLeft():
    frontDriveMotor.run(Adafruit_MotorHAT.FORWARD)
    rearDriveMotor.run(Adafruit_MotorHAT.FORWARD)
    turnMotor.run(Adafruit_MotorHAT.FORWARD)

# move forward right
def goForwardRight():
    frontDriveMotor.run(Adafruit_MotorHAT.FORWARD)
    rearDriveMotor.run(Adafruit_MotorHAT.FORWARD)
    turnMotor.run(Adafruit_MotorHAT.BACKWARD)

# move reverse left
def goReverseLeft():
    frontDriveMotor.run(Adafruit_MotorHAT.BACKWARD)
    rearDriveMotor.run(Adafruit_MotorHAT.BACKWARD)
    turnMotor.run(Adafruit_MotorHAT.FORWARD)

# move reverse right
def goReverseRight():
    frontDriveMotor.run(Adafruit_MotorHAT.BACKWARD)
    rearDriveMotor.run(Adafruit_MotorHAT.BACKWARD)
    turnMotor.run(Adafruit_MotorHAT.BACKWARD)

app = Flask(__name__)

@app.route('/')
def index():
    # display button layout
    return render_template('index.html')

@app.route('/controller/<buttonPress>')
def controller(buttonPress):
    # trigger event depending on the button pressed
    # and then return an ok signal
    if buttonPress == 'Forward':
        goForward()
    elif buttonPress == 'ForwardLeft':
        goForwardLeft()
    elif buttonPress == 'ForwardRight':
        goForwardRight()
    elif buttonPress == 'Reverse':
        goReverse()
    elif buttonPress == 'ReverseLeft':
        goReverseLeft()
    elif buttonPress == 'ReverseRight':
        goReverseRight()
    elif buttonPress == 'Stop':
        turnOffMotors()
    else:
        # Send a signal if command requested does not exist
        # for debugging
        return 'Command not found'

    return 'ok'


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
