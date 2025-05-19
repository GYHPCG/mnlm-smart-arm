'''
Author: '破竹' '2986779260@qq.com'
Date: 2025-03-25 22:13:55
LastEditors: '破竹' '2986779260@qq.com'
LastEditTime: 2025-05-07 22:18:57
FilePath: \code\mnlm-smart-arm\assiant.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''

from openai import OpenAI
from arm_dance import arm_dance
from arm_clamp_block import arm_clamp_block
from arm_move import arm_move
from arm_rgb_control import rgb_control
from arm_zero import arm_zero 
from arm_read_servo import read_servo
from arm_ctrl_servo import ctrl_servo
from arm_left_right import left_right
from arm_rotate import arm_rotate
from move_single_servo import move_single_servo
from move_all_servo import move_all_servo
from grab_block import vlm_move_ready,top_view_shot_full_fushi
from utils_vlm import move_to,place_to
import json
from listener import get_received_command 
import os
from vlm_agent import vlm_move,tradition_grasp_object
from vision_identify import vision_identify 
import sys
sys.path.append("/home/dofbot/code/mnlm-smart-arm/robot_arm/dofbot_ws/src")
from dofbot_color_follow.follow_color_act import follow_color_run 
from dofbot_snake_follow.scripts.snake_follow import  snake_follow_run

def assiant(command_str):
    print(command_str)
    # 将字符串解析为字典
    response_content = json.loads(command_str)
    for each in response_content['function']: # 运行智能体规划编排的每个函数
            print('开始执行动作', each)
            eval(each)

if __name__ == '__main__':
    assiant("旋转180度")