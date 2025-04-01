'''
Author: '破竹' '2986779260@qq.com'
Date: 2025-04-01 14:33:25
LastEditors: '破竹' '2986779260@qq.com'
LastEditTime: 2025-04-01 14:36:00
FilePath: \code\mnlm-smart-arm\robot_arm\listener.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import rospy
from std_msgs.msg import String
import json

# 全局变量，用于存储接收到的 JSON 数据
received_command = None

def callback(data):
    """
    Callback function to process received JSON data.
    """
    global received_command
    try:
        # 将接收到的字符串解析为 JSON
        command = json.loads(data.data)
        print("Received JSON command:", command)
        # 将 JSON 数据转换为字符串并存储到全局变量
        received_command = json.dumps(command)
    except json.JSONDecodeError as e:
        rospy.logerr(f"Failed to decode JSON: {e}")

def get_received_command():
    """
    Returns the last received JSON command as a string.
    If no command has been received, it waits until a command is available.
    """
    global received_command
    # 等待直到接收到数据
    rate = rospy.Rate(10)  # 10 Hz
    while received_command is None and not rospy.is_shutdown():
        rospy.loginfo("Waiting for JSON command...")
        rate.sleep()
    return received_command

def listener():
    """
    Subscribes to the 'json_command_topic' to receive JSON commands.
    """
    rospy.init_node("command_listener_node", anonymous=True)
    rospy.Subscriber("json_command_topic", String, callback)
    rospy.loginfo("Listening for JSON commands on 'json_command_topic'...")
    rospy.spin()

if __name__ == "__main__":
    listener()