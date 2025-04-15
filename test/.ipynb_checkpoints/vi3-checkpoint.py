# -*- coding: utf-8 -*-
import numpy as np
import math
from spatialmath.base import e2h
from roboticstoolbox import DHRobot, RevoluteMDH
from machinevisiontoolbox import CentralCamera
from grab_block import arm_move,move_to_ready,top_view_shot,arm_clamp_block
def initialize_camera():
    """
    初始化相机模型
    """
    cam = CentralCamera(
        f=[919.21981864 * 10e-6, 913.16565134 * 10e-6],
        rho=10e-6,
        imagesize=[640, 480],
        pp=[356.41270451, 236.9305],
        name="mycamera"
    )
    return cam

def initialize_robot():
    """
    初始化机械臂模型
    """
    # 机械臂舵机
    DFbot1 = DHRobot(
        [
            RevoluteMDH(d=0.04145, qlim=np.array([-np.pi, np.pi])),
            RevoluteMDH(alpha=np.pi / 2, qlim=np.array([-np.pi, np.pi])),
            RevoluteMDH(a=-0.08285, qlim=np.array([-np.pi, np.pi])),
            RevoluteMDH(a=-0.08285, qlim=np.array([-np.pi, np.pi])),
            RevoluteMDH(alpha=-np.pi / 2, qlim=np.array([0, np.pi])),
            RevoluteMDH(a=0.04, d=0.057, qlim=np.array([-np.pi, np.pi]))
        ],
        name="DFbot",
    )

    # 机械臂夹爪
    DFbot2 = DHRobot(
        [
            RevoluteMDH(d=0.04145, qlim=np.array([-np.pi / 2, np.pi / 2])),
            RevoluteMDH(alpha=np.pi / 2, qlim=np.array([-np.pi / 2, np.pi / 2])),
            RevoluteMDH(a=-0.08285, qlim=np.array([-np.pi / 2, np.pi / 2])),
            RevoluteMDH(a=-0.08285, qlim=np.array([-np.pi / 2, np.pi])),
            RevoluteMDH(alpha=-np.pi / 2, d=0.11, qlim=np.array([0, np.pi]))
        ],
        name="DFbot",
    )
    return DFbot1, DFbot2

def pixel_to_servo_angles(x_pixel, y_pixel, depth, cam, DFbot1, DFbot2):
    """
    将相机坐标 (x, y) 和深度转换为舵机角度
    :param x_pixel: 相机坐标 x
    :param y_pixel: 相机坐标 y
    :param depth: 深度值
    :param cam: 相机模型
    :param DFbot1: 机械臂模型 1
    :param DFbot2: 机械臂模型 2
    :return: 舵机角度列表
    """
    # 相机内参矩阵
    K = np.array([
        [919.21981864, 0., 356.41270451],
        [0., 913.16565134, 236.9305],
        [0., 0., 1.]
    ])

    # 机械臂的正运动学，计算当前位姿
    T1 = DFbot1.fkine([0, -np.pi / 3, np.pi / 3, np.pi, 0, 0])
    T1 = DFbot1.fkine([0,-np.pi/3,np.pi/3,np.pi,0,np.pi/2])
    # 外参矩阵（位姿矩阵的逆）
    extrinsic = np.linalg.inv(T1)

    # 将像素坐标转换为相机坐标系中的点
    point_2d = depth * np.array([x_pixel, y_pixel, 1])
    point_camera = e2h(np.linalg.inv(K) @ point_2d)

    # 将相机坐标系中的点转换到世界坐标系
    new_point_3d = np.array(np.linalg.inv(extrinsic) @ point_camera)
    
    print("step1")
    # 使用逆运动学求解关节角度
    T21 = DFbot2.fkine([0, -np.pi / 3, np.pi / 3, np.pi, 0])
    T2 = np.array(T21)
    T2[:, -1] = new_point_3d.flatten()
    
    print("step2")
    sol = DFbot2.ikine_LM(
        T2,
        q0=[0, -np.pi / 3, np.pi / 3, np.pi, 0],
        ilimit=5000,
        slimit=5000,
        joint_limits=True,
        tol=0.001
    )
    joint_angles = sol.q
#     joint_angles = [ 0.   ,      -0.65289473 , 0.66444728 , 3.12870043 , 0.        ]
#     joint_angles =  [ 0. ,        -0.40185891 , 0.51018213  ,3.0328737  , 0.        ]
#     joint_angles = [-0.00505628, -0.63278889, -0.03250824, -2.47971392, -0.00501725]
#     joint_angles = [ 0.05250454,-0.67323703,0.68610388,3.12762084,0.0524625 ]
    print("step3")
    print(joint_angles)
    # 转换为舵机角度
    deg = [x / np.pi * 180 for x in joint_angles]
    d1 = deg[0] + 90
    d2 = -deg[1]
    d3 = 90 - deg[2]
    d4 = 180 - deg[3]
    d5 = deg[4] + 90
    return [d1, d2, d3, d4, d5]

def init_grab(x_pixel,y_pixel):
    # 初始化相机和机械臂
    cam = initialize_camera()
    DFbot1, DFbot2 = initialize_robot()

    # 输入相机坐标和深度
    x_pixel = 556  # 示例像素坐标 x
    y_pixel = 326  # 示例像素坐标 y
    depth = 0.05    # 示例深度（单位：米）

    # 计算舵机角度
    servo_angles = pixel_to_servo_angles(x_pixel, y_pixel, depth, cam, DFbot1, DFbot2)

    print("舵机角度：", servo_angles)
    move_to_ready()
    top_view_shot()
#     servo_angles = [89.71029649148431, 45.25613284306083, 91.86258487811448, -35, 89.71253294095186]
    arm_move(servo_angles)
    arm_clamp_block(1)
if __name__ == "__main__":
    init_grab( x_pixel = 256,y_pixel = 128)