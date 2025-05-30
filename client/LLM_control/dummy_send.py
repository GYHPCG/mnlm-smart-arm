'''
Author: '破竹' '2986779260@qq.com'
Date: 2025-03-31 18:00:16
LastEditors: '破竹' '2986779260@qq.com'
LastEditTime: 2025-03-31 20:21:25
FilePath: \code\mnlm-smart-arm\command_send.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import json
import os

import requests


def send_commands_to_service(user_input, service_url):
    # Load the JSON commands from the specified file
    with open(json_file_path, "r") as file:
        commands = json.load(file)
    print(f"Commands: {commands}")
    # commands = f"""
    # {{
    #     "operations": []
    # }}
    # """
    # Send the JSON commands to the HTTP service
    # 将字符串转为json
    # 检查 user_input 是否为空
   
    
    response = requests.post(service_url, json=commands)

    # Check the response status
    if response.status_code == 200:
        print("Commands sent successfully.")
        print("Response:", response)
    else:
        print("Failed to send commands.")
        print("Status Code:", response.status_code)
        print("Response:", response.text)


if __name__ == "__main__":
    json_file_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "D:\Desktop\毕设\code\mnlm-smart-arm\client\RAG\dummy_command.json"
    )
    service_url = "http://192.168.43.144:5688/robot_command"

    send_commands_to_service(json_file_path, service_url)
