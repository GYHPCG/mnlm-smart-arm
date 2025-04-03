#!/usr/bin/env python3
#coding=utf-8
import time
from Arm_Lib import Arm_Device

# 创建机械臂对象
Arm = Arm_Device()
time.sleep(.1)

# 将第id个舵机移动到到px,py位置
def ctrl_servo(id, px, py):
    Arm.Arm_serial_servo_write(id, px, py)
    time.sleep(1)
    del Arm

if __name__ == '__main__':
    ctrl_servo(1, 0, 0)