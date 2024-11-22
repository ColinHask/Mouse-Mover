import sys
import pyautogui as pag
import random
import time
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class AFKEngine(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)


    def run(self):
        '''
        Initialise the runner function with passed self.args, self.kwargs.
        '''
        print("run_AFK started")
        
        while True:
            x = random.randint(500,1000)
            y = random.randint(200,600)
            # duration = random.randint(0.1,1)
            pag.moveTo(x, y, duration=0.2)
            time.sleep(1)


class GUIWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mouse Mover")
        lbl = QLabel()
        lbl.setText("Welcome to Mouse Mover! Click the button to toggle automatic mouse moving.")
        self.button = QPushButton(text="START Mouse Movement", parent=self)
        self.button.setCheckable(True)
        self.button.clicked.connect(self.toggle_AFK)

        

        layout = QVBoxLayout()
        layout.addWidget(lbl)
        layout.addWidget(self.button)

        #central widget takes up full space in window
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        
        self.thread = QThread()

        #threading for AFK
        # self.threadpool = QThreadPool()
        # print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

    #toggles AFK using button
    def toggle_AFK(self ,s,):
        if self.button.isChecked():
            self.button.setText("STOP Mouse Movement")
            self.AFK = True
            self.worker = AFKEngine()
            self.worker.moveToThread(self.thread)

            # Connect signals and slots
            self.thread.started.connect(self.worker.run)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
           

            self.thread.start()
        else:
            self.button.setText("START Mouse Movement")
            self.AFK = False
            self.thread.quit()


        



        

        






app = QApplication(sys.argv)
window = GUIWindow()
window.show()
app.exec()