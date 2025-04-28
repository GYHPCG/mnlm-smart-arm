# -*- coding: utf-8 -*-
# import RPi.GPIO as GPIO
# 初始化GPIO
# GPIO.setwarnings(False)   # 不打印 warning 信息
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(20, GPIO.OUT)
# GPIO.setup(21, GPIO.OUT)
# GPIO.output(20, 1)  

import RPi.GPIO as GPIO
import time

LED_PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

try:
    while True:
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()