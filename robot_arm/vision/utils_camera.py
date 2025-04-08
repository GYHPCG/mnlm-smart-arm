'''
Author: '破竹' '2986779260@qq.com'
Date: 2025-04-07 22:41:03
LastEditors: '破竹' '2986779260@qq.com'
LastEditTime: 2025-04-07 22:43:31
FilePath: \code\mnlm-smart-arm\robot_arm\vision\demo_capture.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import cv2

def bgr8_to_jpeg(value, quality=75):
    return bytes(cv2.imencode('.jpg', value)[1])

def get_camera():
    print("正在获取摄像头数据...")
    image = cv2.VideoCapture(0)  # 打开摄像头
    if not image.isOpened():
        print("Error: Could not open camera.")
        exit()

    while True:
        ret, frame = image.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        cv2.imshow("Camera", frame)  # 使用 OpenCV 显示图像

        if cv2.waitKey(1) & 0xFF == ord('q'):  # 按 'q' 键退出
            break

    image.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    get_camera()
