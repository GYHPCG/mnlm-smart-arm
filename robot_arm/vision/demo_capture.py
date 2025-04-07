'''
Author: '破竹' '2986779260@qq.com'
Date: 2025-04-07 22:41:03
LastEditors: '破竹' '2986779260@qq.com'
LastEditTime: 2025-04-07 22:43:31
FilePath: \code\mnlm-smart-arm\robot_arm\vision\demo_capture.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import cv2
import ipywidgets.widgets as widgets
import threading
import time
image_widget = widgets.Image(format='jpeg', width=600, height=500) #设置摄像头显示组件

display(image_widget)

#bgr8转jpeg格式
import enum
import cv2
def bgr8_to_jpeg(value, quality=75):
    return bytes(cv2.imencode('.jpg', value)[1])

image = cv2.VideoCapture(0,cv2.CAP_V4L2) #打开摄像头
ret, frame = image.read()
image_widget.value = bgr8_to_jpeg(frame)