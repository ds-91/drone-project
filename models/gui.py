import sys, app, time, cv2
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QThread, QRunnable, QThreadPool
from threading import Thread

class GUI:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = QWidget()
        self.layout = QVBoxLayout(self.window)
        self.window.setWindowTitle('test window')
        self.window.setGeometry(0, 0, 640, 480)
        
        self.label = QLabel()
        self.pixmap = QPixmap('test.png')
        self.label.setPixmap(self.pixmap)

        self.layout.addWidget(self.label)
        self.window.setLayout(self.layout)

        self.drone = None
        
        #thread = Thread(target = self.show_video_feed)
        #thread.start()

    def show_video_feed(self):
        # wait 10 seconds to make sure feed starts before capturing
        # otherwise it fails until app restarted
        print('sleeping for 10 sec')
        time.sleep(10)
        cap = cv2.VideoCapture('udp://0.0.0.0:11111', cv2.CAP_FFMPEG)
        if not cap.isOpened():
            print('cap not opened!!')
            exit(-1)

        while True:
            ret, frame = cap.read()

            if not ret:
                print('EMPTY FRAME')
                break

            #cv2.imshow('frame', frame)

            # try to show frame 'image' in pixmap
            img = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888).rgbSwapped()
            self.label.setPixmap(QPixmap.fromImage(img))
            self.label.update()

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()

    def read(self):
        cv2.imshow('frame', self.frame)
        cv2.waitKey(0)

    def show(self):
        self.window.show()


    def testButtonPress(self):
        pass


    def set_self_drone(self, drone):
        self.drone = drone
