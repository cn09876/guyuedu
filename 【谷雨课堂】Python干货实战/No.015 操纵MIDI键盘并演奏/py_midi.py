# coding:utf-8
# 【谷雨课堂】干货实战 No.015 用Python操纵MIDI键盘并演奏
# 作者：谷雨

from __future__ import print_function
import json
import logging
import sys
import time
import rtmidi
import win32com.client

#语音合成输出
def speak(s):
    print("-->"+s)
    win32com.client.Dispatch("SAPI.SpVoice").Speak(s)


midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

if available_ports:
    midiout.open_port(0)
else:
    midiout.open_virtual_port("My virtual output")

from rtmidi.midiutil import open_midiinput

log = logging.getLogger('midiin_callback')
logging.basicConfig(level=logging.DEBUG)


class MidiInputHandler(object):
    def __init__(self, port,midiout):
        self.port = port
        self.midiout = midiout
        self._wallclock = time.time()

    def __call__(self, event, data=None):
        message, deltatime = event
        #self.midiout.send_message(message)
        self._wallclock += deltatime
        aa=message[1]
        bb=message[2]
        if True:
                if bb==0:
                        if aa==60:speak("兜")
                        if aa==61:speak("升兜")
                        if aa==62:speak("来")
                        if aa==63:speak("升来")
                        if aa==64:speak("眯")
                        if aa==65:speak("升眯")
        print("[%s] %r" % (self.port,  message))


# Prompts user for MIDI input port, unless a valid port number or name
# is given as the first argument on the command line.
# API backend defaults to ALSA on Linux.
port = 0

try:
    midiin, port_name = open_midiinput(port)
except (EOFError, KeyboardInterrupt):
    sys.exit()

print("Attaching MIDI input callback handler.")
midiin.set_callback(MidiInputHandler(port_name,midiout))

print("Entering main loop. Press Control-C to exit.")
try:
    # Just wait for keyboard interrupt,
    # everything else is handled via the input callback.
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print('')
finally:
    print("Exit.")
    midiin.close_port()
    del midiin
    del midiout