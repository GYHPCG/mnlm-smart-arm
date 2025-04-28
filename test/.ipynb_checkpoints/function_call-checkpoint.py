import os
import json
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
# 初始化 OpenAI 客户端（需要提前设置环境变量 OPENAI_API_KEY）
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ========== 预定义函数 ==========
def get_current_weather(location: str, unit: str = "celsius"):
    """模拟天气API（实际开发中替换为真实API调用）"""
    # 这里使用固定数据模拟，真实场景可调用如 OpenWeatherMap API
    weather_data = {
        "location": location,
        "temperature": "25",
        "unit": unit,
        "forecast": ["sunny", "windy"],
        "humidity": 65
    }
    return json.dumps(weather_data)

# ========== 函数调用处理器 ==========
def execute_function_call(function_name: str, arguments: dict):
    """根据函数名调用对应函数"""
    if function_name == "get_current_weather":
        return get_current_weather(
            location=arguments.get("location"),
            unit=arguments.get("unit", "celsius")  # 默认值处理
        )
    else:
        raise NotImplementedError(f"函数 {function_name} 未实现")

# ========== 主对话流程 ==========
def chat_with_function_calling():
    # 初始化对话历史
    messages = [{
        "role": "system",
        "content": "当需要实时天气信息时，请调用天气查询函数。用中文回复用户。"
    }]

    # 用户提问示例
    user_input = "上海现在多少度？湿度如何？"
    messages.append({"role": "user", "content": user_input})

    # 第一次请求：让模型决定是否调用函数
    first_response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
        functions=[{
            "name": "get_current_weather",
            "description": "获取指定地区的当前天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市或地区名称，例如：上海市、北京"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "温度单位"
                    }
                },
                "required": ["location"]
            }
        }],
        function_call="auto"
    )

    # 解析模型响应
    response_message = first_response.choices[0].message
    print("首次模型响应结构:", json.dumps(response_message.model_dump(), ensure_ascii=False))

    # 如果触发函数调用
    if response_message.function_call:
        # 提取调用信息
        func_name = response_message.function_call.name
        args = json.loads(response_message.function_call.arguments)

        # 执行函数调用
        print(f"\n触发函数调用: {func_name}({args})")
        try:
            function_response = execute_function_call(func_name, args)
        except Exception as e:
            function_response = json.dumps({"error": str(e)})

        # 将函数结果加入对话历史
        messages.append({
            "role": "function",
            "name": func_name,
            "content": function_response
        })

        # 第二次请求：生成最终回复
        print("\n使用函数结果生成最终回复...")
        second_response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages
        )
        final_answer = second_response.choices[0].message.content
        print("\n最终回复:", final_answer)
    else:
        print("未触发函数调用:", response_message.content)

# ========== 执行示例 ==========
if __name__ == "__main__":
    chat_with_function_calling()