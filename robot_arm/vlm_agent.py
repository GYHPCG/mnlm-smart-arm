# -*- coding: utf-8 -*-
'''
Author: '破竹' '2986779260@qq.com'
Date: 2025-05-08 18:11:00
LastEditors: '破竹' '2986779260@qq.com'
LastEditTime: 2025-05-10 22:21:46
FilePath: \code\mnlm-smart-arm\robot_arm\vlm_agent.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''


from utils_vlm import *
from arm_zero import *
from top_view_shot import *
import time
import json
from grab_block import start_to_end,vlm_move_ready
from vision_grab import *
import sys
sys.path.append("/home/dofbot/code/mnlm-smart-arm/robot_arm/dofbot_ws/src/dofbot_color_identify/scripts")
from grab_target import *

def vlm_move(PROMPT='帮我把绿色方块放在红色方块上', input_way='keyboard'):
    '''
    多模态大模型识别图像，吸泵吸取并移动物体
    input_way：speech语音输入，keyboard键盘输入
    '''

    print('多模态大模型识别图像，吸泵吸取并移动物体')
    
    # 机械臂归零
    # print('机械臂归零')
    # arm_zero()
    
    print('第二步，给出的指令是：', PROMPT)
    
    ## 第三步：拍摄俯视图
    print('第三步：拍摄俯视图')
    vlm_move_ready()
    # print(top_view_shot.__module__)  # 输出函数所在的模块路径
    top_view_shot(check=True)
    
    ## 第四步：将图片输入给多模态视觉大模型
    print('第四步：将图片输入给多模态视觉大模型')
    img_path = '../image/top_view_now11.jpg'
    
    n = 1
    while n < 5:
        try:
            print('    尝试第 {} 次访问多模态大模型'.format(n))
            result = QwenVL_API(PROMPT, img_path=img_path)
            result = json.loads(result)
            print('    多模态大模型调用成功！')
            print(result)
            break
        except Exception as e:
            print('    多模态大模型返回数据结构错误，再尝试一次', e)
            n += 1
    
    ## 第五步：视觉大模型输出结果后处理和可视化
    print('第五步：视觉大模型输出结果后处理和可视化')
    # START_X_CENTER, START_Y_CENTER, END_X_CENTER, END_Y_CENTER = post_processing_viz(result, img_path, check=True)
    
    if "end" in result:
        transfer_object_to_target(result,img_path)
    else:
        grasp_object(result,img_path)
    
    print('第八步：任务完成')
    cv2.destroyAllWindows()   # 关闭所有opencv窗口
    # exit()

def tradition_grasp_object(PROMPT='帮我拿起蓝色方块', input_way='keyboard'):
    '''
    多模态大模型识别图像，吸泵吸取并移动物体
    input_way：speech语音输入，keyboard键盘输入
    '''

    print('多模态大模型识别图像，吸泵吸取并移动物体')
    
    print('第二步，给出的指令是：', PROMPT)
    
    ## 第三步：拍摄俯视图
    print('第三步：拍摄俯视图')
    vlm_move_ready()
    print(top_view_shot.__module__)  # 输出函数所在的模块路径
    top_view_shot(check=True)
    
    ## 第四步：将图片输入给多模态视觉大模型
    print('第四步：将图片输入给多模态视觉大模型')
    img_path = '../image/top_view_now11.jpg'
    cv_grasp_object(PROMPT,img_path)
     
    
if __name__ == '__main__':
    # vlm_move()
    tradition_grasp_object()   
