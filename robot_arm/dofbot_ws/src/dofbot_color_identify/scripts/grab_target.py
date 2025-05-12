#!/usr/bin/env python
# coding: utf-8
import rospy
import Arm_Lib
import cv2 as cv
import numpy as np
from time import sleep
from identify_grap import identify_grap
from dofbot_info.srv import kinemarics, kinemaricsRequest, kinemaricsResponse
from post_processing_viz import post_processing_viz_one,post_processing_viz_two

class identify_GetTarget:
    def __init__(self):
        # 创建抓取实例
        self.grap = identify_grap()
        # 机械臂识别位置调节
        self.xy = [90, 135]
        # 创建机械臂实例
        self.arm = Arm_Lib.Arm_Device()
        # ROS节点初始化
        self.n = rospy.init_node('dofbot_identify', anonymous=True)
        # 创建获取反解结果的客户端
        self.client = rospy.ServiceProxy("dofbot_kinemarics", kinemarics)

    def select_color(self, image, color_hsv, color_list):
        '''
        选择识别颜色
        :param image:输入图像
        :param color_hsv: 示例{color_name:((lowerb),(upperb))}
        :param color_list: 颜色序列:['0'：无 '1'：红色 '2'：绿色 '3'：蓝色 '4'：黄色]
        :return: 输出处理后的图像,(颜色,位置)
        '''
        # 规范输入图像大小
        self.image = cv.resize(image, (640, 480))
        msg = {}
        if len(color_list)==0:return self.image,msg
        if '1' in color_list:
            self.color_name=color_list['1']
            pos = self.get_Sqaure(color_hsv[self.color_name])
            if pos != None: msg[self.color_name] = pos
        if '2' in color_list:
            self.color_name=color_list['2']
            pos = self.get_Sqaure(color_hsv[self.color_name])
            if pos != None: msg[self.color_name] = pos
        if '3' in color_list:
            self.color_name=color_list['3']
            pos = self.get_Sqaure(color_hsv[self.color_name])
            if pos != None: msg[self.color_name] = pos
        if '4' in color_list:
            self.color_name=color_list['4']
            pos = self.get_Sqaure(color_hsv[self.color_name])
            if pos != None: msg[self.color_name] = pos
        return self.image, msg


    def image_to_arm_coordinates(self, top_left, bottom_right):
        """
        将图像坐标转换为机械臂可用坐标
        
        参数:
        top_left: (x1, y1) 左上角坐标
        bottom_right: (x2, y2) 右下角坐标
        
        返回:
        (x, y): 机械臂可用坐标
        """
        # 1. 计算中心点
        center_x = (top_left[0] + bottom_right[0]) / 2
        center_y = (top_left[1] + bottom_right[1]) / 2
        
        # 2. 坐标转换
        # 图像中心点 (320, 480)
        # 考虑图像坐标系和机械臂坐标系的转换
        arm_x = round(((center_x - 320) / 4000), 5)  # 水平方向转换
        arm_y = round(((480 - center_y) / 3000) * 0.8 + 0.19, 5)  # 垂直方向转换
        
        return (arm_x, arm_y)

    def get_arm_coordinates(self, x1, y1, x2, y2):
        """
        更简单的接口，直接使用四个坐标值
        
        参数:
        x1, y1: 左上角坐标
        x2, y2: 右下角坐标
        
        返回:
        (x, y): 机械臂可用坐标
        """
        return self.image_to_arm_coordinates((x1, y1), (x2, y2))
                
    def get_Sqaure(self, color_hsv):
        '''
        颜色识别,获得方块的坐标
        '''
        (lowerb, upperb) = color_hsv
        # 复制原始图像,避免处理过程中干扰
        mask = self.image.copy()
        # 将图像转换为HSV。
        hsv = cv.cvtColor(self.image, cv.COLOR_BGR2HSV)
        # 筛选出位于两个数组之间的元素。
        img = cv.inRange(hsv, lowerb, upperb)
        # 设置非掩码检测部分全为黑色
        mask[img == 0] = [0, 0, 0]
        # 获取不同形状的结构元素
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))
        # 形态学闭操作
        dst_img = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)
        # 将图像转为灰度图
        dst_img = cv.cvtColor(dst_img, cv.COLOR_RGB2GRAY)
        # 图像二值化操作
        ret, binary = cv.threshold(dst_img, 10, 255, cv.THRESH_BINARY)
        # 获取轮廓点集(坐标) python2和python3在此处略有不同
        contours, heriachy = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)  # 获取轮廓点集(坐标)
        for i, cnt in enumerate(contours):
            # boundingRect函数计算边框值，x，y是坐标值，w，h是矩形的宽和高
            x, y, w, h = cv.boundingRect(cnt)
            # 计算轮廓的⾯积
            area = cv.contourArea(cnt)
            # ⾯积限制
            if area > 1000:
                # 中心坐标
                point_x = float(x + w / 2)
                point_y = float(y + h / 2)
                # 在img图像画出矩形，(x, y), (x + w, y + h)是矩形坐标，(0, 255, 0)设置通道颜色，2是设置线条粗度
                cv.rectangle(self.image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # 绘制矩形中心
                cv.circle(self.image, (int(point_x), int(point_y)), 5, (0, 0, 255), -1)
                # 在图片中绘制结果
                cv.putText(self.image, self.color_name, (int(x - 15), int(y - 15)),
                           cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
                # 计算方块在图像中的位置
                print("%d %d"%(point_x,point_y))
                (a, b) = (round(((point_x - 320) / 4000), 5), round(((480 - point_y) / 3000) * 0.8+0.19, 5))
                print("------------------ identify up -------------------")
                print(a, b)
#                 print("------------------ identify down -------------------")
                return (a, b)

    def target_run(self, msg, xy=None):
        '''
        抓取函数
        :param msg: (颜色,位置)
        '''
        if xy != None: self.xy = xy
        move_status=0
        for i in msg.values():
            if i !=None: move_status=1
        if move_status==1:
            self.arm.Arm_Buzzer_On(1)
            sleep(0.5)
        for name, pos in msg.items():
            # print "pos : ",pos
            # print "name : ",name
            try:
                # 此处ROS反解通讯,获取各关节旋转角度
                joints = self.server_joint(pos)
                # 调取移动函数
                self.grap.identify_move(str(name), joints)
            except Exception: print("sqaure_pos empty")
        if move_status==1:
            # 架起
            joints_uu = [90, 80, 50, 50, 265, 30]
            # 移动至物体位置上方
            self.arm.Arm_serial_servo_write6_array(joints_uu, 1000)
            sleep(1)
            # 初始位置
            joints_0 = [self.xy[0], self.xy[1], 0, 0, 90, 30]
            # 移动至初始位置
            self.arm.Arm_serial_servo_write6_array(joints_0, 500)
            sleep(0.5)
            
    def vlm_target_run(self, msg, xy=None):
        '''
        抓取函数
        :param msg: (颜色,位置)
        '''
        if xy != None: self.xy = xy
        move_status=0
        for i in msg.values():
            if i !=None: move_status=1
        if move_status==1:
            self.arm.Arm_Buzzer_On(1)
            sleep(0.5)
        for name,pos in msg.items():
            # print "pos : ",pos
            # print "name : ",name
            try:
                # 此处ROS反解通讯,获取各关节旋转角度
                joints = self.server_joint(pos)
                # 调取移动函数
                self.grap.vlm_move(joints)
            except Exception: print("sqaure_pos empty")
        if move_status==1:
            # 回到抓取起始位置
            # 架起
            joints_uu = [90, 80, 50, 50, 265, 30]
            # 移动至物体位置上方
            self.arm.Arm_serial_servo_write6_array(joints_uu, 1000)
            sleep(1)
            # 初始位置
            joints_0 = [self.xy[0], self.xy[1], 0, 0, 90, 30]
            # 移动至初始位置
            self.arm.Arm_serial_servo_write6_array(joints_0, 500)
            sleep(0.5)

    def double_vlm_target_run(self, msg, xy=None):
        '''
        抓取函数
        :param msg: (颜色,位置)
        '''
        if xy != None: self.xy = xy
        move_status=0
        for i in msg.values():
            if i !=None: move_status=1
        if move_status==1:
            self.arm.Arm_Buzzer_On(1)
            sleep(0.5)

        try:
             # 此处ROS反解通讯,获取各关节旋转角度
            name1,pos1 = list(msg.items())[0]
            name2,pos2 = list(msg.items())[1]
            
            start_joints = self.server_joint(pos1)
            end_joints = self.server_joint(pos2)

            self.grap.double_vlm_move(start_joints,end_joints)
            
        except Exception: print("sqaure_pos empty")
        # for name,pos in msg.items():
        #     # print "pos : ",pos
        #     # print "name : ",name
        #     try:
        #         # 此处ROS反解通讯,获取各关节旋转角度
        #         joints = self.server_joint(pos)
        #         # 调取移动函数
        #         self.grap.vlm_move(joints)
        #     except Exception: print("sqaure_pos empty")
        if move_status==1:
            # 回到抓取起始位置
            # 架起
            joints_uu = [90, 80, 50, 50, 265, 30]
            # 移动至物体位置上方
            self.arm.Arm_serial_servo_write6_array(joints_uu, 1000)
            sleep(1)
            # 初始位置
            joints_0 = [self.xy[0], self.xy[1], 0, 0, 90, 30]
            # 移动至初始位置
            self.arm.Arm_serial_servo_write6_array(joints_0, 500)
            sleep(0.5)
    
    def move_to(self, msg, xy=None):
        '''
        抓取函数
        :param msg: (颜色,位置)
        '''
        if xy != None: self.xy = xy
        move_status=0
        for i in msg.values():
            if i !=None: move_status=1
        if move_status==1:
            self.arm.Arm_Buzzer_On(1)
            sleep(0.5)
        for name,pos in msg.items():
            # print "pos : ",pos
            # print "name : ",name
            try:
                # 此处ROS反解通讯,获取各关节旋转角度
                joints = self.server_joint(pos)
                # 调取移动函数
                self.grap.move_to(joints)
            except Exception: print("sqaure_pos empty")
            
    def server_joint(self, posxy):
        '''
        发布位置请求,获取关节旋转角度
        :param posxy: 位置点x,y坐标
        :return: 每个关节旋转角度
        '''
        # 等待server端启动
        self.client.wait_for_service()
        # 创建消息包
        request = kinemaricsRequest()
        request.tar_x = posxy[0]
        request.tar_y = posxy[1]
        request.kin_name = "ik"
        try:
            response = self.client.call(request)
            if isinstance(response, kinemaricsResponse):
                # 获得反解响应结果
                joints = [0.0, 0.0, 0.0, 0.0, 0.0]
                joints[0] = response.joint1
                joints[1] = response.joint2
                joints[2] = response.joint3
                joints[3] = response.joint4
                joints[4] = response.joint5
                # 当逆解越界,出现负值时,适当调节.
                if joints[2] < 0:
                    joints[1] += joints[2] * 3 / 5
                    joints[3] += joints[2] * 3 / 5
                    joints[2] = 0
                # print joints
                return joints
        except Exception:
            rospy.loginfo("arg error")


def grasp_object(result,img_path):
      ## 第五步：视觉大模型输出结果后处理和可视化
    print('第五步：视觉大模型输出结果后处理和可视化')
    START_X_CENTER, START_Y_CENTER= post_processing_viz_one(result, img_path, check=True)
    START_X_MIN = int(result['start_xyxy'][0][0])
    START_Y_MIN = int(result['start_xyxy'][0][1])
    # 起点，右下角像素坐标
    START_X_MAX = int(result['start_xyxy'][1][0])
    START_Y_MAX = int(result['start_xyxy'][1][1])
    target      = identify_GetTarget()
    target_xy = target.get_arm_coordinates(START_X_MIN,START_Y_MIN,START_X_MAX,START_Y_MAX)
     # 输出结果
    print("Detected Targets:", target_xy)
    # ta =  {'red': (234, 233), 'green': (455, 222)}
    ta =  {'start':target_xy}
     # 假设我们有一个目标位置进行抓取测试
    if target_xy:
        target.vlm_target_run(ta)
        
def transfer_object_to_target(result,img_path):
    print('第五步：视觉大模型输出结果后处理和可视化')
    START_X_CENTER, START_Y_CENTER, END_X_CENTER, END_Y_CENTER = post_processing_viz_two(result, img_path, check=True)
     #可视化结束
    print("可视化结束")
    # 起点，左上角像素坐标
    START_X_MIN = int(result['start_xyxy'][0][0])
    START_Y_MIN = int(result['start_xyxy'][0][1])
    # 起点，右下角像素坐标
    START_X_MAX = int(result['start_xyxy'][1][0])
    START_Y_MAX = int(result['start_xyxy'][1][1])

    # 终点，左上角像素坐标
    END_X_MIN = int(result['end_xyxy'][0][0])
    END_Y_MIN = int(result['end_xyxy'][0][1])
    # 终点，右下角像素坐标
    END_X_MAX = int(result['end_xyxy'][1][0])
    END_Y_MAX = int(result['end_xyxy'][1][1])
    
    target      = identify_GetTarget()
    start_targets = target.get_arm_coordinates(START_X_MIN,START_Y_MIN,START_X_MAX,START_Y_MAX)
    end_targets = target.get_arm_coordinates(END_X_MIN,END_Y_MIN,END_X_MAX,END_Y_MAX)

    # starts = {"start": start_targets}
    # ends = {"end": end_targets}
    msg = {
        "start": start_targets,
        "end": end_targets,
    }
    target.double_vlm_target_run(msg)

def get_xy(result, img_path):
    START_X_CENTER, START_Y_CENTER= post_processing_viz_one(result, img_path, check=True)
    START_X_MIN = int(result['start_xyxy'][0][0])
    START_Y_MIN = int(result['start_xyxy'][0][1])
    # 起点，右下角像素坐标
    START_X_MAX = int(result['start_xyxy'][1][0])
    START_Y_MAX = int(result['start_xyxy'][1][1])

    target      = identify_GetTarget()
    start_targets = target.get_arm_coordinates(START_X_MIN,START_Y_MIN,START_X_MAX,START_Y_MAX)
    
    msg = {
        "start": start_targets,
    }
    return msg
    

def move_to_other(result,img_path):
     msg = get_xy(result,img_path)

     target      = identify_GetTarget()
     
     target.move_to(msg)

    

import numpy as np

def simulate_image():
    """创建一个模拟图像用于测试"""
    img = np.zeros((480, 640, 3), dtype=np.uint8)
    # 在图像中绘制一些色块作为测试对象
    cv.rectangle(img, (100, 100), (150, 150), (0, 0, 255), -1)  # 红色方块
    return img

if __name__ == '__main__':
    target      = identify_GetTarget()
    targets = target.get_arm_coordinates(154,278,224,348)
     # 输出结果
    print("Detected Targets:", targets)
    # ta =  {'red': (234, 233), 'green': (455, 222)}
    ta =  {'start':targets}
    # 假设我们有一个目标位置进行抓取测试
    if targets:
        target.vlm_target_run(ta)