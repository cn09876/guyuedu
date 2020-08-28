# coding:utf-8
# 【谷雨课堂】干货实战 No.022 AI作曲!生成一段背景音乐
# 作者：谷雨

import json
import random
from midiutil.MidiFile import MIDIFile
import pygame as pg


class RandomNote(object):
    def __init__(self, choose_from, interval_upper, interval_lower):
        self.last_played = 0
        self.notes = choose_from
        self.interval_upper = interval_upper
        self.interval_lower = interval_lower

    def random_note(self):
        while True:
            note = random.choice(range(1, len(self.notes) + 1))
            if not self.last_played:
                break
            else:
                if random.choice(self.interval_upper) \
                        >= abs(note - self.last_played) \
                        >= random.choice(self.interval_lower):
                    break
                else:
                    continue
        self.last_played = note
        return self.notes[self.last_played - 1]

    def reset(self):
        self.last_played = 0


class RandomMusic(object):
    def __init__(self, length=4, tempo=90):
        self.length = length
        self.tempo = tempo

        rules_file = open("rules.json", "r")
        rules = json.load(rules_file)
        rules_file.close()
        self.rhythm = rules["rhythm"]
        self.seq_chord = rules["seq_chord"]
        self.seq_perc = rules["seq_perc"]
        self.velocity = rules["velocity"]
        self.rn = RandomNote(rules["notes"], rules["interval_upper"], rules["interval_lower"])
        self.MyMIDI = MIDIFile(3)
        self.current_track_number = 0

    def create_melody_sequence(self):
        seq_melody = []
        for i in range(self.length):
            for phrase in self.rhythm:
                self.rn.reset()
                for duration in phrase:
                    seq_melody.append((self.rn.random_note(), duration))
        return seq_melody

    def create_melody_track(self):
        seq_melody = self.create_melody_sequence()

        self.MyMIDI.addTrackName(
            track=self.current_track_number,
            time=0, trackName="piano")
        self.MyMIDI.addTempo(
            track=self.current_track_number,
            time=0, tempo=self.tempo)
        self.MyMIDI.addProgramChange(
            tracknum=self.current_track_number,
            channel=0, time=0, program=0)

        pos = 0
        for pitch, duration in seq_melody:
            relative_pos = pos - int(pos / 4) * 4
            if 0 <= relative_pos < 1:
                vol = self.velocity["strong"]
            elif 2 <= relative_pos < 3:
                vol = self.velocity["intermediate"]
            else:
                vol = self.velocity["weak"]
            self.MyMIDI.addNote(
                track=self.current_track_number,
                channel=0, pitch=pitch, time=pos, duration=duration, volume=vol)
            if relative_pos in [0, 2]:
                self.MyMIDI.addControllerEvent(
                    track=self.current_track_number,
                    channel=0, time=pos, controller_number=64, parameter=127)
                self.MyMIDI.addControllerEvent(
                    track=self.current_track_number,
                    channel=0, time=pos + 1.96875, controller_number=64, parameter=0)
            pos += duration
        self.current_track_number += 1

    def create_chord_track(self):
        self.MyMIDI.addTrackName(
            track=self.current_track_number,
            time=0, trackName="chords")
        self.MyMIDI.addTempo(
            track=self.current_track_number,
            time=0, tempo=self.tempo)
        self.MyMIDI.addProgramChange(
            tracknum=self.current_track_number,
            channel=0, time=0, program=0)

        # C  D  E  F  G  A  B  | C  D  E  F  G  A  B  | C
        # 48 50 52 53 55 57 59 | 60 62 64 65 67 69 71 | 72

        pos = 0
        while pos < self.length * 16:
            for item in self.seq_chord:
                for pitch in item:
                    self.MyMIDI.addControllerEvent(
                        track=self.current_track_number,
                        channel=0, time=pos, controller_number=64, parameter=127)
                    self.MyMIDI.addControllerEvent(
                        track=self.current_track_number,
                        channel=0, time=pos + 1.96875, controller_number=64, parameter=0)
                    self.MyMIDI.addNote(
                        track=self.current_track_number,
                        channel=0, pitch=pitch, time=pos, duration=2, volume=76)
                    self.MyMIDI.addControllerEvent(
                        track=self.current_track_number,
                        channel=0, time=pos + 2, controller_number=64, parameter=127)
                    self.MyMIDI.addControllerEvent(
                        track=self.current_track_number,
                        channel=0, time=pos + 3.96875, controller_number=64, parameter=0)
                    self.MyMIDI.addNote(
                        track=self.current_track_number,
                        channel=0, pitch=pitch, time=pos + 2, duration=2, volume=68)
                pos += 4
        self.current_track_number += 1

    def create_perc_track(self):
        self.MyMIDI.addTrackName(
            track=self.current_track_number,
            time=0, trackName="perc")
        self.MyMIDI.addTempo(
            track=self.current_track_number,
            time=0, tempo=self.tempo)
        self.MyMIDI.addProgramChange(
            tracknum=self.current_track_number,
            channel=9, time=0, program=0)

        pos = 0
        while pos < self.length * 16:
            if pos != 0:
                self.MyMIDI.addNote(
                    track=self.current_track_number,
                    channel=9, pitch=49, time=pos, duration=0.5, volume=102)
            for pitch, duration in self.seq_perc:
                relative_pos = pos - int(pos / 4) * 4
                if 0 <= relative_pos < 1:
                    vol = 102
                elif 2 <= relative_pos < 3:
                    vol = 96
                else:
                    vol = 92
                self.MyMIDI.addNote(
                    track=self.current_track_number,
                    channel=9, pitch=pitch, time=pos, duration=duration, volume=vol)
                pos += duration
        self.current_track_number += 1

    def create_midi_file(self, filename, melody=True, chord=True, perc=True):
        if melody:
            self.create_melody_track()
        if chord:
            self.create_chord_track()
        if perc:
            self.create_perc_track()
        with open(filename, "wb") as midi_file:
            self.MyMIDI.writeFile(midi_file)


#--------------------------------------------------------------------------------------------------------------
#随机生成一段音乐 
mid = RandomMusic(length=8,tempo=75)
mid.create_midi_file("midi.mid")

#播放刚才生成的音乐
pg.mixer.init(44100, 16, 2, 2048)
pg.mixer.music.set_volume(0.8)
clock = pg.time.Clock()
pg.mixer.music.load("midi.mid")
pg.mixer.music.play()
while pg.mixer.music.get_busy():
    clock.tick(30)

