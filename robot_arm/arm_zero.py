'''
Author: '破竹' '2986779260@qq.com'
Date: 2025-04-03 19:45:58
LastEditors: '破竹' '2986779260@qq.com'
LastEditTime: 2025-04-08 21:14:14
FilePath: \code\mnlm-smart-arm\robot_arm\arm_zero.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
#!/usr/bin/env python3
#coding=utf-8
import time
from Arm_Lib import Arm_Device

# 创建机械臂对象
Arm = Arm_Device()
time.sleep(.1)

def arm_zero():
    Arm.Arm_serial_servo_write6(90, 135, 0, 45, 90, 135, 500)
    time.sleep(1)


if __name__ == '__main__':
    arm_zero()