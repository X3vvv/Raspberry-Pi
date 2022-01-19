#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from bottle import get, post, run, request, template

import RPi.GPIO as GPIO
import configparser


class Car(object):
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        config = configparser.ConfigParser()
        config.read("/home/pi/Documents/Raspberry-Pi/car/config.ini")
        self.enab_pin = [
            config.getint("DEFAULT", "ena"),
            config.getint("DEFAULT", "enb"),
        ]
        self.inx_pin = [
            config.getint("DEFAULT", "in1"),  # left wheel 1
            config.getint("DEFAULT", "in2"),  # left wheel 2
            config.getint("DEFAULT", "in3"),  # right wheel 1
            config.getint("DEFAULT", "in4"),  # right wheel 2
        ]
        self.left_pin = [self.inx_pin[0], self.inx_pin[1]]
        self.right_pin = [self.inx_pin[2], self.inx_pin[3]]
        self.setup()

    # init gpios
    def setup(self):
        # set enable gpio as HIGH
        for pin in self.enab_pin:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.HIGH)
        # set controlling gpio as LOW
        for pin in self.inx_pin:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)

    # forward
    def front(self):
        self.setup()
        GPIO.output(self.left_pin[0], GPIO.HIGH)
        GPIO.output(self.right_pin[0], GPIO.HIGH)

    # left
    def leftFront(self):
        self.setup()
        GPIO.output(self.right_pin[0], GPIO.HIGH)

    # right
    def rightFront(self):
        self.setup()
        GPIO.output(self.left_pin[0], GPIO.HIGH)

    # back
    def rear(self):
        self.setup()
        GPIO.output(self.left_pin[1], GPIO.HIGH)
        GPIO.output(self.right_pin[1], GPIO.HIGH)

    # back + left
    def leftRear(self):
        self.setup()
        GPIO.output(self.right_pin[1], GPIO.HIGH)

    # back + right
    def rightRear(self):
        self.setup()
        GPIO.output(self.left_pin[1], GPIO.HIGH)


def main(status):

    car = Car()

    if status == "front":
        car.front()
    elif status == "rear":
        car.rear()
    elif status == "left":
        car.leftFront()  # TODO
    elif status == "right":
        car.rightFront()  # TODO
    elif status == "leftFront":
        car.leftFront()
    elif status == "rightFront":
        car.rightFront()
    elif status == "leftRear":
        car.leftRear()
    elif status == "rightRear":
        car.rightRear()
    elif status == "stop":
        car.setup()


@get("/")
def index():
    return template("/home/pi/Documents/Raspberry-Pi/car/index")


@post("/cmd")
def cmd():
    adss = request.body.read().decode()
    print("Pressed:" + adss)
    main(adss)
    return "OK"


run(host="0.0.0.0")
