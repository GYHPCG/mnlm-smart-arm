'''
Author: '破竹' '2986779260@qq.com'
Date: 2025-03-25 22:13:55
LastEditors: '破竹' '2986779260@qq.com'
LastEditTime: 2025-05-21 17:09:38
FilePath: \code\mnlm-smart-arm\assiant.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''

from openai import OpenAI
import json
from rag_indexer import get_rag_result
from command_send import send_commands_to_service
import os
import time
import threading

def generate_prompt(command_str)->str:
    robot_arm_document_path = './robot_arm.md'
    print("api_document_path: ", robot_arm_document_path)

    if os.path.exists(os.path.expanduser(robot_arm_document_path)):
                with open(os.path.expanduser(robot_arm_document_path), "r",encoding='utf-8') as f:
                    robot_arm_document= "".join(f.readlines())

    # robto_arm_api_document = '../rag/operations_data.json'
    # if os.path.exists(os.path.expanduser(robto_arm_api_document)):
    #             with open(os.path.expanduser(robto_arm_api_document), "r",encoding='utf-8') as f:
    #                   api_document = "".join(f.readlines())
    api_document = "结合RAG结果和过去的记忆，请进行任务规划，并生成对应的动作。对应api在rag结果里"

    SYSTEM_PROMOPT=f"""
    你是一个智能的机械臂，同时你是一个任务规划大师，对输入的指令可以进行理解和任务分解，机械臂内置了一些函数和相关的API文档，请你根据我的指令，特别参考API文档，生成对应的动作的函数并输出(动作可能是由多个函数组合而来),注意当涉及到拿起某个物体，抓起某个物体的时候，直接调用vlm_move函数。
    【重要】如果用户的指令是闲聊、提问（例如"你是谁"、"你能做什么"， "你觉得人工智能怎么样"）、打招呼或任何不需要机械臂执行具体物理动作的请求，请将 "function" 字段设置为空列表 `[]`，然后按照自己知道的结果回复。
    【输出json格式】
    你直接输出json本身内容即可,不需要```json的开头或结尾
    在"function"键中，输出函数名列表，列表中每个元素都是字符串，代表要运行的函数名称和参数。每个函数既可以单独运行，也可以和其他函数先后运行。列表元素的先后顺序，表示执行函数的先后顺序。如果不需要执行任何动作，则输出空列表 `[]`。
    在"response"键中，根据我的指令和你编排的动作（或不执行动作），以第一人称输出你回复我的话，不要超过100个字，可以幽默和发散，用上歌词、台词、互联网热梗、名场面。response回复内容要灵活一点，拟人化一点
    【以下是一些具体的例子】
    An example output would be:
        {{
            "function": ["move_single_servo(1,60,500)","move_single_servo(2,50,500)"],
            "response": "收到你的请求啦，我开始执行动作。" 
        }},
        {{
            "function": ["rgb_control(255,0,0)","arm_dance()"],
            "response": "好的，我开始执行 arm_rgb_control 动作。" 
        }},
        {{
            "function": ["move_single_servo(2,90,500)"，],
            "response": "okok，我就要执行 move_single_servo 动作。" 
        }},
        {{
            "function": ["move_all_servo([0, 90, 90, 45, 32, 0],op_time)"],
            "response": "好的，执行 move_all_servo 动作。" 
        }},
        {{ // 这是一个闲聊的例子
            "function": [],
            "response": "你好！很高兴和你聊天。"
        }},
        {{ // 这是回答问题的例子
             "function": [],
             "response": "我是一个能帮你干活的机械臂！"
        }}

    Note: The list of operations can be 1 ore many. And the servos are with ids from 1 to 6.
    ---
    API Document:
    ---
    {api_document}
    ---
    robot_arm document:
    ___
    {robot_arm_document}
    ---
    """  
    
    return SYSTEM_PROMOPT
      
def generate_operations_sequence(command_str):
    client = OpenAI(
        # openai系列的sdk，包括langchain，都需要这个/v1的后缀
        base_url='https://api.openai-proxy.org/v1',
        api_key='sk-Cinx17W4V8Ss4B7HSfxUrf2kikhbvZE7EGHy5SYwWJBWs6Qm',
    )
    # command = get_received_command()
    SYSTEM_PROMOPT= generate_prompt(command_str)
    USER_PROMPT = f"根据用户输入内容，来进行回答和操作：{command_str}"
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMOPT,
            },
            {
                "role": "user",
                "content": USER_PROMPT,
            }
        ],
        model="gpt-4o",
    )
    response_content = chat_completion.choices[0].message.content.strip()
    
    print("执行动作\n")
    print(response_content)
    
    # 在后台执行命令发送，不等待其完成
    threading.Thread(
        target=send_commands_to_service,
        args=(response_content, "http://192.168.43.144:5688/robot_command"),
        daemon=True
    ).start()

    return response_content

def get_response(command_str,use_rag):
      # 如果启动rag，则调用rag的接口
      global response
      if use_rag:
         retrieved_context = get_rag_result(command_str)
         prompt = f"参考以下RAG查询出的api操作知识和过去的对话记忆：{retrieved_context}\n用户指令：{command_str}\n请生成操作序列。"
         print(f"rag后的prompt为：{prompt}")
         response = generate_operations_sequence(prompt)
         response = json.loads(response)
      
      else :
        print("未启动rag，使用默认的指令生成器")
        response = generate_operations_sequence(command_str)
        response = json.loads(response)
      
      return response['response']

if __name__ == '__main__':
    # generate_operations_sequence("旋转180度")
    res = get_response("你面前有什么东西",True)
    print(res)