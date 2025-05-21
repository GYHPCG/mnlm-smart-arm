#!/usr/bin/env python3
#coding=utf-8
import time
from Arm_Lib import Arm_Device

# Get DOFBOT object
Arm = Arm_Device()
time.sleep(.1)

#  enable=1: clamp,=0: release
def arm_clamp_block(enable):
    if enable == 0:
        Arm.Arm_serial_servo_write(6, 60, 400)
    else:
        Arm.Arm_serial_servo_write(6, 135, 400)
    time.sleep(.5)

    
# Define control DOFBOT function, control No.1-No.5 servo，p=[S1,S2,S3,S4,S5]
def arm_move(p, s_time = 1000):
    for i in range(5):
        id = i + 1
        if id == 5:
            time.sleep(.1)
            Arm.Arm_serial_servo_write(id, p[i], int(s_time*1.2))
        else :
            Arm.Arm_serial_servo_write(id, p[i], s_time)
        time.sleep(1)
    time.sleep(s_time/1000)

# DOFBOT moves up
def arm_move_up():
    Arm.Arm_serial_servo_write(2, 90, 1500)
    Arm.Arm_serial_servo_write(3, 90, 1500)
    Arm.Arm_serial_servo_write(4, 90, 1500)
    time.sleep(.1)
    

# Define variable parameters at different locations
p_mould = [90, 130, 0, 0, 90]
p_top = [90, 80, 50, 50, 270]
p_Brown = [90, 53, 33, 36, 270]

p_Yellow = [65, 22, 64, 56, 270]
p_Red = [117, 19, 66, 56, 270]

p_Green = [136, 66, 20, 29, 270]
p_Blue = [44, 66, 20, 28, 270]

# Make the DOFBOT move to a position ready to grab
def move_to_ready():
    arm_clamp_block(0)
    arm_move(p_mould, 1000)
    time.sleep(1)

def vlm_move_ready():
    rotate = Arm.Arm_serial_servo_read(1)
    # xy=[90,135]
    joints_0 = [rotate, 135, 0, 0, 90, 30]
    Arm.Arm_serial_servo_write6_array(joints_0, 1000)
def top_view_shot_full_fushi():
#     Arm.Arm_serial_servo_write6(89.71029649148431, 45.25613284306083, 91.86258487811448, -35, 89.71253294095186,0,1000)
#     arm_move([89.71029649148431, 45.25613284306083, 91.86258487811448, -35, 89.71253294095186],1000)
    Arm.Arm_serial_servo_write6(0+90,60, 90-60, 180-180, 0+90,0,1000)
    time.sleep(3)

# Grab a block from the gray block and place it on the yellow block.
def gray_to_yellow():
    arm_move(p_top, 1000)
    arm_move(p_Brown, 1000)
    arm_clamp_block(1)

    arm_move(p_top, 1000)
    arm_move(p_Yellow, 1000)
    arm_clamp_block(0)


    arm_move(p_mould, 1000)

    time.sleep(1)

# Grab a block from the gray block and place it on the red block.
def gray_to_red():
    arm_move(p_top, 1000)
    arm_move(p_Brown, 1000)
    arm_clamp_block(1)

    arm_move(p_top, 1000)
    arm_move(p_Red, 1000)
    arm_clamp_block(0)

    arm_move_up()
    arm_move(p_mould, 1100)

    time.sleep(1)


# Grab a block from the gray block and place it on the green block.
def gray_to_green():
    arm_move(p_top, 1000)
    arm_move(p_Brown, 1000)
    arm_clamp_block(1)

    arm_move(p_top, 1000)
    arm_move(p_Green, 1000)
    arm_clamp_block(0)

    arm_move_up()
    arm_move(p_mould, 1100)

    time.sleep(1)

# Grab a block from the gray block and place it on the blue block.
def gray_to_blue():
    arm_move(p_top, 1000)
    arm_move(p_Brown, 1000)
    arm_clamp_block(1)

    arm_move(p_top, 1000)
    arm_move(p_Blue, 1000)
    arm_clamp_block(0)

    arm_move_up()
    arm_move(p_mould, 1100)

    time.sleep(1)

def start_to_end(p_start, p_end, p_time=1000):
    arm_move(p_top,p_time)
    arm_move(p_start,p_time)
    arm_clamp_block(1)

    arm_move(p_top,p_time)
    arm_move(p_end,p_time)
    arm_clamp_block(0)

    arm_move_up()
    arm_move(p_mould,time+100)

    time.sleep(1)



if __name__ == '__main__':
    move_to_ready()
    gray_to_yellow()
    gray_to_red()
    gray_to_green()
    gray_to_blue()
    del Arm  # 释放资源
    print('程序结束！')
