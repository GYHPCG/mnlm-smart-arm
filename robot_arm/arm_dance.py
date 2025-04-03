'''
Author: '破竹' '2986779260@qq.com'
Date: 2025-03-29 16:37:22
LastEditors: '破竹' '2986779260@qq.com'
LastEditTime: 2025-03-29 17:47:30
FilePath: \code\mnlm-smart-arm\arm_dance.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
#!/usr/bin/env python3
#coding=utf-8
import time
from Arm_Lib import Arm_Device

print("调用跳舞函数\n")

Arm = Arm_Device()
time.sleep(.1)

time_1 = 500
time_2 = 1000
time_sleep = 0.5

# 机械臂跳舞
def arm_dance():
    # 让舵机复位归中
    Arm.Arm_serial_servo_write6(90, 90, 90, 90, 90, 90, 500)
    time.sleep(1)
    

    Arm.Arm_serial_servo_write(2, 180-120, time_1)
    time.sleep(.001)
    Arm.Arm_serial_servo_write(3, 120, time_1)
    time.sleep(.001)
    Arm.Arm_serial_servo_write(4, 60, time_1)
    time.sleep(time_sleep)

    Arm.Arm_serial_servo_write(2, 180-135, time_1)
    time.sleep(.001)
    Arm.Arm_serial_servo_write(3, 135, time_1)
    time.sleep(.001)
    Arm.Arm_serial_servo_write(4, 45, time_1)
    time.sleep(time_sleep)

    Arm.Arm_serial_servo_write(2, 180-120, time_1)
    time.sleep(.001)
    Arm.Arm_serial_servo_write(3, 120, time_1)
    time.sleep(.001)
    Arm.Arm_serial_servo_write(4, 60, time_1)
    time.sleep(time_sleep)

    Arm.Arm_serial_servo_write(2, 90, time_1)
    time.sleep(.001)
    Arm.Arm_serial_servo_write(3, 90, time_1)
    time.sleep(.001)
    Arm.Arm_serial_servo_write(4, 90, time_1)
    time.sleep(time_sleep)

    Arm.Arm_serial_servo_write(2, 180-80, time_1)
    time.sleep(.001)
    Arm.Arm_serial_servo_write(3, 80, time_1)
    time.sleep(.001)
    Arm.Arm_serial_servo_write(4, 80, time_1)
    time.sleep(time_sleep)



    Arm.Arm_serial_servo_write(2, 180-60, time_1)
    time.sleep(.001)
    Arm.Arm_serial_servo_write(3, 60, time_1)
    time.sleep(.001)
    Arm.Arm_serial_servo_write(4, 60, time_1)
    time.sleep(time_sleep)

    Arm.Arm_serial_servo_write(2, 180-45, time_1)
    time.sleep(.001)
    Arm.Arm_serial_servo_write(3, 45, time_1)
    time.sleep(.001)
    Arm.Arm_serial_servo_write(4, 45, time_1)
    time.sleep(time_sleep)

    Arm.Arm_serial_servo_write(2, 90, time_1)
    time.sleep(.001)
    Arm.Arm_serial_servo_write(3, 90, time_1)
    time.sleep(.001)
    Arm.Arm_serial_servo_write(4, 90, time_1)
    time.sleep(.001)
    time.sleep(time_sleep)



    Arm.Arm_serial_servo_write(4, 20, time_1)
    time.sleep(.001)
    Arm.Arm_serial_servo_write(6, 150, time_1)
    time.sleep(.001)
    time.sleep(time_sleep)

    Arm.Arm_serial_servo_write(4, 90, time_1)
    time.sleep(.001)
    Arm.Arm_serial_servo_write(6, 90, time_1)
    time.sleep(time_sleep)

    Arm.Arm_serial_servo_write(4, 20, time_1)
    time.sleep(.001)
    Arm.Arm_serial_servo_write(6, 150, time_1)
    time.sleep(time_sleep)

    Arm.Arm_serial_servo_write(4, 90, time_1)
    time.sleep(.001)
    Arm.Arm_serial_servo_write(6, 90, time_1)
    time.sleep(.001)
    Arm.Arm_serial_servo_write(1, 0, time_1)
    time.sleep(.001)
    Arm.Arm_serial_servo_write(5, 0, time_1)
    time.sleep(time_sleep)



    Arm.Arm_serial_servo_write(3, 180, time_1)
    time.sleep(.001)
    Arm.Arm_serial_servo_write(4, 0, time_1)
    time.sleep(time_sleep)

    Arm.Arm_serial_servo_write(6, 180, time_1)
    time.sleep(time_sleep)

    Arm.Arm_serial_servo_write(6, 0, time_2)
    time.sleep(time_sleep)



    Arm.Arm_serial_servo_write(6, 90, time_2)
    time.sleep(.001)
    Arm.Arm_serial_servo_write(1, 90, time_1)
    time.sleep(.001)
    Arm.Arm_serial_servo_write(5, 90, time_1)
    time.sleep(time_sleep)

    Arm.Arm_serial_servo_write(3, 90, time_1)
    time.sleep(.001)
    Arm.Arm_serial_servo_write(4, 90, time_1)
    time.sleep(time_sleep)
    
    print(" END OF LINE! ")

if __name__ == '__main__':
    arm_dance()
