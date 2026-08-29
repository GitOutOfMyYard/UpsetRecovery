from typing import Optional, Callable

from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget, \
    QLineEdit
from PyQt5.QtCore import pyqtSignal

from upset_recovery_sim.src.config import WINDOW_SIZE
from upset_recovery_sim.src.dtos import LoginDataDto
from upset_recovery_sim.src.presenters.view_interfaces import IWelcomingView


class LoginField(QLineEdit):
    def __init__(self, text):
        super().__init__(text)
        self.setPlaceholderText(text)
        self.setMaximumSize(400, 32)
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

    def get_login_data(self) -> Optional[LoginDataDto]:
        result = None
        if self.check_fields():
            first_name = self.first_name_field.text()
            middle_name = self.middle_name_field.text()
            last_name = self.last_name_field.text()
            group = self.group_field.text()
            self.logging = False
            for field in (self.group_field, self.last_name_field, self.middle_name_field, self.first_name_field):
                field.clear()
            self.close()
            result = LoginDataDto(group, last_name, first_name, middle_name)
            return result

        return result

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

    #
    # def set_prepare_test_callback(self, callback: Callable[[], None]):
    #     self.startTestBtnPressed.connect(callback)
    #
    # def set_start_test_callback(self, callback: Callable[[], None]):
    #     self.log_window.startBtnPressed.connect(callback)
    #
    # def set_start_train_callback(self, callback: Callable[[], None]):
    #     self.startTestBtnPressed.connect(callback)


class WelcomingView(IWelcomingView):

    def __init__(self):
        self._widget = WelcomingWidget()

    def login_user(self):
        return self._widget.login_user()

    def set_prepare_test_callback(self, callback: Callable[[], None]) -> None:
        self._widget.startTestBtnPressed.connect(callback)

    def set_start_test_callback(self, callback: Callable[[], None]) -> None:
        self._widget.log_window.startBtnPressed.connect(callback)


    def set_start_train_callback(self, callback: Callable[[], None]) -> None:
        self._widget.startTrainBtnPressed.connect(callback)

    def get_login_data(self) -> Optional[LoginDataDto]:
        return self._widget.log_window.get_login_data()

    def get_widget(self) -> QWidget:
        return self._widget


class PFDMainWindow(QMainWindow):

    def __init__(self, welcome_view: WelcomingView) -> None:
        super().__init__()
        minimum_width, minimum_height = WINDOW_SIZE
        self.setMinimumSize(minimum_width, minimum_height)
        self.setWindowTitle('Upset Recovery')
        self.setCentralWidget(welcome_view.get_widget())
