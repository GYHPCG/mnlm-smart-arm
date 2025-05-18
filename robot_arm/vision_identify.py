from top_view_shot import *
from grab_block import start_to_end,vlm_move_ready
from arm_voice_broadcast import speech
from utils_vlm import *

def vision_identify(PROMPT="图像中有什么东西"):
    ## 第一步：拍摄俯视图
    print('第1步：拍摄俯视图')
    vlm_move_ready()
    print(top_view_shot.__module__)  # 输出函数所在的模块路径
    top_view_shot(check=True)

    print('第2步：将图片输入给多模态视觉大模型')
    img_path = '../image/top_view_now11.jpg'

    n = 1
    while n < 5:
        try:
            print('    尝试第 {} 次访问多模态大模型'.format(n))
            # result = yi_vision_api(PROMPT, img_path='temp/vl_now.jpg')  # yi_vision定位能力出现波动，暂时换用QwenVL系列
            result = QwenVL_API(PROMPT, img_path=img_path)
            result = json.loads(result)
            print('    多模态大模型调用成功！')
            print(result)
            break
        except Exception as e:
            print('    多模态大模型返回数据结构错误，再尝试一次', e)
            n += 1

    speech(result)

if __name__ == '__main__':
    print("run identify")
    vision_identify("图像中有什么东西")

        