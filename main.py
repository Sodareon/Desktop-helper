
import sys
import os
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore, QtGui, Qt
import subprocess
import configparser
import keyboard
import voice_helper


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle("Desktop Helper")
        self.setGeometry(100, 100, 600, 800)
        self.old_pos = (100, 100)
        self.settings = Settings()
        self.assistant = voice_helper.Assistant(self.settings.name)
        self.voice_on = False

        # Изменение обычного окна в окно-картинку
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)
        self.pixmap = QtGui.QPixmap("fon.png")
        self.pal = self.palette()
        self.pal.setBrush(QtGui.QPalette.Normal, QtGui.QPalette.Window, QtGui.QBrush(self.pixmap))
        self.pal.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, QtGui.QBrush(self.pixmap))
        self.setPalette(self.pal)
        self.setMask(self.pixmap.mask())

        # Контекстное меню
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

        self.menu = QtWidgets.QMenu(self)
        action1 = self.menu.addMenu('Папки')
        sub_action = action1.addAction('test2')
        sub_action.triggered.connect(open_folder)
        action2 = self.menu.addAction('Найстроки')
        action2.triggered.connect(self.settings.application_settings)
        action3 = self.menu.addAction('Закрыть окно')
        action3.triggered.connect(self.hide)
        action4 = self.menu.addAction('вкл/выкл')
        action4.triggered.connect(self.voice_helper)

        # Трей и его меню
        self.tray_icon = QtWidgets.QSystemTrayIcon(self)
        self.tray_icon.setIcon(Qt.QIcon("fon_trey.png"))

        show_action = QtWidgets.QAction("Развернуть", self)
        quit_action = QtWidgets.QAction("Выйти", self)
        hide_action = QtWidgets.QAction("Свернуть", self)
        show_action.triggered.connect(self.show)
        quit_action.triggered.connect(self.exit_program)
        hide_action.triggered.connect(self.hide)
        tray_menu = QtWidgets.QMenu()
        tray_menu.addAction(hide_action)
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        # Горячие клавиши
        keyboard.add_hotkey('alt+s', self.show)
        keyboard.add_hotkey('ctrl+s', self.hide)
        keyboard.add_hotkey('shift+s', self.exit_program)

    def show_context_menu(self, point):
        self.menu.exec(self.mapToGlobal(point))

    # вызывается при нажатии кнопки мыши
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.old_pos = event.pos()

    # вызывается при отпускании кнопки мыши
    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.old_pos = None

    # вызывается всякий раз, когда мышь перемещается
    def mouseMoveEvent(self, event):
        if not self.old_pos:
            return
        delta = event.pos() - self.old_pos
        self.move(self.pos() + delta)

    def voice_helper(self):
        if self.voice_on:
            self.voice_on = False
            # выкл голос
        else:
            self.voice_on = True

            self.assistant.name = self.settings.name
            self.assistant.volume = self.settings.volume
            print(self.assistant.name)
            self.assistant.start()

    def exit_program(self):
        with open(self.settings.file, "w") as config_file:
            self.settings.config.write(config_file)
        exit()


class Settings(QMainWindow):
    def __init__(self):
        super(Settings, self).__init__()
        self.name = "маруся"
        self.setWindowTitle("Найстроки")
        self.setGeometry(100, 100, 600, 800)

        self.file = "settings.ini"

        self.volume = 100
        self.config = configparser.ConfigParser()

        self.config_data()

        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.slider.setRange(0, 100)
        self.slider.setValue(self.volume)
        self.slider.valueChanged.connect(lambda: self.slider_change())
        self.label = QtWidgets.QLabel('0', self)
        self.label.move(150, 0)
        self.label.setText(str(self.slider.value()))

        self.btn = QtWidgets.QPushButton('Сохранить', self)
        self.btn.move(20, 70)
        self.btn.clicked.connect(self.save_name)

        self.name_entry = QtWidgets.QLineEdit(self)
        self.name_entry.move(20, 100)
        self.name_entry.setText(self.name)

    def slider_change(self):
        self.label.setText(str(self.slider.value()))
        self.volume = self.slider.value()

    def save_name(self):
        print('сохранено')
        self.config.set("Settings", "volume", f"{self.volume}")
        if self.name_entry.text():
            self.name = self.name_entry.text().lower()
            self.config.set("Settings", "name", self.name)

    def application_settings(self):
        self.show()

    def config_create(self):
        self.config.add_section("Settings")
        self.config.set("Settings", "name", "маруся")
        self.config.set("Settings", "volume", "100")

        with open(self.file, "w") as config_file:
            self.config.write(config_file)

    def config_data(self):
        if not os.path.exists(self.file):
            self.config_create()
        self.config.read(self.file)
        self.name = self.config.get("Settings", "name")
        self.volume = int(self.config.get("Settings", "volume"))


def open_folder():
    try:
        subprocess.Popen('explorer "%s"' % "test2", cwd="C:/Users/napal/Desktop/test1")
    except NotADirectoryError:
        print("Папка не найдена")


def application():
    app = QApplication(sys.argv)
    window = Window()

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    application()
