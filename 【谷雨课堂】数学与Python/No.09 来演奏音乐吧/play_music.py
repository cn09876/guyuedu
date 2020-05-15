import time
from mido import Message, MidiFile, MidiTrack
import pygame as pg

bpm=70

mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

track1 = MidiTrack()
mid.tracks.append(track1)
track2 = MidiTrack()
mid.tracks.append(track2)

'''
播放一个音符
note 简谱的音符
length 音符长度
'''
def play_note(note, length, track,base_num=1, delay=0, velocity=1.0, channel=0):
   meta_time = 60 * 60 * 10 / bpm
   major_notes = [0, 2, 2, 1, 2, 2, 2, 1]
   base_note = 60
   track.append(Message('note_on', note=base_note + base_num*12 + sum(major_notes[0:note]), velocity=round(64*velocity), time=round(delay*meta_time), channel=channel))
   track.append(Message('note_off', note=base_note + base_num*12 + sum(major_notes[0:note]), velocity=round(64*velocity), time=round(meta_time*length), channel=channel))

#播放MIDI
def play_music(music_file):
    clock = pg.time.Clock()
    pg.mixer.music.load(music_file)
    pg.mixer.music.play()
    while pg.mixer.music.get_busy():
        clock.tick(30)

#播放集合中的音符
def guyu_play(yfs):
    pg.mixer.init()
    for y in yfs:        
        play_note(note=y[0],base_num=y[1],length=y[2],track=track)
    mid.save("1.mid")
    play_music("1.mid")

def play():
    pg.mixer.init()
    mid.save("1.mid")
    play_music("1.mid")

def guyu_hexuan():
    play_note(note=1,base_num=0,length=1,track=track)
    play_note(note=1,base_num=0,length=1,track=track1)
    play_note(note=1,base_num=0,length=1,track=track2)

    play_note(note=2,base_num=0,length=1,track=track)
    play_note(note=2,base_num=0,length=1,track=track1)
    play_note(note=2,base_num=0,length=1,track=track2)

    play_note(note=3,base_num=0,length=1,track=track)
    play_note(note=3,base_num=0,length=1,track=track1)
    play_note(note=3,base_num=0,length=1,track=track2)

    play_note(note=4,base_num=0,length=1,track=track)
    play_note(note=4,base_num=0,length=1,track=track1)
    play_note(note=4,base_num=0,length=1,track=track2)

    play_note(note=5,base_num=0,length=1,track=track)
    play_note(note=5,base_num=0,length=1,track=track1)
    play_note(note=5,base_num=0,length=1,track=track2)

    play_note(note=4,base_num=0,length=1,track=track)
    play_note(note=4,base_num=0,length=1,track=track1)
    play_note(note=4,base_num=0,length=1,track=track2)

    play_note(note=3,base_num=0,length=1,track=track)
    play_note(note=3,base_num=0,length=1,track=track1)
    play_note(note=3,base_num=0,length=1,track=track2)

    play_note(note=2,base_num=0,length=1,track=track)
    play_note(note=2,base_num=0,length=1,track=track1)
    play_note(note=2,base_num=0,length=1,track=track2)

    play_note(note=1,base_num=0,length=1,track=track)
    play_note(note=1,base_num=0,length=1,track=track1)
    play_note(note=1,base_num=0,length=1,track=track2)


    play_note(note=3,base_num=0,length=1,track=track)
    play_note(note=3,base_num=0,length=1,track=track1)
    play_note(note=3,base_num=0,length=1,track=track2)


    play_note(note=5,base_num=0,length=1,track=track)
    play_note(note=5,base_num=0,length=1,track=track1)
    play_note(note=5,base_num=0,length=1,track=track2)


    play_note(note=3,base_num=0,length=1,track=track)
    play_note(note=3,base_num=0,length=1,track=track1)
    play_note(note=3,base_num=0,length=1,track=track2)


    play_note(note=1,base_num=0,length=5,track=track)
    play_note(note=3,base_num=0,length=5,track=track1)
    play_note(note=5,base_num=0,length=5,track=track2)
    play()
######################################
shao_niao=[
    [1,0,0.5],#我
    [2,0,0.5],#还
    [1,0,0.8],#是
    [5,0,0.5],#从
    [5,0,0.5],#前
    [5,0,0.5],#那
    [3,0,0.5],#个
    [5,0,0.6],#少
    [3,0,0.8],#年
    [3,0,0.5],#没
    [2,0,0.5],#有
    [2,0,0.5],#一
    [2,0,0.5],#丝
    [2,0,0.5],#丝
    [1,0,0.5],#改
    [3,0,0.8],#变
    [2,0,0.5],#时
    [3,0,0.5],#间
    [6,-1,0.5],#只
    [1,0,0.5],#不
    [1,0,0.5],#过
    [6,-1,0.5],#是
    [6,-1,0.6],#考
    [1,0,0.7], #验
    [2,0,0.5], #种
    [1,0,0.5], #在
    [4,0,0.5], #心
    [4,0,0.5], #中
    [4,0,0.5], #信
    [3,0,0.5], #念
    [4,0,0.5], #丝
    [3,0,0.5], #毫
    [2,0,0.5],#未
    [1,0,0.8],#减
    [5,0,0.5],#眼
    [5,0,0.5],#前
    [5,0,0.5],#这
    [3,0,0.5],#个
    [5,0,0.8],#少
    [3,0,0.6],#年
    [3,0,0.5],#还
    [2,0,0.6],#是
    [2,0,0.5],#最
    [2,0,0.5],#初
    [2,0,0.5],#那
    [1,0,0.5],#张
    [3,0,0.7],#脸
    [2,0,0.5],#面
    [3,0,0.5],#前
    [6,-1,0.5],#再
    [1,0,0.5],#多
    [1,0,0.5],#艰
    [6,-1,0.5],#险
    [6,-1,0.5],#不
    [1,0,0.5],#退
    [1,0,9],#却
]

a1=[1,2,3,4,5]

###顺序音符
demo123456=[
    #音符,八度,音长
    [1,0,1],
    [2,0,1],
    [3,0,1],
    [4,0,1],
    [5,0,1],
    [6,0,1],
    [7,0,1],
    [1,1,10],
    [1,1,1],
    [7,0,1],
    [6,0,1],
    [5,0,1],
    [4,0,1],
    [3,0,1],
    [2,0,1],
    [1,0,10],
]

#bpm=200
#guyu_play(demo123456)

#来个大三和弦
#bpm=80
#guyu_hexuan()

bpm=60
guyu_play(shao_niao)
