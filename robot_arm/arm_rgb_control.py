'''
Author: '破竹' '2986779260@qq.com'
Date: 2025-03-25 22:45:34
LastEditors: '破竹' '2986779260@qq.com'
LastEditTime: 2025-03-25 22:46:03
FilePath: \code\LLM\rgb.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import time
from Arm_Lib import Arm_Device

# 获取机械臂的对象
Arm = Arm_Device()
time.sleep(.1)

def rgb_control(r,g,b):
    Arm.Arm_RGB_set(50, 0, 0) #RGB亮红灯
    time.sleep(.5)
    # Arm.Arm_RGB_set(0, 50, 0) #RGB亮绿灯
    # time.sleep(.5)
    # Arm.Arm_RGB_set(0, 0, 50) #RGB亮蓝灯
    # time.sleep(.5)

    print(" END OF LINE! ")


