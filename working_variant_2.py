import speech_recognition
import sys
import pyttsx3
import datetime
import webbrowser
import subprocess
import requests
import random
import pymorphy2
import wikipediaapi
from googletrans import Translator

class Assistant:
    def __init__(self, name):
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
            cur_weather = round(data["main"]["temp"])
            cur_weather_feels = round(data["main"]["feels_like"])
            city = change_word_form(self.city)
            print(f"Температура в {city} сейчас {cur_weather} "
                  f"° цельсия, ощущается как {cur_weather_feels} ° цельсия")

            self.talk(f"Температура в {city} сейчас {cur_weather} ° цельсия,"
                      f" ощущается как {cur_weather_feels} ° цельсия")

        except Exception as ex:
            print(ex)
            print("Что-то не работает")


    def random_goodbye(self):
        bye = ["Пока", "До свидания", "До встречи"]
        hour = int(datetime.datetime.now().hour)
        if (hour >= 0) and (hour < 5):
            bye.append("Спокойной ночи")
        elif (hour >= 5) and (hour < 12):
            bye.append("Хорошего дня")
        elif (hour >= 12) and (hour < 18):
            bye.append("Увидимся позже")
        else:
            bye.append("Не сидите допоздна")
        print("Прощание...")
        self.talk(random.choice(bye))


    def search_in_wikipedia(self, search_term):
        wiki = wikipediaapi.Wikipedia("ru")
        wiki_page = wiki.page(search_term)
        try:
            if wiki_page.exists():
                webbrowser.get().open(wiki_page.fullurl)
                print(f"Вот что найдено по запросу {search_term} в Википедии: ", end="")
                print(wiki_page.summary)
                self.talk(("Вот что найдено по запросу {} в Википедии").format(search_term))
                self.talk(wiki_page.summary)
            else:
                print("По запросу ничего не найдено")
                self.talk("По запросу {} ничего не найдено".format(search_term))
        except:
            print("Похоже возникла какая-то ошибка")
            self.talk("Похоже возникла какая-то ошибка")


    def google_translate(self,word_to_translate):
        translator = Translator()
        r = translator.detect(word_to_translate)
        if r == "en":
            result = translator.translate(word_to_translate, src=r, dest="ru")
            print(result.text)
            self.talk(result.text)
        elif r == "ru":
            result = translator.translate(word_to_translate, src=r, dest="en")
            print(result.text)
            self.talk(result.text)
    def commands(self, voice):
        if self.name in voice:
            if "время" in voice or "времени" in voice or "который час" in voice:
                now = datetime.datetime.now()
                print(f"Сейчас {str(now.hour)}:{str(now.minute)}")
                self.talk("Сейчас " + str(now.hour) + ":" + str(now.minute))
            elif "анекдот" in voice or "рассмеши меня" in voice:
                print("Мой разработчик не научил меня анекдотам ... Ха ха ха")
                self.talk("Мой разработчик не научил меня анекдотам ... Ха ха ха")
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
            elif "поиск в википедии" in voice or "википедия" in voice or "википедии" in voice:
                print("Скажите запрос")
                self.talk("Скажите запрос")
                search_term = self.record_and_recognize_audio()
                print(search_term)
                self.search_in_wikipedia(search_term)
            elif "поиск в браузере" in voice or "поиск в google" in voice or "найди в браузере" in voice or "найди в google" in voice:
                print("Скажите запрос")
                self.talk("Скажите запрос")
                search_term = self.record_and_recognize_audio()
                print(search_term)
                url = "https://google.com/search?q=" + search_term
                webbrowser.get().open(url)
            elif "поиск в youtube" in voice or "найди в youtube" in voice:
                print("Скажите запрос")
                self.talk("Скажите запрос")
                search_term = self.record_and_recognize_audio()
                print(search_term)
                url = "https://www.youtube.com/results?search_query=" + search_term
                webbrowser.get().open(url)
            elif "переведи" in voice:
                print("Скажите слово или фразу")
                self.talk("Скажите слово или фразу")
                word = self.record_and_recognize_audio()
                print(word)
                self.google_translate(word)
            elif "пока" in voice:
                self.random_goodbye()
                self.flag = False

    def work(self):
        # старт записи речи с последующим выводом распознанной речи
        voice_input = self.record_and_recognize_audio()
        print(voice_input)
        # выполнение команды пользователя
        self.commands(voice_input)


def random_greetings():
    greetings = ["Привет", "Здравствуйте", "Приветствую"]
    hour = int(datetime.datetime.now().hour)
    if (hour >= 0) and (hour < 5):
        greetings.append("Доброй ночи")
    elif (hour >= 5) and (hour < 12):
        greetings.append("Доброе утро")
    elif (hour >= 12) and (hour < 18):
        greetings.append("Добрый день")
    else:
        greetings.append("Добрый вечер")
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


def change_word_form(word):
    morph = pymorphy2.MorphAnalyzer()
    p = morph.parse(word)[0]
    p = p.inflect({"loct"})
    return p[0]


def main():
    assistant = Assistant("маруся")
    assistant.talk(random_greetings())
    while assistant.flag:
        assistant.work()


if __name__ == "__main__":
    main()
