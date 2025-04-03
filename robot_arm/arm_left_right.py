#!/usr/bin/env python3
#coding=utf-8
import time
from Arm_Lib import Arm_Device

# 创建机械臂对象
Arm = Arm_Device()
time.sleep(.1)

def left_right():
     # 让舵机复位归中
    Arm.Arm_serial_servo_write6(90, 90, 90, 90, 90, 90, 500)
    time.sleep(1)

    # 控制3号和4号舵机上下运行
    Arm.Arm_serial_servo_write(3, 0, 1000)
    time.sleep(.001)
    Arm.Arm_serial_servo_write(4, 180, 1000)
    time.sleep(1)
    
    # 控制1号舵机左右运动
    Arm.Arm_serial_servo_write(1, 180, 500)
    time.sleep(.5)
    Arm.Arm_serial_servo_write(1, 0, 1000)
    time.sleep(1)
    
    # 控制舵机恢复初始位置
    Arm.Arm_serial_servo_write6(90, 90, 90, 90, 90, 90, 1000)
    time.sleep(1.5)


if __name__ == '__main__':
    try:
        left_right()
    except KeyboardInterrupt:
        print("exit")
        

