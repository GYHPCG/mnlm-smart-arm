
from openai import OpenAI
from arm_dance import arm_dance
from arm_clamp_block import arm_clamp_block
from arm_move import arm_move

SYSTEM_PROMOPT='''
你是我的机械臂助手，机械臂内置了一些函数，请你根据我的指令来调用这些函数。
【以下是所有内置函数介绍】
定义夹积木块函数,arm_clamp_block(enable)，enable=1：夹住，=0：松开
定义移动机械臂函数,同时控制1-5号舵机运动,arm_move(p, s_time = 500)，p=[S1,S2,S3,S4,S5],其中S1-S5分别是舵机1-5的角度，s_time是舵机运动时间，单位ms
定义机械臂跳舞函数，arm_dance()，让机械臂跳舞
定义机械臂归零函数，arm_zero()，让机械臂回到原点
你现在的任务是：
'''

if __name__ == '__main__':
    client = OpenAI(
        # openai系列的sdk，包括langchain，都需要这个/v1的后缀
        base_url='https://api.openai-proxy.org/v1',
        api_key='sk-Cinx17W4V8Ss4B7HSfxUrf2kikhbvZE7EGHy5SYwWJBWs6Qm',
    )
    PROMOPT="跳舞,夹积木块"
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
    #response_content = chat_completion.choices[0].message.content.strip()
    
    # print(response_content)