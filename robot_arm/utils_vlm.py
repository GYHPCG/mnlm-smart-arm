# -*- coding: utf-8 -*-
print('导入视觉大模型模块')
import time
import cv2
import numpy as np
from PIL import Image
from PIL import ImageFont, ImageDraw
# 导入中文字体，指定字号
font = ImageFont.truetype('asset/SimHei.ttf', 26)


# 系统提示词
SYSTEM_PROMPT = '''
你是一个智能机械臂，同时也是一个视觉定位大师，能够从640x480的照片片中准确获取出对应物体的左上角坐标和右下角坐标。现在用户对你进行提问：
比如：
1. 人们问你面前有什么，你需要识别出图片里的东西。并返回识别结果放在json中，不要回复其它内容,如```json开头和结尾。
如，图片中有什么东西？你的输出格式是：response给出你的反应(灵活一些)，然后thing_name里列出看到的物品
{
    "response":"好的，再在图片中我看到了一些东西"
    "thing_name": ["红色方块", "绿色方块", "房子简笔画"]
}
---
2. 人们让你抓起某个物体或者让你移动到指定位置。你需要提取出该物体的位置，坐标从左上角(0,0)开始，右下角结束，向右为x轴，向下为y轴，并从这张图中分别找到这个物体左上角和右下角的像素坐标，输出json数据结构。例如，如果我的指令是：帮我抓起红色方块。你输出这个的格式：
{
 "response": "好的，我尝试帮你拿起红色方块",
 "start":"红色方块",
 "start_xyxy":[[102,505],[324,860]],
}

只回复json本身即可，不要回复其它内容,如```json的开头或结尾。
---
3. 人们让你把红色方块放在蓝色方块上。你需要从这句话中提取出起始物体和终止物体，坐标从左上角(0,0)开始，右下角结束，向右为x轴，向下为y轴，并从这张图中分别找到这两个物体左上角和右下角的像素坐标，输出json数据结构。
例如，如果我的指令是：请帮我把红色方块放在蓝色方块上。
你输出这样的格式：
{
 "thing_name": ["红色方块", "绿色方块", "房子简笔画"],
 "start":"红色方块",
 "start_xyxy":[[102,505],[324,860]],
 "end":"蓝色方块",
 "end_xyxy":[[300,150],[476,310]]
}

只回复json本身即可，不要回复其它内容,如```json的开头或结尾。

我现在的指令是：
'''

# gpt4o调用函数
import openai
from openai import OpenAI
import base64
import json
from grab_block import start_to_end,vlm_move_ready
from top_view_shot import *
import sys
sys.path.append("/home/dofbot/code/mnlm-smart-arm/robot_arm/dofbot_ws/src/dofbot_color_identify/scripts")
from grab_target import *

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
def gpt4o_API(PROMPT='手上拿的东西放到旁边', img_path='../image/top_view_now11.jpg'):
    '''
    gpt4o大模型API
    '''
    
    client = OpenAI(
        # openai系列的sdk，包括langchain，都需要这个/v1的后缀
        base_url='https://api.openai-proxy.org/v1',
        api_key='sk-Cinx17W4V8Ss4B7HSfxUrf2kikhbvZE7EGHy5SYwWJBWs6Qm',
    )
    # 编码为base64数据
    base64_image = encode_image(img_path)
    
    chat_completion = client.chat.completions.create(
        # model="gpt-4o-2024-11-20",
        model = "o4-mini-2025-04-16",
        messages=[
            {
                "role": "user",
                "content": [
                    { "type": "text", "text": f"{SYSTEM_PROMPT + PROMPT}" },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    },
                ],
            }
        ],
    ) 
     
    # print(chat_completion)
    response_content = chat_completion.choices[0].message.content.strip()
    print("vlm 多模态模型调用成功")
    print(response_content)

    return response_content



get_xy_prompt = '''
    你正在使用一个视觉大模型，请从图片中提取出指定物体的坐标，图片大小为640x480, 坐标从左上角(0,0)开始，右下角结束，向右为x轴，向下为y轴，并返回json数据结构。
    例如，如果图片中只有两个物体，一个红色方块，蓝色方块。我的指令是：获取红色方块的坐标。你需要返回这样的格式：
    {
    "response": "好的，我尝试帮你获取红色方块的位置",
    "start":"红色方块",
    "start_xyxy":[[102,505],[324,860]],
    }
    只回复json本身即可，不要回复其它内容,如```json的开头或结尾。

    我现在的指令是：
    '''

cv_get_xy_prompt = ''''
 你正在使用一个视觉大模型,我现在有个函数可以获取物体的位置。cv_get_xy(img_path,color_list)。其中color_list的内容可为{"0"："none","1"："red","2": "green","3"："blue","4"："yellow"}。
 例子：1. 帮我抓住红色方块，则color_list = {"1":"red"}
       2. 帮我拿起蓝色方块，则color_list = {"2": 'blue'}

       现在我的指令是，帮我拿起红色方块。你需要返回这样的格式：
       {
          "response": "好的，我尝试帮你获取红色方块的位置",
           "color_list": {"1": "red"}
       }
       只回复json本身即可，不要回复其它内容,如```json的开头或结尾。
       我现在的指令是:
       
'''

def cv_gpt_get_xy(PROMPT='抓到到红色方块位置', img_path='../image/top_view_now11.jpg'):
    '''
    gpt4o大模型API
    '''
    
    client = OpenAI(
        # openai系列的sdk，包括langchain，都需要这个/v1的后缀
        base_url='https://api.openai-proxy.org/v1',
        api_key='sk-Cinx17W4V8Ss4B7HSfxUrf2kikhbvZE7EGHy5SYwWJBWs6Qm',
    )
    # 编码为base64数据
    base64_image = encode_image(img_path)
    
    chat_completion = client.chat.completions.create(
        model="gpt-4o-2024-11-20",
        messages=[
            {
                "role": "user",
                "content":f"{cv_get_xy_prompt} + {PROMPT}"
            }
        ],
    ) 
     
    # print(chat_completion)
    response_content = chat_completion.choices[0].message.content.strip()
    # xy = json_data['position']
    print("获取x,y坐标成功")
    print(response_content)
    return response_content

def cv_get_result(PROMPT='移动到黄色方块位置',img_path='../image/top_view_now11.jpg'):
    res = cv_gpt_get_xy(PROMPT,img_path)
    res = json.loads(res)
    color_list = res.get("color_list", {})
    print(color_list)
    return color_list

def cv_grasp_object(PROMPT='移动到黄色方块位置',img_path='../image/top_view_now11.jpg'):
    color_list = cv_get_result(PROMPT,img_path)
    cv_get_xy(img_path,color_list)
    
    
    
def get_xy(PROMPT='移动到红色方块位置', img_path='../image/top_view_now11.jpg'):
    '''
    gpt4o大模型API
    '''
    
    client = OpenAI(
        # openai系列的sdk，包括langchain，都需要这个/v1的后缀
        base_url='https://api.openai-proxy.org/v1',
        api_key='sk-Cinx17W4V8Ss4B7HSfxUrf2kikhbvZE7EGHy5SYwWJBWs6Qm',
    )
    # 编码为base64数据
    base64_image = encode_image(img_path)
    
    chat_completion = client.chat.completions.create(
        model="gpt-4o-2024-11-20",
        messages=[
            {
                "role": "user",
                "content": [
                    { "type": "text", "text": f"{get_xy_prompt + PROMPT}" },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    },
                ],
            }
        ],
    ) 
     
    # print(chat_completion)
    response_content = chat_completion.choices[0].message.content.strip()
    # xy = json_data['position']
    print("获取x,y坐标成功")
    print(response_content)
    return response_content

def move_to(PROMPT='移动到红色方块位置', input_way='keyboard'):
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
    
    n = 1
    while n < 5:
        try:
            print('    尝试第 {} 次访问多模态大模型'.format(n))
            # result = yi_vision_api(PROMPT, img_path='temp/vl_now.jpg')  # yi_vision定位能力出现波动，暂时换用QwenVL系列
            result = get_xy(PROMPT, img_path=img_path)
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
    move_to_other(result,img_path)
    
    print('第八步：任务完成')
    cv2.destroyAllWindows()   # 关闭所有opencv窗口

def post_processing_viz_one(result, img_path, check=False):
    
    '''
    视觉大模型输出结果后处理和可视化
    check：是否需要人工看屏幕确认可视化成功，按键继续或退出
    '''

    # 后处理
    img_bgr = cv2.imread(img_path)
    img_h = img_bgr.shape[0]
    img_w = img_bgr.shape[1]

    # 输出长和宽
    print('    图片长宽：', img_w, img_h)
    # 缩放因子
    FACTOR = 999
    # 起点物体名称
    START_NAME = result['start']
    # 终点物体名称
    END_NAME = result['end']
    # 起点，左上角像素坐标
    START_X_MIN = int(result['start_xyxy'][0][0])
    START_Y_MIN = int(result['start_xyxy'][0][1])
    # 起点，右下角像素坐标
    START_X_MAX = int(result['start_xyxy'][1][0])
    START_Y_MAX = int(result['start_xyxy'][1][1])
    # 起点，中心点像素坐标
    START_X_CENTER = int((START_X_MIN + START_X_MAX) / 2)
    START_Y_CENTER = int((START_Y_MIN + START_Y_MAX) / 2)
    
    # 可视化
    # 画起点物体框
    img_bgr = cv2.rectangle(img_bgr, (START_X_MIN, START_Y_MIN), (START_X_MAX, START_Y_MAX), [0, 0, 255], thickness=3)
    # 画起点中心点
    img_bgr = cv2.circle(img_bgr, [START_X_CENTER, START_Y_CENTER], 6, [0, 0, 255], thickness=-1)
    # 写中文物体名称
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB) # BGR 转 RGB
    img_pil = Image.fromarray(img_rgb) # array 转 pil
    draw = ImageDraw.Draw(img_pil)
    # 写起点物体中文名称
    draw.text((START_X_MIN, START_Y_MIN-32), START_NAME, font=font, fill=(255, 0, 0, 1)) # 文字坐标，中文字符串，字体，rgba颜色
    # 写终点物体中文名称
    # draw.text((END_X_MIN, END_Y_MIN-32), END_NAME, font=font, fill=(0, 0, 255, 1)) # 文字坐标，中文字符串，字体，rgba颜色
    img_bgr = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR) # RGB转BGR
    # 保存可视化效果图
    cv2.imwrite('../image/vl_now_viz.jpg', img_bgr)

    # formatted_time = time.strftime("%Y%m%d%H%M", time.localtime())
    # cv2.imwrite('visualizations/{}.jpg'.format(formatted_time), img_bgr)

    # # 在屏幕上展示可视化效果图
    # cv2.imshow('success_vlm', img_bgr) 

    # if check:
    #     print('    请确认可视化成功，按c键继续，按q键退出')
    #     while(True):
    #         key = cv2.waitKey(10) & 0xFF
    #         if key == ord('c'): # 按c键继续
    #             break
    #         if key == ord('q'): # 按q键退出
    #             # exit()
    #             cv2.destroyAllWindows()   # 关闭所有opencv窗口
    #             raise NameError('按q退出')
    # else:
    #     if cv2.waitKey(1) & 0xFF == None:
    #         pass
    time.sleep(5)
    return START_X_CENTER, START_Y_CENTER



def post_processing_viz(result, img_path, check=False):
    
    '''
    视觉大模型输出结果后处理和可视化
    check：是否需要人工看屏幕确认可视化成功，按键继续或退出
    '''

    # 后处理
    img_bgr = cv2.imread(img_path)
    img_h = img_bgr.shape[0]
    img_w = img_bgr.shape[1]

    # 输出长和宽
    print('    图片长宽：', img_w, img_h)
    # 缩放因子
    FACTOR = 999
    # 起点物体名称
    START_NAME = result['start']
    # 终点物体名称
    END_NAME = result['end']
    # 起点，左上角像素坐标
    START_X_MIN = int(result['start_xyxy'][0][0])
    START_Y_MIN = int(result['start_xyxy'][0][1])
    # 起点，右下角像素坐标
    START_X_MAX = int(result['start_xyxy'][1][0])
    START_Y_MAX = int(result['start_xyxy'][1][1])
    # 起点，中心点像素坐标
    START_X_CENTER = int((START_X_MIN + START_X_MAX) / 2)
    START_Y_CENTER = int((START_Y_MIN + START_Y_MAX) / 2)
    # 终点，左上角像素坐标
    END_X_MIN = int(result['end_xyxy'][0][0])
    END_Y_MIN = int(result['end_xyxy'][0][1])
    # 终点，右下角像素坐标
    END_X_MAX = int(result['end_xyxy'][1][0])
    END_Y_MAX = int(result['end_xyxy'][1][1])
    # 终点，中心点像素坐标
    END_X_CENTER = int((END_X_MIN + END_X_MAX) / 2)
    END_Y_CENTER = int((END_Y_MIN + END_Y_MAX) / 2)
    
    # 可视化
    # 画起点物体框
    img_bgr = cv2.rectangle(img_bgr, (START_X_MIN, START_Y_MIN), (START_X_MAX, START_Y_MAX), [0, 0, 255], thickness=3)
    # 画起点中心点
    img_bgr = cv2.circle(img_bgr, [START_X_CENTER, START_Y_CENTER], 6, [0, 0, 255], thickness=-1)
    # 画终点物体框
    img_bgr = cv2.rectangle(img_bgr, (END_X_MIN, END_Y_MIN), (END_X_MAX, END_Y_MAX), [255, 0, 0], thickness=3)
    # 画终点中心点
    img_bgr = cv2.circle(img_bgr, [END_X_CENTER, END_Y_CENTER], 6, [255, 0, 0], thickness=-1)
    # 写中文物体名称
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB) # BGR 转 RGB
    img_pil = Image.fromarray(img_rgb) # array 转 pil
    draw = ImageDraw.Draw(img_pil)
    # 写起点物体中文名称
    draw.text((START_X_MIN, START_Y_MIN-32), START_NAME, font=font, fill=(255, 0, 0, 1)) # 文字坐标，中文字符串，字体，rgba颜色
    # 写终点物体中文名称
    draw.text((END_X_MIN, END_Y_MIN-32), END_NAME, font=font, fill=(0, 0, 255, 1)) # 文字坐标，中文字符串，字体，rgba颜色
    img_bgr = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR) # RGB转BGR
    # 保存可视化效果图
    cv2.imwrite('../image/vl_now_viz.jpg', img_bgr)

    # formatted_time = time.strftime("%Y%m%d%H%M", time.localtime())
    # cv2.imwrite('visualizations/{}.jpg'.format(formatted_time), img_bgr)

    # # 在屏幕上展示可视化效果图
    # cv2.imshow('success_vlm', img_bgr) 

    # if check:
    #     print('    请确认可视化成功，按c键继续，按q键退出')
    #     while(True):
    #         key = cv2.waitKey(10) & 0xFF
    #         if key == ord('c'): # 按c键继续
    #             break
    #         if key == ord('q'): # 按q键退出
    #             # exit()
    #             cv2.destroyAllWindows()   # 关闭所有opencv窗口
    #             raise NameError('按q退出')
    # else:
    #     if cv2.waitKey(1) & 0xFF == None:
    #         pass
    time.sleep(5)
    return START_X_CENTER, START_Y_CENTER, END_X_CENTER, END_Y_CENTER

if __name__ == '__main__':
    # 测试
    # result = gpt4o_API(PROMPT='把绿色方块放到蓝色方块上面', img_path='../image/top_view_now11.jpg')
    # print(result)
    # result = json.loads(result)
    # print(result)
    # post_processing_viz(result, img_path='../image/top_view_now11.jpg', check=True)

    res = cv_get_result("获取黄色方块的位置",img_path='../image/top_view_now11.jpg')