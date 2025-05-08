'''
Author: '破竹' '2986779260@qq.com'
Date: 2025-05-07 16:33:17
LastEditors: '破竹' '2986779260@qq.com'
LastEditTime: 2025-05-07 22:47:19
FilePath: \code\mnlm-smart-arm\robot_arm\dofbot_ws\src\dofbot_color_follow\follow_color_act.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import cv2
import Arm_Lib
from .color_follow import color_follow  # 假设 color_follow 模块已实现追踪逻辑
import random

# 添加全局变量控制运行状态
is_running = False

def stop_color_follow():
    """停止颜色追踪"""
    global is_running
    is_running = False

def follow_color_run(color='red'):
    """
    运行颜色追踪程序
    :param color: 要追踪的颜色，可选 'red', 'green', 'blue', 'yellow'
    """
    global is_running
    is_running = True
    
    # 初始化机械臂
    Arm = Arm_Lib.Arm_Device()
    joints_0 = [90, 135, 20, 25, 90, 30]
    Arm.Arm_serial_servo_write6_array(joints_0, 1000)
    
    # 预定义颜色 HSV 范围
    color_hsv = {
        "red": ((0, 25, 90), (10, 255, 255)),
        "green": ((53, 36, 40), (80, 255, 255)),
        "blue": ((110, 80, 90), (120, 255, 255)),
        "yellow": ((25, 20, 55), (50, 255, 255))
    }
    
    # 验证颜色有效性
    if color not in color_hsv:
        raise ValueError(f"不支持的颜色: {color}，请选择 'red', 'green', 'blue', 'yellow'")
    
    # 初始化追踪器和摄像头
    follower = color_follow()
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    # 随机颜色用于显示文本
    random_colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(255)]
    
    try:
        while cap.isOpened() and is_running:
            ret, frame = cap.read()
            if not ret: break
            
            # 执行颜色追踪
            processed_frame = follower.follow_function(frame, color_hsv[color])
            
            # 在图像上叠加当前追踪颜色
            cv2.putText(processed_frame, 
                       f"Tracking: {color}", 
                       (30, 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 
                       1, 
                       random_colors[random.randint(0, 254)], 
                       2)
            
            # 显示结果
            cv2.imshow("Color Tracking Demo", processed_frame)
            
            # 按 'q' 退出
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
        # 机械臂复位
        Arm.Arm_serial_servo_write6_array(joints_0, 1000)
        is_running = False

if __name__ == "__main__":
    # 示例：直接调用函数
    follow_color_run(color='red')  # 修改此处颜色参数即可