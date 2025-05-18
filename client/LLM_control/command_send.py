'''
Author: '破竹' '2986779260@qq.com'
Date: 2025-03-31 18:00:16
LastEditors: '破竹' '2986779260@qq.com'
LastEditTime: 2025-05-07 18:50:32
FilePath: \code\mnlm-smart-arm\command_send.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import json
import time

import requests


def send_commands_to_service(user_input, service_url):
    """
    发送命令到服务端
    参数:
    user_input: 可以是字符串或JSON对象
    service_url: 服务端URL
    """
    # 检查输入是否为空
    if user_input is None:
        print("Error: user_input is empty or None. Skipping operation.")
        return

    try:
        # 判断输入类型并相应处理
        if isinstance(user_input, dict):
            # 如果已经是字典类型，直接使用
            print(f"Input is already a JSON object: {user_input}")
            json_com = user_input
        else:
            # 尝试解析字符串为JSON
            try:
                # 尝试将字符串解析为JSON
                json_com = json.loads(user_input)
                print(f"Successfully parsed string to JSON: {json_com}")
            except json.JSONDecodeError:
                # 如果解析失败，将整个字符串作为user_input的值
                json_com = {"user_input": user_input}
                print(f"Converted string to JSON: {json_com}")

        # 确保JSON使用UTF-8编码
        json_com = json.dumps(json_com, ensure_ascii=False)
        print(f"Final JSON to send: {json_com}")

        # 发送请求
        time.sleep(2)
        response = requests.post(service_url, json=json.loads(json_com))

        # 检查响应状态
        if response.status_code == 200:
            print("Commands sent successfully.")
            print("Response:", response)
        else:
            print("Failed to send commands.")
            print("Status Code:", response.status_code)
            print("Response:", response.text)

    except Exception as e:
        print(f"Error processing command: {e}")
        return


if __name__ == "__main__":
    # json_file_path = os.path.join(
    #     os.path.dirname(os.path.dirname(__file__)), "D:\Desktop\毕设\code\mnlm-smart-arm\client\RAG\dummy_command.json"
    # )
    service_url = "http://192.168.43.144:5688/robot_command"
    #生成一个简单json
    json_com = "跳舞"
    send_commands_to_service(json_com, service_url)
