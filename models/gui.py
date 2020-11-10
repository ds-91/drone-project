from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton

import sys

class GUI:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = QWidget()
        self.window.setWindowTitle('test window')
        self.window.setGeometry(0, 0, 640, 480)
        self.window.move(60, 15)
        self.b = QPushButton('TEST', parent=self.window)
        self.b.move(60, 15)
        self.b.clicked.connect(self.testButtonPress)

    def show(self):
        self.window.show()

    def testButtonPress(self):
        print('button was pressed!!!')
