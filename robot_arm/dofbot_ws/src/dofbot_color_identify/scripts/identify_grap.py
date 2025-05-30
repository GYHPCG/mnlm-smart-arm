#!/usr/bin/env python
# coding: utf-8

import Arm_Lib
from time import sleep


class identify_grap:
    def __init__(self):
        # 设置移动状态
        self.move_status = True
        # 创建机械臂实例
        self.arm = Arm_Lib.Arm_Device()
        # 夹爪加紧角度
        self.grap_joint = 150

    def move(self, joints, joints_down):
        '''
        移动过程
        :param joints: 移动到物体位置的各关节角度
        :param joints_down: 机械臂抬起各关节角度
        :param color_angle: 移动到旁边的角度
        '''
        rotate = self.arm.Arm_serial_servo_read(1)
        joints_uu = [rotate, 80, 50, 50, 265, self.grap_joint]
        # 抬起
        joints_up = [joints_down[0], 80, 50, 50, 265, 30]
        # 架起
        self.arm.Arm_serial_servo_write6_array(joints_uu, 1500)
        sleep(1.5)
        # 开合夹爪
        for i in range(5):
            self.arm.Arm_serial_servo_write(6, 180, 100)
            sleep(0.08)
            self.arm.Arm_serial_servo_write(6, 30, 100)
            sleep(0.08)
#         # 松开夹爪
#         self.arm.Arm_serial_servo_write(6, 0, 500)
#         sleep(0.5)
        # 移动至物体位置
        self.arm.Arm_serial_servo_write6_array(joints, 500)
        sleep(0.5)
        # 进行抓取,夹紧夹爪
        self.arm.Arm_serial_servo_write(6, self.grap_joint, 500)
        sleep(0.5)
        # 架起
        self.arm.Arm_serial_servo_write6_array(joints_uu, 1000)
        sleep(1)
        # 抬起至对应位置上方
        self.arm.Arm_serial_servo_write(1, joints_down[0], 500)
        sleep(0.5)
        # 抬起至对应位置
        self.arm.Arm_serial_servo_write6_array(joints_down, 1000)
        sleep(1)
        # 释放物体,松开夹爪
        self.arm.Arm_serial_servo_write(6, 30, 500)
        sleep(0.5)
        # 抬起
        self.arm.Arm_serial_servo_write6_array(joints_up, 1000)
        sleep(1)

    def move_no_place(self, joints, joints_down):
        '''
        移动过程
        :param joints: 移动到物体位置的各关节角度
        :param joints_down: 机械臂抬起各关节角度
        :param color_angle: 移动到旁边的角度
        '''
        rotate = self.arm.Arm_serial_servo_read(1)
        print(f"no_place rotate: {rotate}")
        joints_uu = [rotate, 80, 50, 50, 265, self.grap_joint]
        # 抬起
        joints_up = [joints_down[0], 80, 50, 50, 265, 30]
        # 架起
        self.arm.Arm_serial_servo_write6_array(joints_uu, 1500)
        sleep(1.5)
        # 开合夹爪
        for i in range(5):
            self.arm.Arm_serial_servo_write(6, 180, 100)
            sleep(0.08)
            self.arm.Arm_serial_servo_write(6, 30, 100)
            sleep(0.08)
#         # 松开夹爪
#         self.arm.Arm_serial_servo_write(6, 0, 500)
#         sleep(0.5)
        # 移动至物体位置
        self.arm.Arm_serial_servo_write6_array(joints, 500)
        sleep(0.5)
        # 进行抓取,夹紧夹爪
        self.arm.Arm_serial_servo_write(6, self.grap_joint, 500)
        sleep(0.5)
        # # 架起
        self.arm.Arm_serial_servo_write6_array(joints_uu, 1000)
        sleep(1)
        # 抬起至对应位置上方
        self.arm.Arm_serial_servo_write(1, joints_down[0], 500)
        sleep(0.5)
        #抬起至对应位置
        self.arm.Arm_serial_servo_write6_array(joints_down, 1000)
        sleep(1)
        # # 释放物体,松开夹爪
        # self.arm.Arm_serial_servo_write(6, 30, 500)
        # sleep(0.5)
        # # 抬起
        # self.arm.Arm_serial_servo_write6_array(joints_up, 1000)
        sleep(1)

    def vlm_move(self, joints,grasp_joint=150):
        '''
        机械臂移动函数
        :param name:识别的颜色
        :param joints: 反解求得的各关节角度
        '''
        if self.move_status == True:
            # 此处设置,需执行完本次操作,才能向下运行
            self.move_status = False
            # print ("red")
            # print (joints[0], joints[1], joints[2], joints[3], joints[4])
            # 获得目标关节角
            joints = [joints[0], joints[1], joints[2], joints[3], 265, 30]
            # 移动到垃圾桶上方对应姿态
#             joints_down = [45, 80, 35, 40, 265, self.grap_joint]
            # 移动到归中位置
            self.grap_joint = grasp_joint

            rotate = self.arm.Arm_serial_servo_read(1)
            joints_center = [rotate, 135, 0, 45, 90, self.grap_joint]
            # 移动
            self.move_no_place(joints, joints_center)
            # 移动完毕
            self.move_status = True

    def move_to(self, joints):
        '''
        机械臂移动函数
        :param name:识别的颜色
        :param joints: 反解求得的各关节角度
        '''
        if self.move_status == True:
            # 此处设置,需执行完本次操作,才能向下运行
            self.move_status = False
            # print ("red")
            # print (joints[0], joints[1], joints[2], joints[3], joints[4])
            # 获得目标关节角
            joints = [joints[0], joints[1], joints[2], joints[3], 265, 30]
            # 移动到垃圾桶上方对应姿态
#             joints_down = [45, 80, 35, 40, 265, self.grap_joint]
            # 移动到垃圾桶位置放下对应姿态
            # joints_down = [45, 50, 20, 60, 265, self.grap_joint]
            
            # 移动
            self.arm.Arm_serial_servo_write6_array(joints, 1000)
            sleep(0.5)
            # 移动完毕
            self.move_status = True
            
    def place_to(self, joints):
        '''
        机械臂放置函数
        :param name:识别的颜色
        :param joints: 反解求得的各关节角度
        '''
        if self.move_status == True:
            # 此处设置,需执行完本次操作,才能向下运行
            self.move_status = False
            # print ("red")
            # print (joints[0], joints[1], joints[2], joints[3], joints[4])
            # 获得目标关节角
            joints = [joints[0], joints[1], joints[2], joints[3], 265, self.grap_joint]
            # 移动到垃圾桶上方对应姿态
#             joints_down = [45, 80, 35, 40, 265, self.grap_joint]
            # 移动到垃圾桶位置放下对应姿态
            # joints_down = [45, 50, 20, 60, 265, self.grap_joint]
            
            # 移动
            self.arm.Arm_serial_servo_write6_array(joints, 1000)
            sleep(1)
            # 移动完毕
            # # 释放物体,松开夹爪
            self.arm.Arm_serial_servo_write(6, 30, 500)
            sleep(0.5)
            # 抬起
            # self.arm.Arm_serial_servo_write6_array(joints_up, 1000)
            rotate = self.arm.Arm_serial_servo_read(1)
            self.arm.Arm_serial_servo_write6(rotate, 135, 0, 45, 90, 30, 1000)
            sleep(1)
                
            self.move_status = True
    def double_vlm_move(self,start_joints,end_joints,grasp_joint=150):
        '''
        机械臂移动函数
        :param start_joints: 抓取位置反解求得的各关节角度
        :param end_joints: 放置物体位置反解求得的各关节角度
        '''
        if self.move_status == True:
            # 此处设置,需执行完本次操作,才能向下运行
            self.move_status = False
            self.grap_joint = grasp_joint
            # print ("red")
            # print (joints[0], joints[1], joints[2], joints[3], joints[4])
            # 获得目标关节角
            joints = [start_joints[0], start_joints[1], start_joints[2], start_joints[3], 265, 50]
            # 移动到垃圾桶上方对应姿态
#             joints_down = [45, 80, 35, 40, 265, self.grap_joint]
            # 移动到垃圾桶位置放下对应姿态
            joints_down = [end_joints[0], end_joints[1], end_joints[2], end_joints[3], 265, self.grap_joint]
            # 移动
            self.move(joints, joints_down)
            # 移动完毕
            self.move_status = True
        
    def identify_move(self, name, joints):
        '''
        机械臂移动函数
        :param name:识别的颜色
        :param joints: 反解求得的各关节角度
        '''
        if name == "red" and self.move_status == True:
            # 此处设置,需执行完本次操作,才能向下运行
            self.move_status = False
            # print ("red")
            # print (joints[0], joints[1], joints[2], joints[3], joints[4])
            # 获得目标关节角
            joints = [joints[0], joints[1], joints[2], joints[3], 265, 30]
            # 移动到垃圾桶上方对应姿态
#             joints_down = [45, 80, 35, 40, 265, self.grap_joint]
            # 移动到垃圾桶位置放下对应姿态

            joints_down = [45, 50, 20, 60, 265, self.grap_joint]
            # 移动
            self.move(joints, joints_down)
            # 移动完毕
            self.move_status = True
        if name == "blue" and self.move_status == True:
            self.move_status = False
            # print ("blue")
            # print (joints[0], joints[1], joints[2], joints[3], joints[4])
            joints = [joints[0], joints[1], joints[2], joints[3], 265, 30]
#             joints_down = [27, 110, 0, 40, 265, self.grap_joint]
            joints_down = [27, 75, 0, 50, 265, self.grap_joint]
            self.move(joints, joints_down)
            self.move_status = True
        if name == "green" and self.move_status == True:
            self.move_status = False
            # print ("green")
            # print (joints[0], joints[1], joints[2], joints[3], joints[4])
            joints = [joints[0], joints[1], joints[2], joints[3], 265, 30]
#             joints_down = [152, 110, 0, 40, 265, self.grap_joint]
            joints_down = [147, 75, 0, 50, 265, self.grap_joint]
            self.move(joints, joints_down)
            self.move_status = True
        if name == "yellow" and self.move_status == True:
            self.move_status = False
            # print ("yellow")
            # print (joints[0], joints[1], joints[2], joints[3], joints[4])
            joints = [joints[0], joints[1], joints[2], joints[3], 265, 30]
#             joints_down = [137, 80, 35, 40, 265, self.grap_joint]
            joints_down = [133, 50, 20, 60, 265, self.grap_joint]
            self.move(joints, joints_down)
            self.move_status = True