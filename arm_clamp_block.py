#!/usr/bin/env python3
#coding=utf-8
import time
from Arm_Lib import Arm_Device

# 创建机械臂对象
Arm = Arm_Device()
time.sleep(.1)

# 定义夹积木块函数，enable=1：夹住，=0：松开
def arm_clamp_block(enable):
    if enable == 0:
        Arm.Arm_serial_servo_write(6, 60, 400)
    else:
        Arm.Arm_serial_servo_write(6, 135, 400)
    time.sleep(.5)
