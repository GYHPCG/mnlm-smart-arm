# -*- coding: utf-8 -*-
import sys 
sys.path.append("..") 
from utils_vlm import *
from arm_zero import *
from top_view_shot import *
import time
import json
from grab_block import start_to_end,vlm_move_ready
from vision_grab import *
sys.path.append("/home/dofbot/code/mnlm-smart-arm/robot_arm/dofbot_ws/src/dofbot_color_identify/scripts")
from grab_target import *

def eye2hand(X_im=160, Y_im=120):
    '''
    输入目标点在图像中的像素坐标，转换为机械臂坐标
    '''

    # 整理两个标定点的坐标
    cali_1_im = [130, 290]                       # 左下角，第一个标定点的像素坐标，要手动填！
    cali_1_mc = [-21.8, -197.4]                  # 左下角，第一个标定点的机械臂坐标，要手动填！
    cali_2_im = [640, 0]                         # 右上角，第二个标定点的像素坐标
    cali_2_mc = [215, -59.1]                    # 右上角，第二个标定点的机械臂坐标，要手动填！
    
    X_cali_im = [cali_1_im[0], cali_2_im[0]]     # 像素坐标
    X_cali_mc = [cali_1_mc[0], cali_2_mc[0]]     # 机械臂坐标
    Y_cali_im = [cali_2_im[1], cali_1_im[1]]     # 像素坐标，先小后大
    Y_cali_mc = [cali_2_mc[1], cali_1_mc[1]]     # 机械臂坐标，先大后小

    # X差值
    X_mc = int(np.interp(X_im, X_cali_im, X_cali_mc))

    # Y差值
    Y_mc = int(np.interp(Y_im, Y_cali_im, Y_cali_mc))

    return X_mc, Y_mc
    
def vlm_move(PROMPT='帮我把绿色方块放在红色方块上', input_way='keyboard'):
    '''
    多模态大模型识别图像，吸泵吸取并移动物体
    input_way：speech语音输入，keyboard键盘输入
    '''

    print('多模态大模型识别图像，吸泵吸取并移动物体')
    
    # 机械臂归零
    print('机械臂归零')
    arm_zero()
    time.sleep(3)
    
    ## 第一步：完成手眼标定
    print('第一步：完成手眼标定')
    
    ## 第二步：发出指令
    # PROMPT_BACKUP = '帮我把绿色方块放在红色方块上' # 默认指令
    
    # if input_way == 'keyboard':
    #     PROMPT = input('第二步：输入指令')
    #     if PROMPT == '':
    #         PROMPT = PROMPT_BACKUP
    # elif input_way == 'speech':
    #     record() # 录音
    #     PROMPT = speech_recognition() # 语音识别
    print('第二步，给出的指令是：', PROMPT)
    
    ## 第三步：拍摄俯视图
    print('第三步：拍摄俯视图')
    vlm_move_ready()
    print(top_view_shot.__module__)  # 输出函数所在的模块路径
    top_view_shot(check=True)
    
    ## 第四步：将图片输入给多模态视觉大模型
    print('第四步：将图片输入给多模态视觉大模型')
    img_path = '../../image/top_view_now11.jpg'
    
    n = 1
    while n < 5:
        try:
            print('    尝试第 {} 次访问多模态大模型'.format(n))
            # result = yi_vision_api(PROMPT, img_path='temp/vl_now.jpg')  # yi_vision定位能力出现波动，暂时换用QwenVL系列
            result = gpt4o_API(PROMPT, img_path=img_path)
            result = json.loads(result)
            print('    多模态大模型调用成功！')
            print(result)
            break
        except Exception as e:
            print('    多模态大模型返回数据结构错误，再尝试一次', e)
            n += 1
    
    ## 第五步：视觉大模型输出结果后处理和可视化
    print('第五步：视觉大模型输出结果后处理和可视化')
    START_X_CENTER, START_Y_CENTER, END_X_CENTER, END_Y_CENTER = post_processing_viz(result, img_path, check=True)
     # 起点，左上角像素坐标
    START_X_MIN = int(result['start_xyxy'][0][0])
    START_Y_MIN = int(result['start_xyxy'][0][1])
    # 起点，右下角像素坐标
    START_X_MAX = int(result['start_xyxy'][1][0])
    START_Y_MAX = int(result['start_xyxy'][1][1])

    # 终点，左上角像素坐标
    END_X_MIN = int(result['end_xyxy'][0][0])
    END_Y_MIN = int(result['end_xyxy'][0][1])
    # 终点，右下角像素坐标
    END_X_MAX = int(result['end_xyxy'][1][0])
    END_Y_MAX = int(result['end_xyxy'][1][1])
    
    # ## 第六步：手眼标定转换为机械臂坐标
    # print('第六步：手眼标定，将像素坐标转换为机械臂坐标')
    # # 起点，机械臂坐标
    # START_X_MC, START_Y_MC = eye2hand(START_X_CENTER, START_Y_CENTER)
    # # 终点，机械臂坐标
    # END_X_MC, END_Y_MC = eye2hand(END_X_CENTER, END_Y_CENTER)
    
    # ## 第七步：吸泵吸取移动物体
    # print('第七步：吸泵吸取移动物体')
    # # pump_move(mc=mc, XY_START=[START_X_MC, START_Y_MC], XY_END=[END_X_MC, END_Y_MC])
    # start_to_end()
    ## 第八步：收尾
    # init_grab(START_X_CENTER,START_Y_CENTER)
    # init_grab(END_X_CENTER, END_Y_CENTER)
    target      = identify_GetTarget()
    start_targets = target.get_arm_coordinates(START_X_MIN,START_Y_MIN,START_X_MAX,START_Y_MAX)
    end_targets = target.get_arm_coordinates(END_X_MIN,END_Y_MIN,END_X_MAX,END_Y_MAX)

    starts = {"start": start_targets}
    ends = {"end": end_targets}

    if start_targets:
        # target_name, target_pos = list(targets.items())[0]  # 只取第一个找到的目标作为例子
        # target.target_run({target_name: target_pos})
        target.vlm_target_run(starts)
        
    if end_targets:
        # target_name, target_pos = list(targets.items())[0]  # 只取第一个找到的目标作为例子
        # target.target_run({target_name: target_pos})
        target.vlm_target_run(ends)
         
    print('第八步：任务完成')
    # GPIO.cleanup()            # 释放GPIO pin channel
    cv2.destroyAllWindows()   # 关闭所有opencv窗口
    # exit()
    
    
if __name__ == '__main__':
    vlm_move()
    
