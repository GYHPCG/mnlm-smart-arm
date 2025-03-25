
from openai import OpenAI

if __name__ == '__main__':
    client = OpenAI(
        # openai系列的sdk，包括langchain，都需要这个/v1的后缀
        base_url='https://api.openai-proxy.org/v1',
        api_key='sk-Cinx17W4V8Ss4B7HSfxUrf2kikhbvZE7EGHy5SYwWJBWs6Qm',
    )

    chat_completion = client.chat.completions.create(
        # name="Voice Robot Controller",
        # instructions="""
        #     You have a brain and a robot arm, and you receive voice command from the human being, and respond accordingly.
        # """,
        messages=[
            {
                "role": "system",
                "content": "You have a brain and a robot arm, and you receive text command from the human being, and respond accordingly.",
            }
        ],
        # tools=tool_signatures,
        model="gpt-3.5-turbo-1106",
    ) # 如果是其他兼容模型，比如deepseek，直接这里改模型名即可，其他都不用动

    print(chat_completion)