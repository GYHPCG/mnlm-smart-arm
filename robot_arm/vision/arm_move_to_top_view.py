#!/usr/bin/env python3
#coding=utf-8
import time
from Arm_Lib import Arm_Device

# 创建机械臂对象
Arm = Arm_Device()
time.sleep(.1)

def move_to_top_view():
    Arm.Arm_serial_servo_write6(90, 135, 0, 15, 90, 0, 500)
    time.sleep(1)


if __name__ == '__main__':
    move_to_top_view()