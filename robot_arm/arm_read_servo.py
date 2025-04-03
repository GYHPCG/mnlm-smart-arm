'''
Author: '破竹' '2986779260@qq.com'
Date: 2025-04-03 19:23:10
LastEditors: '破竹' '2986779260@qq.com'
LastEditTime: 2025-04-03 19:53:45
FilePath: \code\mnlm-smart-arm\robot_arm\arm_read_servo.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
#!/usr/bin/env python3
#coding=utf-8
import time
from Arm_Lib import Arm_Device

# 读取第id个舵机的位置，返回int
def read_servo(id)->int:
    # 创建机械臂对象
    Arm = Arm_Device()
    time.sleep(.1)
    return Arm.Arm_serial_servo_read(id)

if __name__ == '__main__':
    while True:
        for i in range(1, 7):
            print(f'第{i}个舵机的位置是：{read_servo(i)}')
        time.sleep(1)

 