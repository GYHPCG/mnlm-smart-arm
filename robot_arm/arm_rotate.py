#!/usr/bin/env python3
#coding=utf-8
import time
from Arm_Lib import Arm_Device

# 创建机械臂对象
Arm = Arm_Device()
time.sleep(.1)

def arm_rotate(angle):
    Arm.Arm_serial_servo_write6(1, angle, 1000)

if __name__ == '__main__':
    while True:
        angle = int(input("请输入角度："))
        arm_rotate(angle)
