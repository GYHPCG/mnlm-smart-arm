import numpy as np
from spatialmath.base import e2h
from roboticstoolbox import DHRobot, RevoluteMDH
from machinevisiontoolbox import CentralCamera

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

def compute_target_pose(cam, DFbot1, target_point):
    """
    计算目标点的位姿矩阵
    """
    # 视觉校正
    T1 = DFbot1.fkine([0, -np.pi / 3, np.pi / 3, np.pi, 0, 0])

    # 投影到图像平面
    p = cam.project_point(target_point, pose=T1)
    cam.plot_point(target_point, pose=T1)

    # 求解深度
    mtx = np.array([
        [919.21981864, 0., 356.41270451],
        [0., 913.16565134, 236.9305],
        [0., 0., 1.]
    ])
    K = mtx
    extrinsic = np.linalg.inv(T1)
    point_camera = extrinsic @ np.append(target_point, 1)
    point_2d = K @ point_camera[:3]
    depth = point_2d[2]
    point_2d /= depth

    # 逆投影到三维空间
    xaxis = 356.41270451 - 100
    yaxis = 226.9298497 + 50    
    point_2d = depth * np.array([xaxis, yaxis, 1])
    point_camera = e2h(np.linalg.inv(K) @ point_2d)
    new_point_3d = np.array(np.linalg.inv(extrinsic) @ point_camera)

    return new_point_3d

def solve_inverse_kinematics(DFbot2, target_3d):
    """
    使用逆运动学求解关节角度
    """
    T21 = DFbot2.fkine([0, -np.pi / 3, np.pi / 3, np.pi, 0])
    T2 = np.array(T21)
    T2[:, -1] = target_3d.flatten()

    sol = DFbot2.ikine_LM(
        T2,
        q0=[0, -np.pi / 3, np.pi / 3, np.pi, 0],
        ilimit=5000,
        slimit=5000,
        joint_limits=True,
        tol=0.001
    )
    return sol.q

def convert_to_servo_angles(joint_angles):
    """
    将关节角度转换为舵机角度
    """
    deg = [x / np.pi * 180 for x in joint_angles]
    d1 = deg[0] + 90
    d2 = -deg[1]
    d3 = 90 - deg[2]
    d4 = 180 - deg[3]
    d5 = deg[4] + 90
    return [d1, d2, d3, d4, d5]

def main():
    # 初始化相机和机械臂
    cam = initialize_camera()
    DFbot1, DFbot2 = initialize_robot()

    # 输入目标点
    target_point = np.array([-0.165, 0, -0.01])

    # 计算目标点的位姿
    target_3d = compute_target_pose(cam, DFbot1, target_point)

    # 使用逆运动学求解关节角度
    joint_angles = solve_inverse_kinematics(DFbot2, target_3d)

    # 转换为舵机角度
    servo_angles = convert_to_servo_angles(joint_angles)

    print("舵机角度：", servo_angles)

if __name__ == "__main__":
    main()