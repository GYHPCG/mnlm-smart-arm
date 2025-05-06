#!/usr/bin/env python
# coding: utf-8
import cv2 as cv
import threading
from time import sleep
from dofbot_config import *
import ipywidgets as widgets
from IPython.display import display
from identify_target import identify_GetTarget


## 创建获取目标实例
target      = identify_GetTarget()
# 创建相机标定实例
calibration = Arm_Calibration()
# 初始化一些参数
num=0
dp    = []
xy=[90,135]
msg   = {}
threshold = 140
model = "General"
color_list = {}
# 初始化HSV值
color_hsv  = {"red"   : ((0, 43, 46), (10, 255, 255)),
              "green" : ((35, 43, 46), (77, 255, 255)),
              "blue"  : ((100, 43, 46), (124, 255, 255)),
              "yellow": ((26, 43, 46), (34, 255, 255))}
HSV_path="/home/dofbot/dofbot_ws/src/dofbot_color_identify/scripts/HSV_config.txt"
# XYT参数路径
XYT_path="/home/dofbot/dofbot_ws/src/dofbot_color_identify/scripts/XYT_config.txt"
try: read_HSV(HSV_path,color_hsv)
except Exception: print("Read HSV_config Error !!!")
try: xy, thresh = read_XYT(XYT_path)
except Exception: print("Read XYT_config Error !!!")

### 初始化机械臂位置

import Arm_Lib
# 创建机械臂驱动实例
arm = Arm_Lib.Arm_Device()
joints_0 = [xy[0], xy[1], 0, 0, 90, 30]
arm.Arm_serial_servo_write6_array(joints_0, 1000)