'''
Author: '破竹' '2986779260@qq.com'
Date: 2025-03-31 17:56:58
LastEditors: '破竹' '2986779260@qq.com'
LastEditTime: 2025-04-01 15:14:53
FilePath: \code\mnlm-smart-arm\robot_arm\command_receiver.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import rospy
from std_msgs.msg import String
from flask import Flask, request
import json
import threading
import assiant

app = Flask(__name__)
publisher = None

@app.route("/robot_command", methods=["POST"])
def json_example():
    if request.is_json:
        content = request.get_json()
        command_str = json.dumps(content)
        print("接受 JSON command: %s\n" % command_str)
        rospy.loginfo("Received JSON command: %s" % command_str)
        msg = String()
        msg.data = command_str
        publisher.publish(msg)
        return "JSON command received and published!", 200
    else:
        return "Request was not JSON", 400

def flask_thread():
    app.run(host="0.0.0.0", port=5688)


if __name__ == "__main__":
    rospy.init_node("command_receiver_node", anonymous=True)
    publisher = rospy.Publisher("json_command_topic", String, queue_size=10)

    # Run Flask in a separate thread
    threading.Thread(target=flask_thread, daemon=True).start()

    rospy.spin()

    assiant.assiant()