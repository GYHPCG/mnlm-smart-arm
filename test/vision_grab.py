import numpy as np
import math
from spatialmath import SE3
from machinevisiontoolbox import mkcube
from spatialmath.base import e2h, h2e
from roboticstoolbox import *
from machinevisiontoolbox import CentralCamera


cam = CentralCamera(f=[919.21981864*10e-6,913.16565134*10e-6], rho=10e-6, imagesize=[640, 480], pp=[356.41270451,236.9305], name="mycamera")
print(cam)

#真实世界坐标系下的点
P=np.array([-0.18, 0, -0.01])

# 机械臂舵机
DFbot1 = DHRobot(
    [                 
                    RevoluteMDH(d=0.04145,qlim=np.array([-np.pi,np.pi])),            
                    RevoluteMDH(alpha=np.pi/2,qlim=np.array([-np.pi,np.pi])),
                    RevoluteMDH(a=-0.08285,qlim=np.array([-np.pi,np.pi])),
                    RevoluteMDH(a=-0.08285,qlim=np.array([-np.pi,np.pi])),
                    RevoluteMDH(alpha=-np.pi/2,qlim=np.array([0,np.pi])),
                    RevoluteMDH(a=0.04,d=0.057,qlim=np.array([-np.pi,np.pi]))
                  
    ],
    name="DFbot",
)

# 机械臂夹爪
DFbot2 = DHRobot(
    [                 
                    RevoluteMDH(d=0.04145,qlim=np.array([-np.pi/2,np.pi/2])),            
                    RevoluteMDH(alpha=np.pi/2,qlim=np.array([-np.pi/2,np.pi/2])),
                    RevoluteMDH(a=-0.08285,qlim=np.array([-np.pi/2,np.pi/2])),
                    RevoluteMDH(a=-0.08285,qlim=np.array([-np.pi/2,np.pi])),
                    RevoluteMDH(alpha=-np.pi/2,d=0.11,qlim=np.array([0,np.pi]))
                  
    ],
    name="DFbot",
)

#视觉校正
T1=DFbot1.fkine([0,-np.pi/3,np.pi/3,np.pi,0,0])

#单一点投影
p = cam.project_point(P, pose=T1 )
cam.plot_point(P, pose=T1 )

#立方体投影

X, Y, Z = mkcube(s=0.03,centre=(-0.165, 0, -0.025), edge=True)
cam.plot_wireframe(X, Y, Z,pose=T1)

#求解深度
mtx=np.array([[919.21981864,   0.        , 356.41270451],
       [  0.        , 913.16565134, 236.9305    ],
       [  0.        ,   0.        ,   1.        ]])

# 内参矩阵
K = mtx
 
# 位姿矩阵
pose=T1
 
# 外参矩阵（位姿矩阵的逆）
extrinsic = np.linalg.inv(pose)
 
# 3D点（世界坐标系）
point_3d = np.array([-0.165, 0, -0.01, 1])
 
# 将点从世界坐标系转换到相机坐标系
point_camera = extrinsic @ point_3d
 
# 投影到图像平面
point_2d = K @ point_camera[:3]
depth=point_2d[2]
point_2d /= depth  # 归一化

# 将相机坐标系下的点(x,y)转换到世界坐标系
xaxis=356.41270451-100
yaxis=226.9298497+50
point_2d=depth*np.array([xaxis,yaxis,1])
point_camera=e2h(np.linalg.inv(K)@point_2d)
new_point_3d=np.array(np.linalg.inv(extrinsic)@point_camera)

T21=DFbot2.fkine([0,-np.pi/3,np.pi/3,np.pi,0])

T2=np.array(T21)
T2[:,-1]=new_point_3d.flatten()
#T2[2,-1]=0.01

sol = DFbot2.ikine_LM(T2,q0=[0,-np.pi/3,np.pi/3,np.pi,0],ilimit=5000, slimit=5000,joint_limits=True,tol=0.001)
state = sol.q

# 转为角度

deg=[x/np.pi*180 for x in state]
def convert_deg(deg):
    d1=deg[0]+90
    d2=-deg[1]
    d3=90-deg[2]
    d4=180-deg[3]
    d5=deg[4]+90
    return [d1,d2,d3,d4,d5]
