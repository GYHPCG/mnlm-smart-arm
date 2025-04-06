'''
Author: '破竹' '2986779260@qq.com'
Date: 2025-04-06 20:21:19
LastEditors: '破竹' '2986779260@qq.com'
LastEditTime: 2025-04-06 20:25:22
FilePath: \code\mnlm-smart-arm\robot_arm\move_all_servo.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
#!/usr/bin/env python3
#coding=utf-8
import time
from Arm_Lib import Arm_Device

# 创建机械臂对象
Arm = Arm_Device()
time.sleep(.1)

# 移动所有舵机到指定位置
def move_all_servo(angle, op_time=500):
    Arm.Arm_serial_servo_write6(angle[0],angle[1],angle[2],angle[3],angle[4],angle[5], op_time)
    time.sleep(1)


if __name__ == '__main__':
    move_all_servo([0, 90, 90, 45, 32, 0],500)