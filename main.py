import os
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime

opts = {
    "name": ("маруся", "марусь"),
    "tbr": ("скажи", "расскажи", "покажи", "сколько", "произнеси"),
    "cmds": {
        "ctime": ("текущее время", "сейчас времени", "который час"),
        "stupid1": ('расскажи анекдот', 'рассмеши меня', 'ты знаешь анекдоты')
    }
}

def speak(what):
    print(what)
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()

def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language="ru-RU").lower()
        if voice.startswith(opts["name"]):
            cmd = voice
            for i in opts["name"]:
                cmd = cmd.replace(i, "").strip()
            for i in opts["tbr"]:
                cmd = cmd.replace(i, "").strip()
            cmd = recognize_cmd(cmd)
            execute_cmd(cmd["cmd"])
    except sr.UnknownValueError:
        speak("Голос не распознан!")
    except sr.RequestError:
        speak("Неизвестная ошибка, проверьте интернет!")


def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c, v in opts['cmds'].items():
        for i in v:
            vrt = fuzz.ratio(cmd, i)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt
    return RC

def execute_cmd(cmd):
    if cmd == 'ctime':
        now = datetime.datetime.now()
        speak("Сейчас " + str(now.hour) + ":" + str(now.minute))
    elif cmd == "stupid1":
        speak("Мой разработчик не научил меня анекдотам ... Ха ха ха")
    else:
        speak("Команда не распознана повторите")

r = sr.Recognizer()
m = sr.Microphone()

with m as source:
    r.adjust_for_ambient_noise(source)

speak_engine = pyttsx3.init()

speak("Привет!")

stop_listening = r.listen_in_background(m, callback)
while True: time.sleep(0.1)