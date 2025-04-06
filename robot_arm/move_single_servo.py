'''
Author: '破竹' '2986779260@qq.com'
Date: 2025-04-06 20:18:24
LastEditors: '破竹' '2986779260@qq.com'
LastEditTime: 2025-04-06 20:18:47
FilePath: \code\mnlm-smart-arm\robot_arm\move_single_servo.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
#!/usr/bin/env python3
#coding=utf-8
import time
from Arm_Lib import Arm_Device

# 创建机械臂对象
Arm = Arm_Device()
time.sleep(.1)

# 将第id个舵机移动angle角度，运动时间为op_time
def move_single_servo(id, angle, op_time):
    Arm.Arm_serial_servo_write(id, angle, op_time)
    time.sleep(1)


if __name__ == '__main__':
    move_single_servo(1, 60, 500)