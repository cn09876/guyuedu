# coding:utf-8
# 【谷雨课堂】干货实战 No.024 Python实现《信条》逆向语音翻译机
# 作者：谷雨

 
from pydub import AudioSegment
from pydub.playback import play
import wave
import pyaudio
import numpy as np
import matplotlib.pyplot as plt  #专业绘图库
import pylab
from scipy.io import wavfile

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
    print("开始录制...")
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
    
    print("录制结束！")
    

audio_record("rec.wav",5)

#读取刚才录好的语音文件
song = AudioSegment.from_wav("rec.wav")
#进行逆向
backwards = song.reverse()
#保存文件
backwards.export("out.wav", format='wav')
#播放文件
play(backwards)

