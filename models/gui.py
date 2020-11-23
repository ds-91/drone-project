import sys, app, time, cv2, datetime
from pytz import timezone
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from threading import Thread

class GUI:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = QWidget()
        self.layout = QVBoxLayout(self.window)
        self.sub_layout = QHBoxLayout(self.window)
        self.window.setWindowTitle('Remote Drone')
        self.window.setGeometry(0, 0, 640, 480)
        
        # Label that displays the video feed
        self.video_label = QLabel()
        self.pixmap = QPixmap('video_blank.png')
        self.video_label.setPixmap(self.pixmap)
        
        # Button to take a picture
        self.button_capture_image = QPushButton('Take Picture')
        self.button_capture_image.clicked.connect(self.capture_image)

        self.layout.addWidget(self.video_label)
        self.layout.addWidget(self.button_capture_image)
        self.window.setLayout(self.layout)
        
        self.drone = None
        self.output_img = None

        self.layout.addLayout(self.sub_layout)
        self.label = QLabel('Speed: 0')
        self.label_1 = QLabel('Battery: 78')
        self.label_2 = QLabel('Temperature: 88')
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label_1.setAlignment(Qt.AlignCenter)
        self.label_2.setAlignment(Qt.AlignCenter)
        self.sub_layout.addWidget(self.label)
        self.sub_layout.addWidget(self.label_1)
        self.sub_layout.addWidget(self.label_2)
        

    def show_video_feed(self):
        # wait 10 seconds to make sure feed starts before capturing
        # otherwise it fails until app restarted
        print('sleeping for 5 sec')
        time.sleep(5)
        cap = cv2.VideoCapture('udp://0.0.0.0:11111?overrun_nonfatal=1&fifo_size=50000000', cv2.CAP_FFMPEG)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 0)
        if not cap.isOpened():
            print('cap not opened!!')
            exit(-1)

        while True:
            ret, frame = cap.read()

            if not ret:
                print('EMPTY FRAME')
                break

            # try to show frame 'image' in pixmap
            img = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888).rgbSwapped()
            # scale image smaller
            img.scaledToWidth(640, QtCore.Qt.SmoothTransformation)
            img.scaledToHeight(480, QtCore.Qt.SmoothTransformation)
            self.output_img = img.scaled(640, 480, QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation)
            self.video_label.setPixmap(QPixmap.fromImage(self.output_img))
            self.video_label.update()

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()


    def show(self):
        self.window.show()


    def capture_image(self):
        tz = timezone('US/Eastern')
        ts = datetime.datetime.now(tz)

        if self.output_img:
            self.output_img.save(f'{ts}.png')
            print('took a picture!')
        else:
            print('video capture is not open!')


    def set_self_drone(self, drone):
        self.drone = drone
