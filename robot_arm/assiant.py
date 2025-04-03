'''
Author: '破竹' '2986779260@qq.com'
Date: 2025-03-25 22:13:55
LastEditors: '破竹' '2986779260@qq.com'
LastEditTime: 2025-04-03 20:31:14
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

import json
from listener import get_received_command 

SYSTEM_PROMOPT='''
你是我的机械臂助手，机械臂内置了一些函数，请你根据我的指令来调用这些函数。
【以下是所有内置函数介绍】
定义夹积木块函数,arm_clamp_block(enable)，enable=1：夹住，=0：松开
定义移动机械臂函数,同时控制1-5号舵机运动,arm_move(p, s_time = 500)，p=[S1,S2,S3,S4,S5],其中S1-S4分别是舵机1-4的角度，范围为(0,180),小于90度向前弯，大于向后弯， S5为舵机5的角度范围(0,270)，s_time是舵机运动时间，单位ms
定义机械臂跳舞函数，arm_dance()，让机械臂跳舞
定义机械臂归零函数，arm_zero()，让机械臂回到原点
定义机械臂rgb灯光函数，arm_rgb_control()，让机械臂灯光颜色随机变化
定义机械臂归中函数，arm_zero()，让机械臂回到原点
定义机械臂获取舵机角度函数，arm_read_servo(id)->int，id=1-6，返回舵机id的角度
定义机械臂控制舵机函数，ctrl_servo(id, px, py)，id=1-5，px,py是舵机id对应的位置，单位是mm，比如ctrl_servo(1, 100, 200)，表示将舵机1的位置设置为100mm，200mm。

【输出json格式】
你直接输出json即可，从{开始，不要输出包含```json的开头或结尾
在'function'键中，输出函数名列表，列表中每个元素都是字符串，代表要运行的函数名称和参数。每个函数既可以单独运行，也可以和其他函数先后运行。列表元素的先后顺序，表示执行函数的先后顺序
在'response'键中，根据我的指令和你编排的动作，以第一人称输出你回复我的话，不要超过20个字，可以幽默和发散，用上歌词、台词、互联网热梗、名场面。比如李云龙的台词、甄嬛传的台词、练习时长两年半。

【以下是一些具体的例子】
我的指令：回到原点。你输出：{'function':['back_zero()'], 'response':'回家吧，回到最初的美好'}
我的指令：先回到原点，然后跳舞。你输出：{'function':['back_zero()', 'arm_dance()'], 'response':'我的舞姿，练习时长两年半'}

你现在的任务是：
'''

def assiant(command_str):
    client = OpenAI(
        # openai系列的sdk，包括langchain，都需要这个/v1的后缀
        base_url='https://api.openai-proxy.org/v1',
        api_key='sk-Cinx17W4V8Ss4B7HSfxUrf2kikhbvZE7EGHy5SYwWJBWs6Qm',
    )
    # command = get_received_command()
    PROMOPT= command_str
    chat_completion = client.chat.completions.create(
        # name="Voice Robot Controller",
        # instructions="""
        #     You have a brain and a robot arm, and you receive voice command from the human being, and respond accordingly.
        # """,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMOPT + PROMOPT,
            }
        ],
        # tools=tool_signatures,
        model="gpt-3.5-turbo-1106",
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
    assiant("先回到原点，然后跳舞。")