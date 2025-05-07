'''
Author: '破竹' '2986779260@qq.com'
Date: 2025-03-31 17:56:58
LastEditors: '破竹' '2986779260@qq.com'
LastEditTime: 2025-05-07 18:27:06
FilePath: \code\mnlm-smart-arm\robot_arm\command_receiver.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import rospy
from std_msgs.msg import String
from flask import Flask, request
import json
import threading
import assiant3
import time

app = Flask(__name__)
publisher = None
command_str = None  # 定义全局变量
@app.route("/robot_command", methods=["POST"])
def json_example():
    global command_str  # 声明使用全局变量
    if request.is_json:
        content = request.get_json()
        command_str = json.dumps(content, ensure_ascii=False)
        print("接受 JSON command: %s\n" % command_str)
        # rospy.loginfo("Received JSON command: %s" % command_str)
        # msg = String()
        # msg.data = command_str
        # publisher.publish(msg)
        return "JSON command received and published!", 200
    else:
        return "Request was not JSON", 400

def flask_thread():
    app.run(host="0.0.0.0", port=5688)


if __name__ == "__main__":
    # rospy.init_node("command_receiver_node", anonymous=True)
    # publisher = rospy.Publisher("json_command_topic", String, queue_size=10)

    # # Run Flask in a separate thread
    threading.Thread(target=flask_thread, daemon=True).start()

   
    # 主线程中处理命令
    while True:
        if command_str is not None and command_str != "":  # 检查是否有新的命令
            print("Processing command in assiant:", command_str)
            assiant3.assiant(command_str)  # 将命令传递给 assiant
            command_str = None  # 重置命令，等待下一条命令
        time.sleep(5)  # 避免占用过多 CPU