# mnlm-smart-arm
code of LLM + arm

# 使用说明
项目目前有3个分支，分别为main branch, v2 branch, v3 branch。
其中main branch部分添加功能还在测试，不稳定。
v2 branch具备基本功能，可以运行，可以正常使用。
v3 branch是v2 branch的升级版本，目前功能已经稳定，可以正常使用。
在使用v3 branch时候，你需要将.env.template文件重命名为.env，并填写你的OpenAI API Key,closeai API Key,QwenVla API Key。其中openai API Key和closeai API Key是可选的，如果你不需要视觉抓取功能的话。

运行本项目，你需要进入client目录下的LLM_controller目录下，然后运行main.py
然后你需要在你的机械臂端，即robot_arm文件下运行main.py,同理如果你需要机械臂视觉抓取共功能，你还需进入dofbot_ws/src下启动ROS服务端。启动命令如下：
```shell
cd ~/dofbot_ws/  # 进入工作空间
catkin_make   # 编译
source devel/setup.bash  # 更新系统环境
roslaunch dofbot_info dofbot_server.launch  # 启动服务端节点
```

