#!/usr/bin/env python
# coding: utf-8
import cv2
import random
from .dofbot_config import *
from .snake_target import snake_target
from .snake_ctrl import snake_ctrl
import Arm_Lib
import threading

# 添加全局变量控制运行状态
is_running = False
snake_thread = None

def stop_snake_follow():
    """停止蛇形追踪"""
    global is_running, snake_thread
    is_running = False
    if snake_thread and snake_thread.is_alive():
        snake_thread.join(timeout=1.0)  # 等待线程结束，最多等待1秒

class SnakeController:
    def __init__(self, color='red'):
        # 初始化机械臂
        self.Arm = Arm_Lib.Arm_Device()
        self.joints_0 = [90, 135, 0, 45, 0, 180]
        self.Arm.Arm_serial_servo_write6_array(self.joints_0, 1000)
        
        # 初始化模块
        self.snake_target = snake_target()
        self.snake_ctrl = snake_ctrl()
        
        # 颜色配置
        self.color = color
        self.color_hsv  = {"red"   : ((0, 43, 46), (10, 255, 255)),
              "green" : ((35, 43, 46), (77, 255, 255)),
              "blue"  : ((100, 43, 46), (124, 255, 255)),
              "yellow": ((26, 43, 46), (34, 255, 255))}
        
        self.random_colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(255)]
        
        # 加载HSV配置
        self.HSV_path = "/home/dofbot/dofbot_ws/src/dofbot_snake_follow/scripts/HSV_config.txt"
        try: read_HSV(self.HSV_path,self.color_hsv)
        except Exception as e: print(f"读取HSV配置错误: {str(e)}")

    def run(self):
        global is_running
        capture = cv2.VideoCapture(0)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        try:
            while capture.isOpened() and is_running:
                ret, img = capture.read()
                if not ret: break
                
                # 处理图像
                img = cv2.resize(img, (640, 480))
                img, snake_msg = self.snake_target.target_run(img, self.color_hsv)

                print("sname_msg %s"%(snake_msg))
                # 运动控制
                if len(snake_msg) == 1:
                    threading.Thread(target=self.snake_ctrl.snake_main, args=(self.color, snake_msg,)).start()
                
                # 叠加显示信息
                cv2.putText(img, self.color, (320, 50),
                           cv2.FONT_HERSHEY_SIMPLEX, 2,
                           self.random_colors[random.randint(0, 254)], 2)
                
                # 显示画面
                cv2.imshow("Snake Control", img)
                
                # 键盘控制
                key = cv2.waitKey(10) & 0xFF
                if key == ord('q'):  # 退出
                    break
                elif key == ord('c'):  # 切换颜色（示例）
                    self.color = 'green' if self.color == 'red' else 'red'
                    
        finally:
            capture.release()
            cv2.destroyAllWindows()
            self.Arm.Arm_serial_servo_write6_array(self.joints_0, 1000)
            is_running = False

def snake_follow_run(color='red'):
    """运行蛇形追踪程序"""
    global is_running, snake_thread
    
    # 如果已经在运行，先停止之前的追踪
    if is_running:
        stop_snake_follow()
    
    is_running = True
    snake_follow = SnakeController(color=color)
    
    # 在新线程中运行追踪
    snake_thread = threading.Thread(target=snake_follow.run)
    snake_thread.start()

if __name__ == "__main__":
    # 通过函数参数启动（示例：追踪红色）
    snake_follow_run(color='red')