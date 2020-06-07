# coding:utf-8
# 【谷雨课堂】干货实战 No.011 语音唤醒与语音识别
# 作者：谷雨

import time
import wave
import pyaudio
from aip import AipSpeech
import win32com.client
import pygame

#语音合成输出
def speak(s):
    print("-->"+s)
    win32com.client.Dispatch("SAPI.SpVoice").Speak(s)

#调用百度云，进行语音识别
def audio_discern(audio_path = "./test.wav",audio_type = "wav"):

    """ 百度云的ID，免费注册 """
    APP_ID = '5377701' 
    API_KEY = 'xCAp8unagboTkKESzyfXEdZA' 
    SECRET_KEY = 'oOAcl2b1wGExlrOH2H9M16kE2YfsqDpE' 

    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    # 读取文件
    def get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()
    # 识别本地文件
    text = client.asr(get_file_content(audio_path), audio_type, 16000)
    return text

#用Pyaudio库录制音频
def audio_record(out_file, rec_time):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16 #16bit编码格式
    CHANNELS = 1 #单声道
    RATE = 16000 #16000采样频率
    p = pyaudio.PyAudio()
    # 创建音频流
    stream = p.open(format=FORMAT, # 音频流wav格式
                    channels=CHANNELS, # 单声道
                    rate=RATE, # 采样率16000
                    input=True,
                    frames_per_buffer=CHUNK)
    print("Start Recording...")
    frames = [] # 录制的音频流
    # 录制音频数据
    for i in range(0, int(RATE / CHUNK * rec_time)):
        data = stream.read(CHUNK)
        frames.append(data)
    # 录制完成
    #print(frames)
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    # 保存音频文件
    with wave.open(out_file, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
    

while(True):
    print("请讲话...")

    audio_path = "./test1.wav"
    # 录制语音指令
    audio_record(audio_path, 3) 

    print("开始做语音识别...")
    ret =  audio_discern(audio_path) # 识别语音指令    
    if ret["err_no"] == 0:
        text = ret["result"][0]      
        print(text)

        if '小娜' in text:
            speak('我在的')

        elif '诗' in text:
            speak('白日依山尽，黄河入海流。 欲穷千里目，更上一层楼。')

        elif '名字' in text:
            speak('我叫晓娜')

        # 如果是"退出"指令则结束程序
        elif text.find("退") != -1: 
            speak('再见')
            break
        else:
            pass

        # 延时一小会儿
        time.sleep(0.5) 
