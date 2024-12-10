import sys
import pyautogui as pag
import random
import time
import win32api, win32con
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui

#keeps program from stopping when cursor hits corner
pag.FAILSAFE = False

class AFKEngine(QObject):

    def __init__(self):
        super().__init__()
        self.running = False
        self.advanced_mode = False
        self.gaming_mode = False

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
                
                #advanced mode and sub-modes
                if self.advanced_mode:
                    print("Advanced mode activated")
                    if self.gaming_mode:
                        #move wasd equal amounts
                        print("Gaming mode running")

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
    
    def toggle_advanced(self,checked,):
        if checked:
            self.advanced_mode = True
        else:
            self.advanced_mode = False  

    def toggle_gaming(self,checked,):
        if checked:
            self.gaming_mode = True
        else:
            self.gaming_mode = False  
            



class GUIWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mouse Mover")
        self.setWindowIcon(QtGui.QIcon('img\logo.png'))

        #create main label
        lbl = QLabel()
        lbl.setText("Welcome to Mouse Mover! Click the button to toggle automatic mouse moving.")

        #create toggling buttton 
        self.button = QPushButton(text="START Mouse Movement", parent=self)
        self.button.setCheckable(True)
        #connect button to toggling text func
        self.button.clicked.connect(self.toggle_button_text)

        #create advanced settings checkbox
        self.advanced_checkbox = QCheckBox(text= "Advanced Settings")
        self.advanced_checkbox.setCheckable(True)
        self.advanced_checkbox.clicked.connect(self.toggle_advanced_settings_vis)

        # create layout for adv settings
        self.advanced_layout = QGridLayout()
        self.advanced_widget = QWidget()
        self.advanced_widget.setVisible(False)
        

        # Adv settings sub widgets
        self.gaming_checkbox = QCheckBox(text= "Gaming mode")
        self.gaming_checkbox.setCheckable(True)
        self.advanced_layout.addWidget(self.gaming_checkbox)
        self.advanced_widget.setLayout(self.advanced_layout)

        # create main layout
        layout = QVBoxLayout()
        layout.addWidget(lbl)
        layout.addWidget(self.button)
        layout.addWidget(self.advanced_checkbox)
        layout.addWidget(self.advanced_widget)

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
        self.advanced_checkbox.clicked.connect(self.worker.toggle_advanced)
        self.gaming_checkbox.clicked.connect(self.worker.toggle_gaming)

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

    def toggle_advanced_settings_vis(self,s):
        if self.advanced_checkbox.isChecked():
            self.advanced_widget.setVisible(True)
        else:
            self.advanced_widget.setVisible(False)
            
#setup main window, show window, and execute app            
app = QApplication(sys.argv)
window = GUIWindow()
window.show()
app.exec()