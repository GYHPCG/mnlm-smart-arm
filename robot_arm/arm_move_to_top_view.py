#!/usr/bin/env python3
#coding=utf-8
import time
from Arm_Lib import Arm_Device

# 创建机械臂对象
Arm = Arm_Device()
time.sleep(.1)

def move_to_top_view():
     # [89.71029649148431, 45.25613284306083, 91.86258487811448, -35, 89.71253294095186]
    Arm.Arm_serial_servo_write6(90, 45, 0, 90, -35, 90, 500)
    time.sleep(1)


if __name__ == '__main__':
    move_to_top_view()