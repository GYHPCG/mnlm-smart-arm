'''
Author: '破竹' '2986779260@qq.com'
Date: 2025-03-25 22:13:55
LastEditors: '破竹' '2986779260@qq.com'
LastEditTime: 2025-04-10 14:34:34
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
import json
from listener import get_received_command 
import os


def generate_prompt(command_str)->str:
    api_document_path = './robot_arm_api.md'
    print("api_document_path: ", api_document_path)

    if os.path.exists(os.path.expanduser(api_document_path)):
                with open(os.path.expanduser(api_document_path), "r",encoding='utf-8') as f:
                    api_document = "".join(f.readlines())

    SYSTEM_PROMOPT=f"""
    你有一个大脑和一个机械臂，机械臂内置了一些函数和相关的API文档，请你根据我的指令，特别参考API文档，生成对应的动作的函数并输出(动作可能是由多个函数组合而来)。
    【以下是所有内置函数介绍】
    定义机械臂跳舞函数，arm_dance()，让机械臂跳舞
    定义机械臂归中函数，arm_zero()，让机械臂回到原点
    定义机械臂rgb灯光函数，rgb_control(r,g,b)，控制机械臂灯光颜色
    定义机械臂归中函数，arm_zero()，让机械臂回到原点
    定义控制第i个舵机函数，move_single_servo(id, angle, op_time)，控制第i个舵机运动，id是舵机编号，angle是舵机角度，op_time是舵机转动时间
    定义控制所有舵机函数，move_all_servo(angle, op_time)，控制所有舵机运动，angle[6]是对应的每个舵机角度，op_time是舵机转动时间

    【输出json格式】
    你直接输出json即可
    在"function"键中，输出函数名列表，列表中每个元素都是字符串，代表要运行的函数名称和参数。每个函数既可以单独运行，也可以和其他函数先后运行。列表元素的先后顺序，表示执行函数的先后顺序
    在"response"键中，根据我的指令和你编排的动作，以第一人称输出你回复我的话，不要超过20个字，可以幽默和发散，用上歌词、台词、互联网热梗、名场面。比如李云龙的台词、甄嬛传的台词、练习时长两年半。

    【以下是一些具体的例子】
    An example output would be:
        {{
            "function": ["move_single_servo(1,60,500)","move_single_servo(2,50,500)"],
            "response": "好的，我开始执行动作。" 
        }},
        {{
            "function": ["arm_rgb_control(255,0,0)","arm_dance()"],
            "response": "好的，我开始执行 arm_rgb_control 动作。" 
        }},
        {{
            "function": ["move_single_servo(2,90,500)"，],
            "response": "好的，执行 move_single_servo 动作。" 
        }},
        {{
            "function": ["move_all_servo([0, 90, 90, 45, 32, 0],op_time)"],
            "response": "好的，执行 move_all_servo 动作。" 
        }},

    Note: The list of operations can be 1 ore many. And the servos are with ids from 1 to 6.
    ---
    API Document:
    ---
    {api_document}
    ---


    你现在的任务是：
    ---
    {command_str}
    ---
    """  
    
    return SYSTEM_PROMOPT
      
def assiant(command_str):
    client = OpenAI(
        # openai系列的sdk，包括langchain，都需要这个/v1的后缀
        base_url='https://api.openai-proxy.org/v1',
        api_key='sk-Cinx17W4V8Ss4B7HSfxUrf2kikhbvZE7EGHy5SYwWJBWs6Qm',
    )
    # command = get_received_command()
    PROMOPT= generate_prompt(command_str)
    chat_completion = client.chat.completions.create(
        # name="Voice Robot Controller",
        # instructions="""
        #     You have a brain and a robot arm, and you receive voice command from the human being, and respond accordingly.
        # """,
        messages=[
            {
                "role": "user",
                "content": PROMOPT,
            }
        ],
        # tools=tool_signatures,
        model="gpt-4o",
    ) # 如果是其他兼容模型，比如deepseek，直接这里改模型名即可，其他都不用动

    print(chat_completion)
    # 提取返回结果的 content 内容
    response_content = chat_completion.choices[0].message.content.strip()
    
    print("执行动作\n")
    print(response_content)
    # 将字符串解析为字典
    response_content = json.loads(response_content)
    
    for each in response_content['function']: # 运行智能体规划编排的每个函数
            print('开始执行动作', each)
            eval(each)

if __name__ == '__main__':
    assiant("旋转180度")