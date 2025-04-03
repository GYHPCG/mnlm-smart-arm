#!/usr/bin/env python3
#coding=utf-8
import time
from Arm_Lib import Arm_Device

# 创建机械臂对象
Arm = Arm_Device()
time.sleep(.1)

def arm_zero():
    Arm.Arm_serial_servo_write6(90, 90, 90, 90, 90, 90, 500)
    time.sleep(1)
    del Arm

if __name__ == '__main__':
    arm_zero()