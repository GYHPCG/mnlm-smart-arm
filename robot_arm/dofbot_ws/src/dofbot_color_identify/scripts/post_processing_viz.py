import time
import cv2
import numpy as np
from PIL import Image
from PIL import ImageFont, ImageDraw
# 导入中文字体，指定字号
font = ImageFont.truetype('/home/dofbot/code/mnlm-smart-arm/robot_arm/asset/SimHei.ttf', 26)

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
    # END_NAME = result['end']
    # 起点，左上角像素坐标
    START_X_MIN = int(result['start_xyxy'][0][0])
    START_Y_MIN = int(result['start_xyxy'][0][1])
    # 起点，右下角像素坐标
    START_X_MAX = int(result['start_xyxy'][1][0])
    START_Y_MAX = int(result['start_xyxy'][1][1])
    # 起点，中心点像素坐标
    START_X_CENTER = int((START_X_MIN + START_X_MAX) / 2)
    START_Y_CENTER = int((START_Y_MIN + START_Y_MAX) / 2)
    # # 终点，左上角像素坐标
    # END_X_MIN = int(result['end_xyxy'][0][0])
    # END_Y_MIN = int(result['end_xyxy'][0][1])
    # # 终点，右下角像素坐标
    # END_X_MAX = int(result['end_xyxy'][1][0])
    # END_Y_MAX = int(result['end_xyxy'][1][1])
    # # 终点，中心点像素坐标
    # END_X_CENTER = int((END_X_MIN + END_X_MAX) / 2)
    # END_Y_CENTER = int((END_Y_MIN + END_Y_MAX) / 2)
    
    # 可视化
    # 画起点物体框
    img_bgr = cv2.rectangle(img_bgr, (START_X_MIN, START_Y_MIN), (START_X_MAX, START_Y_MAX), [0, 0, 255], thickness=3)
    # 画起点中心点
    img_bgr = cv2.circle(img_bgr, [START_X_CENTER, START_Y_CENTER], 6, [0, 0, 255], thickness=-1)
    # 画终点物体框
    # img_bgr = cv2.rectangle(img_bgr, (END_X_MIN, END_Y_MIN), (END_X_MAX, END_Y_MAX), [255, 0, 0], thickness=3)
    # # 画终点中心点
    # img_bgr = cv2.circle(img_bgr, [END_X_CENTER, END_Y_CENTER], 6, [255, 0, 0], thickness=-1)
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

def post_processing_viz_two(result, img_path, check=False):
    
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
