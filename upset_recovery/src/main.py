from PyQt5.QtWidgets import QApplication

from upset_recovery.src.presenters.presenter import Presenter
from upset_recovery.src.views.pdf_mainloop import UpsetRecoveryWindow
from upset_recovery.src.views.mainwindow import PFDMainWindow, WelcomingView



def start_app(app: QApplication) -> None:
    central_widget = WelcomingView()
    presenter = Presenter(central_widget, UpsetRecoveryWindow)
    w = PFDMainWindow(central_widget)
    w.show()
    app.exec_()
