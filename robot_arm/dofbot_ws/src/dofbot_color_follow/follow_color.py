import cv2 as cv
import threading
import random
from time import sleep
import ipywidgets as widgets
from IPython.display import display
from color_follow import color_follow


# 初始化机械臂开始位置
import Arm_Lib
Arm = Arm_Lib.Arm_Device()
joints_0 = [90, 135, 20, 25, 90, 30]
Arm.Arm_serial_servo_write6_array(joints_0, 1000)

#创建实例,初始化参数
follow = color_follow()
# 初始化模式
model = 'General'
# 初始化HSV_learning值
HSV_learning = ()
# 初始化HSV值
color_hsv = {"red": ((0, 25, 90), (10, 255, 255)),
             "green": ((53, 36, 40), (80, 255, 255)),
             "blue": ((110, 80, 90), (120, 255, 255)),
             "yellow": ((25, 20, 55), (50, 255, 255))}
# 设置随机颜色
color = [[random.randint(0, 255) for _ in range(3)] for _ in range(255)]
# HSV参数路径
HSV_path="/home/dofbot/dofbot_ws/src/dofbot_color_follow/HSV_config.txt"
try: read_HSV(HSV_path,color_hsv)
except Exception: print("Read HSV_config Error !!!")


# 创建控件
button_layout = widgets.Layout(width='200px', height='100px', align_self='center')
# 输出控件
output = widgets.Output()
# 颜色追踪
color_follow = widgets.Button(description='color_follow', button_style='success', layout=button_layout)
# 选择颜色
choose_color = widgets.ToggleButtons(options=['red', 'green', 'blue', 'yellow'], button_style='success',
             tooltips=['Description of slow', 'Description of regular', 'Description of fast'])
# 取消追踪
follow_cancel = widgets.Button(description='follow_cancel', button_style='danger', layout=button_layout)
# 学习颜色
learning_color = widgets.Button(description='learning_color', button_style='primary', layout=button_layout)
# 学习颜色追踪
learning_follow = widgets.Button(description='learning_follow', button_style='success', layout=button_layout)
# 退出
exit_button = widgets.Button(description='Exit', button_style='danger', layout=button_layout)
# 图像控件
imgbox = widgets.Image(format='jpg', height=480, width=640, layout=widgets.Layout(align_self='auto'))
# 垂直布局
img_box = widgets.VBox([imgbox, choose_color], layout=widgets.Layout(align_self='auto'))
# 垂直布局
Slider_box = widgets.VBox([color_follow, learning_color, learning_follow,follow_cancel,exit_button],
                          layout=widgets.Layout(align_self='auto'))
# 水平布局
controls_box = widgets.HBox([img_box, Slider_box], layout=widgets.Layout(align_self='auto'))
# ['auto', 'flex-start', 'flex-end', 'center', 'baseline', 'stretch', 'inherit', 'initial', 'unset']

# 模式切换
def color_follow_Callback(value):
    global model
    model = 'color_follow'
def learning_color_Callback(value):
    global model
    model = 'learning_color'
def learning_follow_Callback(value):
    global model
    model = 'learning_follow'
def follow_cancel_Callback(value):
    global model
    model = 'General'
def exit_button_Callback(value):
    global model
    model = 'Exit'
color_follow.on_click(color_follow_Callback)
learning_color.on_click(learning_color_Callback)
learning_follow.on_click(learning_follow_Callback)
follow_cancel.on_click(follow_cancel_Callback)
exit_button.on_click(exit_button_Callback)


# 主程序
def camera():
    global HSV_learning,model
    # 打开摄像头
    capture = cv.VideoCapture(0)
    capture.set(3, 640)
    capture.set(4, 480)
    capture.set(5, 30)  #设置帧率
    # 当摄像头正常打开的情况下循环执行
    while capture.isOpened():
        try:
            # 读取相机的每一帧
            _, img = capture.read()
            # 统一图像大小
            img = cv.resize(img, (640, 480))
            if model == 'color_follow':
                img = follow.follow_function(img, color_hsv[choose_color.value])
                # 添加文字
                cv.putText(img, choose_color.value, (int(img.shape[0] / 2), 50), cv.FONT_HERSHEY_SIMPLEX, 2, color[random.randint(0, 254)], 2)
            if model == 'learning_color':
                img,HSV_learning = follow.get_hsv(img)
            if model == 'learning_follow' :
                if len(HSV_learning)!=0:
                    print(HSV_learning)
                    img = follow.learning_follow(img, HSV_learning)
                    # 添加文字
                    cv.putText(img,'LeColor', (240, 50), cv.FONT_HERSHEY_SIMPLEX, 1, color[random.randint(0, 254)], 1)
            if model == 'Exit':
                cv.destroyAllWindows()
                capture.release()
                break
            imgbox.value = cv.imencode('.jpg', img)[1].tobytes()
        except KeyboardInterrupt:capture.release()

# 启动
display(controls_box,output)
threading.Thread(target=camera, ).start()