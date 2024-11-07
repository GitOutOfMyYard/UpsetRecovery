from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QPushButton, QWidget, QTextEdit, QLineEdit
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPalette, QColor


import sys
from .config import WINDOW_SIZE


class LoginField(QLineEdit):
    def __init__(self, text):
        super().__init__(text)
        # self.setTextColor(Qt.gray)
        self.setPlaceholderText(text)
        # self.setText(text)
        self.setMaximumSize(400, 32)
        # self.not_edited = True
        self.not_edited = False

    def mousePressEvent(self, e):
        if e.pos() in self.rect():
            if self.not_edited:
                self.clear()
                self.not_edited = False
            self.setStyleSheet(
                '''
                color : rgb(0, 0, 0);
                background-color: rgb(255, 255, 255);
                '''
            )
        super().mousePressEvent(e)

    def indicate_wrong_data(self) -> None:
        self.setStyleSheet(
            """
            color: rgb(0, 0, 0);
            background-color: rgb(200, 140, 140)
            """
        )





class LoginWindow(QWidget):

    startBtnPressed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.logging = True
        layout = QVBoxLayout()
        self.setWindowTitle('Login')
        self.first_name_field = LoginField('Введите Имя')
        self.last_name_field = LoginField('Введите Фамилию')
        self.middle_name_field = LoginField('Введите Отчество')
        self.group_field = LoginField('Введите Номер Группы')

        self.start_btn = QPushButton(' Начать !')
        self.cancel_btn = QPushButton(' Отмена ')

        layout.addWidget(self.last_name_field)
        layout.addWidget(self.first_name_field)
        layout.addWidget(self.middle_name_field)
        layout.addWidget(self.group_field)
        layout.addWidget(self.start_btn)
        layout.addWidget(self.cancel_btn)
        self.setLayout(layout)
        self.start_btn.clicked.connect(self.okay)
        self.cancel_btn.clicked.connect(self.cancel)

        self.first_name_field.setSelection(0,
                                           len(self.first_name_field.placeholderText()))

    def cancel(self):
        self.logging = False
        self.close()
        return False

    def get_login_data(self):
        if self.check_fields():
            self.first_name = self.first_name_field.text()
            self.middle_name = self.middle_name_field.text()
            self.last_name = self.last_name_field.text()
            self.group = self.group_field.text()
            self.logging = False
            for field in (self.group_field, self.last_name_field, self.middle_name_field, self.first_name_field):
                field.clear()
            self.close()
            return self.group, self.last_name, self.first_name, self.middle_name
        else:
            return None

    def okay(self):
        if self.check_fields():
            self.startBtnPressed.emit()
            self.logging = False
            self.close()


    def check_fields(self):
        fields_filled = True
        for field in (self.group_field, self.last_name_field, self.middle_name_field, self.first_name_field):
            if not len(field.text()) and field.text() != field.placeholderText():
                fields_filled = False
                field.indicate_wrong_data()
        return fields_filled


class WelcomingWidget(QWidget):
    startTestBtnPressed = pyqtSignal()
    startTrainBtnPressed = pyqtSignal()

    def __init__(self):
        self.log_window = None
        super(QWidget, self).__init__()
        layout = QVBoxLayout()
        self.start_test_btn = QPushButton('Начать "Вывод из СПП"')
        self.start_test_btn.pressed.connect(self.startTestBtnPressed.emit)
        layout.addWidget(self.start_test_btn)
        self.start_train_btn = QPushButton('Включить тренировочный режим')
        self.start_train_btn.pressed.connect(self.startTrainBtnPressed.emit)
        layout.addWidget(self.start_train_btn)
        self.setLayout(layout)

    def start_upset_reovery(self):
        self.startTestBtnPressed.emit()

    def login_user(self):
        if not self.log_window:
            self.log_window = LoginWindow()
        self.log_window.show()


class PFDMainWindow(QMainWindow):

    def __init__(self, central_widget):
        super().__init__()
        minimum_width, minimum_height = WINDOW_SIZE
        self.setMinimumSize(minimum_width, minimum_height)
        self.setWindowTitle('Upset Recovery')
        self.setCentralWidget(central_widget)
