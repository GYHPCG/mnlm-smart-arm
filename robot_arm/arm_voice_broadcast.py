#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import smbus
import time

# I2C 配置
I2C_BUS = 1
I2C_ADDR = 0x30
DATA_HEAD = 0xfd

# 初始化I2C总线
bus = smbus.SMBus(I2C_BUS)

# 编码格式枚举
EncodingFormat = {
    'GB2312': 0x00,
    'GBK': 0x01,
    'BIG5': 0x02,
    'UNICODE': 0x03
}

# 芯片状态枚举
ChipStatus = {
    'InitSuccessful': 0x4A,
    'CorrectCommand': 0x41,
    'ErrorCommand': 0x45,
    'Busy': 0x4E,
    'Idle': 0x4F
}

# 发音人枚举
ReaderType = {
    'XiaoYan': 3,
    'XuJiu': 51,
    'XuDuo': 52,
    'XiaoPing': 53,
    'DonaldDuck': 54,
    'XuXiaoBao': 55
}

def i2c_write(data):
    """通过I2C总线写入数据"""
    for byte in data:
        try:
            bus.write_byte(I2C_ADDR, byte)
            time.sleep(0.01)
        except Exception as e:
            print(f"I2C写入错误: {str(e)}")

def compose_speech_packet(text, encoding=0x00):
    """组合语音合成数据包"""
    text_bytes = text.encode('gb2312')
    packet = [
        DATA_HEAD,
        (len(text_bytes) + 2) >> 8,    # 长度高字节
        (len(text_bytes) + 2) & 0xFF,  # 长度低字节
        0x01,                          # 命令字
        encoding                       # 编码格式
    ]
    return bytes(packet) + text_bytes

def text_to_speech(text, encoding='GB2312'):
    """文本转语音"""
    packet = compose_speech_packet(text, EncodingFormat[encoding])
    i2c_write(packet)

def get_chip_status():
    """获取芯片状态"""
    try:
        i2c_write([DATA_HEAD, 0x00, 0x01, 0x21])  # 状态查询命令
        time.sleep(0.05)
        return bus.read_byte(I2C_ADDR)
    except Exception as e:
        print(f"读取状态失败: {str(e)}")
        return ChipStatus['ErrorCommand']

def wait_for_speech_complete():
    """等待语音播放完成"""
    while get_chip_status() != ChipStatus['Idle']:
        time.sleep(0.1)

def setup_synthesizer(reader='XuDuo', speed=5, volume=8):
    """合成参数配置"""
    # 设置发音人
    i2c_write([DATA_HEAD, 0x00, 0x02, 0x01, 0x6D, ReaderType[reader]])
    # 设置语速 (0-10)
    i2c_write([DATA_HEAD, 0x00, 0x02, 0x01, 0x73, speed])
    # 设置音量 (0-10)
    i2c_write([DATA_HEAD, 0x00, 0x02, 0x01, 0x76, volume])
    time.sleep(0.2)


def speech(res):
    try:
        # 初始化合成器参数
        setup_synthesizer(reader='XuDuo', speed=5, volume=8)
        
        # 合成并播放语音
        text_to_speech(res['response'])
         # 等待播放完成
        wait_for_speech_complete()
        
        time.sleep(1)
        for thing in res['thing_name']:
            text_to_speech(thing)
            time.sleep(1)
        
        # 等待播放完成
        wait_for_speech_complete()
        
        print("语音播报完成！")

    except KeyboardInterrupt:
        print("程序已终止")
    except Exception as e:
        print(f"发生错误: {str(e)}")


if __name__ == "__main__":
    thing = {
    "thing_name": ["红色方块", "绿色方块", "房子简笔画"]
    }
    speech(thing)