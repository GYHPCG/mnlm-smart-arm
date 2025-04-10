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
你是一个智能机器人，拥有一个大脑和一个机械臂，人们可以向你发出命令，询问问题。
比如：1. 人们问你面前有什么，你需要识别出图片里的东西。并返回识别结果放在json中，不要回复其它内容。
     2. 人们让你把红色方块放在房子简笔画上。你需要从这句话中提取出起始物体和终止物体，并从这张图中分别找到这两个物体左上角和右下角的像素坐标，输出json数据结构。
例如，如果我的指令是：请帮我把红色方块放在房子简笔画上。
你输出这样的格式：
{
 "start":"红色方块",
 "start_xyxy":[[102,505],[324,860]],
 "end":"房子简笔画",
 "end_xyxy":[[300,150],[476,310]]
}

只回复json本身即可，不要回复其它内容

我现在的指令是：
'''

# gpt4o调用函数
import openai
from openai import OpenAI
import base64

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
def gpt4o_API(PROMPT='手上拿的东西放到旁边', img_path='../../image/top_viw_now.jpg'):
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
     
    print(chat_completion)
    response_content = chat_completion.choices[0].message.content.strip()
    print("多模态模型调用成功")

    return response_content


def post_processing_viz(result, img_path, check=False):
    
    '''
    视觉大模型输出结果后处理和可视化
    check：是否需要人工看屏幕确认可视化成功，按键继续或退出
    '''

    # 后处理
    img_bgr = cv2.imread(img_path)
    img_h = img_bgr.shape[0]
    img_w = img_bgr.shape[1]
    # 缩放因子
    FACTOR = 999
    # 起点物体名称
    START_NAME = result['start']
    # 终点物体名称
    END_NAME = result['end']
    # 起点，左上角像素坐标
    START_X_MIN = int(result['start_xyxy'][0][0] * img_w / FACTOR)
    START_Y_MIN = int(result['start_xyxy'][0][1] * img_h / FACTOR)
    # 起点，右下角像素坐标
    START_X_MAX = int(result['start_xyxy'][1][0] * img_w / FACTOR)
    START_Y_MAX = int(result['start_xyxy'][1][1] * img_h / FACTOR)
    # 起点，中心点像素坐标
    START_X_CENTER = int((START_X_MIN + START_X_MAX) / 2)
    START_Y_CENTER = int((START_Y_MIN + START_Y_MAX) / 2)
    # 终点，左上角像素坐标
    END_X_MIN = int(result['end_xyxy'][0][0] * img_w / FACTOR)
    END_Y_MIN = int(result['end_xyxy'][0][1] * img_h / FACTOR)
    # 终点，右下角像素坐标
    END_X_MAX = int(result['end_xyxy'][1][0] * img_w / FACTOR)
    END_Y_MAX = int(result['end_xyxy'][1][1] * img_h / FACTOR)
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
    cv2.imwrite('temp/vl_now_viz.jpg', img_bgr)

    formatted_time = time.strftime("%Y%m%d%H%M", time.localtime())
    cv2.imwrite('visualizations/{}.jpg'.format(formatted_time), img_bgr)

    # 在屏幕上展示可视化效果图
    cv2.imshow('zihao_vlm', img_bgr) 

    if check:
        print('    请确认可视化成功，按c键继续，按q键退出')
        while(True):
            key = cv2.waitKey(10) & 0xFF
            if key == ord('c'): # 按c键继续
                break
            if key == ord('q'): # 按q键退出
                # exit()
                cv2.destroyAllWindows()   # 关闭所有opencv窗口
                raise NameError('按q退出')
    else:
        if cv2.waitKey(1) & 0xFF == None:
            pass

    return START_X_CENTER, START_Y_CENTER, END_X_CENTER, END_Y_CENTER

if __name__ == '__main__':
    # 测试
    result = gpt4o_API(PROMPT='手上拿的东西放到旁边', img_path='../../image/top_view_now.jpg')
    print(result)
    # result = json.loads(result)
    # print(result)
    # post_processing_viz(result, img_path='../../image/top_view_now.jpg', check=True)