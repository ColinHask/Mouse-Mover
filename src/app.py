import sys
import pyautogui as pag
import random
import time
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class AFKEngine(QObject):

    def __init__(self):
        super().__init__()
        self.running = False

    #moves user's mouse when activated, prints waiting when waiting
    #main loop for AFK engine
    def run(self):
        print("ENGINE RUNNING")
        while True:
            if self.running == False:
                print("PAUSED")
                time.sleep(2)
            else:
                print("MOVING")
                x = random.randint(500,1000)
                y = random.randint(200,600)
                # duration = random.randint(0.1,1)
                pag.moveTo(x, y, duration=0.2)
                time.sleep(2)

    
    def pause(self):
        self.running = False
        print("run_AFK stopped")

    
    def start(self):
        self.running = True
        print("run_AFK started")

    #toggles AFK using button
    #slot acessed by GUIWindow button
    def toggle_AFK(self ,checked,):
        if checked:
            self.start()
        else:
            self.pause()
            



class GUIWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mouse Mover")

        #create main label
        lbl = QLabel()
        lbl.setText("Welcome to Mouse Mover! Click the button to toggle automatic mouse moving.")

        #create toggling buttton 
        self.button = QPushButton(text="START Mouse Movement", parent=self)
        self.button.setCheckable(True)
        #connect button to toggling text func
        self.button.clicked.connect(self.toggle_button_text)

        # create layout
        layout = QVBoxLayout()
        layout.addWidget(lbl)
        layout.addWidget(self.button)

        #central widget takes up full space in window
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
        #create thread obj
        self.thread = QThread()

        #create AFK engine obj as worker
        self.worker = AFKEngine()

        #connect button clicking (signal) to worker toggle_AFK (slot)
        self.button.clicked.connect(self.worker.toggle_AFK)

        #place worker into thread
        self.worker.moveToThread(self.thread)

        #connect thread starting signal to AFK engine running
        self.thread.started.connect(self.worker.run)
       
        #starts thread containing AFK engine
        self.thread.start()

    #toggles AFK text using button
    def toggle_button_text(self ,s,):
        if self.button.isChecked():
            self.button.setText("STOP Mouse Movement")
        else:
            self.button.setText("START Mouse Movement")
            
#setup main window, show window, and execute app            
app = QApplication(sys.argv)
window = GUIWindow()
window.show()
app.exec()