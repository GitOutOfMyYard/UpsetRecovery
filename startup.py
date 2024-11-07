from PyQt5.QtWidgets import QApplication
import sys
from upset_recovery.presenter import Presenter
from upset_recovery.pdf_mainloop import UpsetRecoveryWindow
from upset_recovery.mainwindow import PFDMainWindow, WelcomingWidget


app = QApplication(sys.argv)
central_widget = WelcomingWidget()
presenter = Presenter(central_widget, UpsetRecoveryWindow)
w = PFDMainWindow(central_widget)
w.show()
app.exec_()
