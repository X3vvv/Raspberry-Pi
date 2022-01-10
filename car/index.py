#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from bottle import get, post, run, request, template

import RPi.GPIO as GPIO


class Car(object):
    def __init__(self):
        self.enab_pin = [5, 6, 13, 19]
        self.inx_pin = [21, 22, 23, 24]
        self.RightAhead_pin = self.inx_pin[0]
        self.RightBack_pin = self.inx_pin[1]
        self.LeftAhead_pin = self.inx_pin[2]
        self.LeftBack_pin = self.inx_pin[3]
        self.setup()

    # init gpios
    def setup(self):
        print("begin setup ena enb pin")
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        for pin in self.enab_pin:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.HIGH)
        # set enable gpio as HIGH
        pin = None
        for pin in self.inx_pin:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)
        # set controlling gpio as LOW
        print("setup ena enb pin over")

    # forward
    def front(self):
        self.setup()
        GPIO.output(self.RightAhead_pin, GPIO.HIGH)
        GPIO.output(self.LeftAhead_pin, GPIO.HIGH)

    # left
    def leftFront(self):
        self.setup()
        GPIO.output(self.RightAhead_pin, GPIO.HIGH)

    # right
    def rightFront(self):
        self.setup()
        GPIO.output(self.LeftAhead_pin, GPIO.HIGH)

    # back
    def rear(self):
        self.setup()
        GPIO.output(self.RightBack_pin, GPIO.HIGH)
        GPIO.output(self.LeftBack_pin, GPIO.HIGH)

    # back + left
    def leftRear(self):
        self.setup()
        GPIO.output(self.RightBack_pin, GPIO.HIGH)

    # back + right
    def rightRear(self):
        self.setup()
        GPIO.output(self.LeftBack_pin, GPIO.HIGH)


def main(status):

    car = Car()

    if status == "front":
        car.front()
    elif status == "rear":
        car.rear()
    elif status == "left":
        pass
    elif status == "right":
        pass
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
    return template("index")


@post("/cmd")
def cmd():
    adss = request.body.read().decode()
    print("Pressed:" + adss)
    main(adss)
    return "OK"


run(host="0.0.0.0")
