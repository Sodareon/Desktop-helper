
import speech_recognition
import sys
import pyttsx3
import datetime
import webbrowser
import subprocess
import requests
import random
from PyQt5.QtCore import QThread


class Assistant(QThread):
    def __init__(self, name, parent=None):
        super(Assistant, self).__init__(parent)
        self.name = name
        self.recognizer = speech_recognition.Recognizer()
        self.microphone = speech_recognition.Microphone()
        self.engine = pyttsx3.init()
        self.flag = True
        self.open_weather_token = "2fad03f24b1ec802000fb071361928b2"
        self.city = "Красноярск"

    def record_and_recognize_audio(self):
        """
        Запись и распознавание аудио
        """
        with self.microphone:
            recognized_data = ""

            # регулирование уровня окружающего шума
            self.recognizer.adjust_for_ambient_noise(self.microphone, duration=2)

            try:
                print("Listening...")
                audio = self.recognizer.listen(self.microphone, 5, 5)

            except speech_recognition.WaitTimeoutError:
                print("Ошибка: время вышло")
                return

            # использование online-распознавания через Google
            try:
                print("Started recognition...")
                recognized_data = self.recognizer.recognize_google(audio, language="ru").lower()

            except speech_recognition.UnknownValueError:
                print("Ошибка: голос не распознан")

            # в случае проблем с доступом в Интернет происходит выброс ошибки
            except speech_recognition.RequestError:
                print("Ошибка: проблема с доступом в интернет")

            return recognized_data

    def talk(self, text_to_speech):
        self.engine.say(text_to_speech)
        self.engine.runAndWait()

    def get_weather(self):

        try:
            r = requests.get(
                f"http://api.openweathermap.org/data/2.5/weather?q={self.city}&appid"
                f"={self.open_weather_token}&units=metric&lang=ru"
            )
            data = r.json()
            self.city = data["name"] + "e"
            cur_weather = round(data["main"]["temp"])
            cur_weather_feels = round(data["main"]["feels_like"])
            print(f"Температура в {self.city} сейчас {cur_weather} "
                  f"° цельсия, ощущается как {cur_weather_feels} ° цельсия")
            self.talk(f"Температура в {self.city} сейчас {cur_weather} ° цельсия,"
                      f" ощущается как {cur_weather_feels} ° цельсия")

        except Exception as ex:
            print(ex)
            print("Что-то не работает")

    def commands(self, voice):
        if self.name in voice:
            if "время" in voice or "времени" in voice or "который час" in voice:
                now = datetime.datetime.now()
                print(f"Сейчас {str(now.hour)}:{str(now.minute)}")
                self.talk("Сейчас " + str(now.hour) + ":" + str(now.minute))
            elif "анекдот" in voice or "рассмеши меня" in voice:
                print("Мой разработчик не научил меня анекдотам ... Ха ха ха")
                self.talk("Мой разработчик не научил меня анекдотам ... Ха ха ха")
            elif "видео" in voice:
                webbrowser.open("https://www.youtube.com/", new=2)
            elif ("открыть" in voice or "открой" in voice) and "блокнот" in voice:
                subprocess.Popen('C:/Windows/system32/notepad.exe')
            elif "установить уровень громкости" in voice or "установить громкость" in voice or "громкость" in voice:
                volume = sort_string(voice)
                if (volume <= 100) and (volume >= 10):
                    self.engine.setProperty("volume", volume/100)
                    self.talk("Уровень громкости изменён")
                else:
                    print("Сказанное значение некорректно")
                    self.talk("Сказанное значение некорректно")
            elif "погода" in voice:
                self.get_weather()
            elif "пока" in voice:
                self.talk("До свидания")
                self.flag = False

    def work(self):
        # старт записи речи с последующим выводом распознанной речи
        voice_input = self.record_and_recognize_audio()
        print(voice_input)
        # выполнение команды пользователя
        self.commands(voice_input)

    def run(self):
        self.talk(random_greetings())
        while self.flag:
            self.work()


def random_greetings():
    greetings = ["Привет", "Здравствуйте", "Приветствую"]
    hour = int(datetime.datetime.now().hour)
    if (hour >= 0) and (hour < 5):
        greetings.append("Доброе утро")
    elif (hour >= 5) and (hour < 12):
        greetings.append("Добрый день")
    elif (hour >= 12) and (hour < 18):
        greetings.append("Добрый вечер")
    else:
        greetings.append("Доброй ночи")
    print("Greetings...")
    return random.choice(greetings)


def sort_string(string):
    percent = []
    num = ""
    for char in string:
        if char.isdigit():
            num += char
        else:
            if num != "":
                percent.append(int(num))
                num = ""
    if num != "":
        percent.append(int(num))
    return percent[0]


def main():
    assistant = Assistant("маруся")
    assistant.run()


if __name__ == "__main__":
    main()
