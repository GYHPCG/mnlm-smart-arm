import cv2
import Arm_Lib
from color_follow import color_follow  # 假设 color_follow 模块已实现追踪逻辑
import random

def run(color='red'):
    """
    运行颜色追踪程序
    :param color: 要追踪的颜色，可选 'red', 'green', 'blue', 'yellow'
    """
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
        while cap.isOpened():
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
        Arm.Arm_serial_servo_write6_array(joints0, 1000)

if __name__ == "__main__":
    # 示例：直接调用函数
    run(color='red')  # 修改此处颜色参数即可