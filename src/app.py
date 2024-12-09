import sys
import pyautogui as pag
import random
import time
import win32api, win32con
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui

import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# Usage
icon_path = resource_path('../img/logo.png')


#keeps program from stopping when cursor hits corner
pag.FAILSAFE = False

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
                #set random movement coordinates
                x = random.randint(500,1000)
                y = random.randint(200,600)

                #set random cursor speed max 7 sec
                duration = random.randint(1,7)

                #move at speed
                pag.moveTo(x, y, duration=duration)
                time.sleep(0.2)

                #set random movement coordinates
                x = random.randint(-500,500)
                y = random.randint(-500,500)

                #jump to location
                win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x, y, 0, 0)

                #set random wait
                rand_time = random.randint(9,15)
                time.sleep(rand_time)

    
    def pause(self):
        self.running = False
        print("AFK stopped")

    
    def start(self):
        self.running = True
        print("AFK started")

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
        self.setWindowIcon(QtGui.QIcon(icon_path))

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