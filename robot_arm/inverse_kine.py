import math

# 定义机械臂的连杆长度（单位：mm）
L1 = 100  # 基座到肩部的长度
L2 = 100  # 肩部到肘部的长度
L3 = 100  # 肘部到腕部的长度
L4 = 50   # 腕部到末端执行器的长度

def inverse_kinematics(x, y, z, wrist_angle=0):
    """
    根据目标位置 (x, y, z) 计算舵机角度 θ1, θ2, θ3, θ4, θ5
    :param x: 目标位置的 x 坐标
    :param y: 目标位置的 y 坐标
    :param z: 目标位置的 z 坐标
    :param wrist_angle: 末端执行器的目标姿态角度（单位：度）
    :return: θ1, θ2, θ3, θ4, θ5 的角度（单位：度）
    """
    # 计算基座旋转角度 θ1
    theta1 = math.atan2(y, x)

    # 计算平面距离 r 和高度 z
    r = math.sqrt(x**2 + y**2)
    z = z - L1

    # 检查目标点是否在机械臂的工作空间内
    if r > (L2 + L3) or r < abs(L2 - L3):
        raise ValueError("目标点超出机械臂的工作空间范围！")

    # 计算肘部角度 θ3
    cos_theta3 = (r**2 + z**2 - L2**2 - L3**2) / (2 * L2 * L3)
    theta3 = math.acos(cos_theta3)

    # 计算肩部角度 θ2
    theta2 = math.atan2(z, r) - math.atan2(L3 * math.sin(theta3), L2 + L3 * math.cos(theta3))

    # 计算腕部角度 θ4
    theta4 = math.radians(wrist_angle) - (theta2 + theta3)

    # 末端执行器旋转角度 θ5
    theta5 = 0  # 根据任务需求设置

    # 将弧度转换为角度
    theta1_deg = math.degrees(theta1)
    theta2_deg = math.degrees(theta2)
    theta3_deg = math.degrees(theta3)
    theta4_deg = math.degrees(theta4)
    theta5_deg = math.degrees(theta5)

    return theta1_deg, theta2_deg, theta3_deg, theta4_deg, theta5_deg

# 测试代码
if __name__ == "__main__":
    # 输入目标位置
    target_x = 150  # 目标 x 坐标
    target_y = 50   # 目标 y 坐标
    target_z = 100  # 目标 z 坐标

    try:
        angles = inverse_kinematics(target_x, target_y, target_z, wrist_angle=0)
        print(f"舵机角度：θ1 = {angles[0]:.2f}°, θ2 = {angles[1]:.2f}°, θ3 = {angles[2]:.2f}°, θ4 = {angles[3]:.2f}°, θ5 = {angles[4]:.2f}°")
    except ValueError as e:
        print(e)