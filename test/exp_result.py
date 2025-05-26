'''
Author: '破竹' '2986779260@qq.com'
Date: 2025-05-26 20:28:41
LastEditors: '破竹' '2986779260@qq.com'
LastEditTime: 2025-05-26 20:32:02
FilePath: \mnlm-smart-arm\test\exp_result.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import matplotlib.pyplot as plt
import matplotlib as mpl

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

categories = ['闲聊指令', '模糊指令', '单指令', '复杂指令']
accuracy = [100, 90, 90, 79]
samples = ['12/12', '9/10', '26/29', '26/33']

plt.figure(figsize=(8, 5))
bars = plt.bar(categories, accuracy, color=['#1f77b4', '#2ca02c', '#ff7f0e', '#d62728'])

# 添加数据标签
for bar, sample in zip(bars, samples):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height, 
             f'{height}%\n({sample})', ha='center', va='bottom', fontsize=9)

plt.ylim(70, 105)
plt.title('不同指令类型的正确率对比', fontsize=12)
plt.ylabel('正确率 (%)', fontsize=10)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# 设置x轴标签字体大小
plt.xticks(fontsize=10)

plt.show()