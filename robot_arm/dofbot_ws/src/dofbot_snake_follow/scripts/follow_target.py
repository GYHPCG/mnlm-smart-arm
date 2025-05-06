#!/usr/bin/env python
# coding: utf-8
import cv2 as cv
import threading
from time import sleep
from dofbot_config import *
import ipywidgets as widgets
from IPython.display import display
from snake_target import snake_target
from snake_ctrl import snake_ctrl

import Arm_Lib
Arm = Arm_Lib.Arm_Device()
joints_0 = [90, 135, 0,45, 0, 180]
Arm.Arm_serial_servo_write6_array(joints_0, 1000)

# 创建实例
snake_target = snake_target()
snake_ctrl = snake_ctrl()
# 初始化模式
model = 'General'
# 设置随机颜色
color = [[random.randint(0, 255) for _ in range(3)] for _ in range(255)]
color_hsv  = {"red"   : ((0, 43, 46), (10, 255, 255)),
              "green" : ((35, 43, 46), (77, 255, 255)),
              "blue"  : ((100, 43, 46), (124, 255, 255)),
              "yellow": ((26, 43, 46), (34, 255, 255))}
HSV_path="/home/dofbot/dofbot_ws/src/dofbot_snake_follow/scripts/HSV_config.txt"
try: read_HSV(HSV_path,color_hsv)
except Exception: print("Read HSV_config Error!!!")

button_layout      = widgets.Layout(width='150px', height='27px', align_self='center')
output = widgets.Output()
choose_color=widgets.ToggleButtons( options=['red', 'green', 'blue','yellow'], button_style='success', 
    tooltips=['Description of slow', 'Description of regular', 'Description of fast'])
# 退出
exit_button = widgets.Button(description='Exit', button_style='danger', layout=button_layout)
imgbox = widgets.Image(format='jpg', height=480, width=640, layout=widgets.Layout(align_self='center'))
down_box = widgets.HBox([choose_color,exit_button], layout=widgets.Layout(align_self='center'));
controls_box = widgets.VBox([imgbox, down_box], layout=widgets.Layout(align_self='center'))
# ['auto', 'flex-start', 'flex-end', 'center', 'baseline', 'stretch', 'inherit', 'initial', 'unset']

def exit_button_Callback(value):
    global model
    model = 'Exit'
#     with output: print(model)
exit_button.on_click(exit_button_Callback)


def camera():
    # 打开摄像头
    capture = cv.VideoCapture(0)
    # 当摄像头正常打开的情况下循环执行
    while capture.isOpened():
        try:
            # 读取相机的每一帧
            _, img = capture.read()
            # 统一图像大小
            img = cv.resize(img, (640, 480))
            # 获得运动信息
            img, snake_msg = snake_target.target_run(img, color_hsv)
            if len(snake_msg) == 1:
                threading.Thread(target=snake_ctrl.snake_main, args=(choose_color.value, snake_msg,)).start()
            if model == 'Exit':
                cv.destroyAllWindows()
                capture.release()
                break
            # 添加文字
            cv.putText(img, choose_color.value, (int(img.shape[0] / 2), 50), cv.FONT_HERSHEY_SIMPLEX, 2, color[random.randint(0, 254)], 2)
            imgbox.value = cv.imencode('.jpg', img)[1].tobytes()
        except KeyboardInterrupt:capture.release()

display(controls_box,output)
threading.Thread(target=camera, ).start()