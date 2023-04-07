import sys
import cv2
import numpy as np
#import PySide6
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

from camera import Camera
from camera_calibration import CameraCalibration

# from gimbal_uart_protocol import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        self.setGeometry(100, 100, 1000, 600)
        self.setStyleSheet("background-color: black;")

        self.menu1 = QPushButton("主菜单", self)
        palette = QPalette()
        palette.setColor(QPalette.ButtonText, QColor(255,128,0))
        self.menu1.setPalette(palette)
        font = QFont("Arial", 15, QFont.Bold)
        self.menu1.setFont(font)
        self.menu1.setStyleSheet("background-color: black")
        self.menu1.setGeometry(200, 0, 200, 35)
        self.menu1.clicked.connect(self.menuClicked1)

        self.menu2 = QPushButton("直播页面", self)
        palette = QPalette()
        palette.setColor(QPalette.ButtonText, QColor(255,128,0))
        self.menu2.setPalette(palette)
        font = QFont("Arial", 15, QFont.Bold)
        self.menu2.setFont(font)
        self.menu2.setStyleSheet("background-color: black")
        self.menu2.setGeometry(405, 0, 200, 40)
        self.menu2.clicked.connect(self.menuClicked1)

        self.menu3 = QPushButton("数据统计", self)
        palette = QPalette()
        palette.setColor(QPalette.ButtonText, QColor(255,128,0))
        self.menu3.setPalette(palette)
        font = QFont("Arial", 15, QFont.Bold)
        self.menu3.setFont(font)
        self.menu3.setStyleSheet("background-color: black")
        self.menu3.setGeometry(610, 0, 200, 35)
        self.menu3.clicked.connect(self.menuClicked1)

        self.label0 = QLabel("比分", self)
        self.label0.setGeometry(50, 50, 230, 30)
        self.label0.setStyleSheet("color: orange")
        self.label0.setAlignment(Qt.AlignCenter)
        font = QFont("Arial", 20, QFont.Bold)
        self.label0.setFont(font)

        global score1
        score1 = 0
        self.label1 = QLabel(self)
        self.label1.setText(str(score1))
        self.label1.setGeometry(50, 80, 100, 30)
        self.label1.setStyleSheet("color: orange")
        self.label1.setAlignment(Qt.AlignCenter)
        font = QFont("Arial", 20, QFont.Bold)
        self.label1.setFont(font)

        self.colon1 = QLabel(":", self)
        self.colon1.setGeometry(160, 80, 10, 30)
        self.colon1.setStyleSheet("color: orange")
        self.colon1.setAlignment(Qt.AlignCenter)
        font = QFont("Arial", 20, QFont.Bold)
        self.colon1.setFont(font)

        global score2
        score2 = 0
        self.label2 = QLabel(self)
        self.label2.setText(str(score2))
        self.label2.setGeometry(180, 80, 100, 30)
        self.label2.setStyleSheet("color: orange")
        self.label2.setAlignment(Qt.AlignCenter)
        font = QFont("Arial", 20, QFont.Bold)
        self.label2.setFont(font)
	
        self.image_label = QLabel(self)
        self.image_label.setGeometry(350, 45, 600, 350)
        self.camera = Camera()
		# # 初始相机
        self.camera.init_camera()
        self.capture = self.camera.get_video_capture()
        self.timerV = QTimer(self)
        self.timerV.timeout.connect(self.loadImage)
        self.timerV.start(int(1000 / self.camera.config['fps']))
        # self.timerV.start(1000)
        
        

        # self.imageLabel = QLabel(self)
        # self.imageLabel.setGeometry(350, 45, 600, 350)
        # self.imageLabel.setAlignment(Qt.AlignCenter)
        # self.loadImage(r"D:\QTworks\untitled\3.jpg")
        

        self.refreshLabel = QLabel(self)
        self.refreshLabel.setGeometry
        self.refreshLabel.setAlignment(Qt.AlignCenter)
        #self.loadImage(r"D:\QTworks\untitled\refresh.jpg")

        self.myButton1 = QPushButton("左侧进1分球", self)
        palette = QPalette()
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        self.myButton1.setPalette(palette)
        font = QFont("Arial", 10, QFont.Bold)
        self.myButton1.setFont(font)
        self.myButton1.setStyleSheet("background-color: grey")
        self.myButton1.setGeometry(50, 120, 100, 35)
        self.myButton1.clicked.connect(self.onButtonClicked1)

        self.myButton2 = QPushButton("右侧进1分球", self)
        palette = QPalette()
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        self.myButton2.setPalette(palette)
        font = QFont("Arial", 10, QFont.Bold)
        self.myButton2.setFont(font)
        self.myButton2.setStyleSheet("background-color: grey")
        self.myButton2.setGeometry(180, 120, 100, 35)
        self.myButton2.clicked.connect(self.onButtonClicked2)

        self.myButton3 = QPushButton("左侧进2分球", self)
        palette = QPalette()
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        self.myButton3.setPalette(palette)
        font = QFont("Arial", 10, QFont.Bold)
        self.myButton3.setFont(font)
        self.myButton3.setStyleSheet("background-color: grey")
        self.myButton3.setGeometry(50, 165, 100, 35)
        self.myButton3.clicked.connect(self.onButtonClicked3)

        self.myButton4 = QPushButton("右侧进2分球", self)
        palette = QPalette()
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        self.myButton4.setPalette(palette)
        font = QFont("Arial", 10, QFont.Bold)
        self.myButton4.setFont(font)
        self.myButton4.setStyleSheet("background-color: grey")
        self.myButton4.setGeometry(180, 165, 100, 35)
        self.myButton4.clicked.connect(self.onButtonClicked4)

        self.myButton5 = QPushButton("左侧进3分球", self)
        palette = QPalette()
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        self.myButton5.setPalette(palette)
        font = QFont("Arial", 10, QFont.Bold)
        self.myButton5.setFont(font)
        self.myButton5.setStyleSheet("background-color: grey")
        self.myButton5.setGeometry(50, 210, 100, 35)
        self.myButton5.clicked.connect(self.onButtonClicked5)

        self.myButton6 = QPushButton("右侧进3分球", self)
        palette = QPalette()
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        self.myButton6.setPalette(palette)
        font = QFont("Arial", 10, QFont.Bold)
        self.myButton6.setFont(font)
        self.myButton6.setStyleSheet("background-color: grey")
        self.myButton6.setGeometry(180, 210, 100, 35)
        self.myButton6.clicked.connect(self.onButtonClicked6)

        self.myButton7 = QPushButton("撤销", self)
        palette = QPalette()
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        self.myButton7.setPalette(palette)
        font = QFont("Arial", 10, QFont.Bold)
        self.myButton7.setFont(font)
        self.myButton7.setStyleSheet("background-color: red")
        self.myButton7.setGeometry(50, 255, 230, 35)
        self.myButton7.clicked.connect(self.onButtonClicked7)

        self.label3 = QLabel("时间", self)
        self.label3.setGeometry(50, 310, 230, 30)
        self.label3.setStyleSheet("color: orange")
        self.label3.setAlignment(Qt.AlignCenter)
        font = QFont("Arial", 20, QFont.Bold)
        self.label3.setFont(font)

        self.timerM = QTimer(self)
        self.labelTimeM = QLabel(self)
        self.labelTimeM.setText(str(0))
        self.labelTimeM.setGeometry(50, 350, 100, 30)
        self.labelTimeM.setStyleSheet("color: orange")
        self.labelTimeM.setAlignment(Qt.AlignCenter)
        font = QFont("Arial", 20, QFont.Bold)
        self.labelTimeM.setFont(font)

        self.colon2 = QLabel(":", self)
        self.colon2.setGeometry(160, 350, 10, 30)
        self.colon2.setStyleSheet("color: orange")
        self.colon2.setAlignment(Qt.AlignCenter)
        font = QFont("Arial", 20, QFont.Bold)
        self.colon2.setFont(font)

        self.timerS = QTimer(self)
        self.timerS.timeout.connect(self.updateLabelS)
        self.timerS.start(1000)
        self.labelTimeS = QLabel(self)
        self.labelTimeS.setText(str(0))
        self.labelTimeS.setGeometry(180, 350, 100, 30)
        self.labelTimeS.setStyleSheet("color: orange")
        self.labelTimeS.setAlignment(Qt.AlignCenter)
        font = QFont("Arial", 20, QFont.Bold)
        self.labelTimeS.setFont(font)

        self.myButton8 = QPushButton("暂停", self)
        palette = QPalette()
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        self.myButton8.setPalette(palette)
        font = QFont("Arial", 10, QFont.Bold)
        self.myButton8.setFont(font)
        self.myButton8.setStyleSheet("background-color: red")
        self.myButton8.setGeometry(50, 390, 230, 35)
        self.myButton8.clicked.connect(self.onButtonClicked8)

        self.label4 = QLabel("手动控制云台", self)
        self.label4.setGeometry(50, 455, 230, 30)
        self.label4.setStyleSheet("color: orange")
        self.label4.setAlignment(Qt.AlignCenter)
        font = QFont("Arial", 20, QFont.Bold)
        self.label4.setFont(font)

        self.myButton9 = QPushButton("右旋5°", self)
        palette = QPalette()
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        self.myButton9.setPalette(palette)
        font = QFont("Arial", 10, QFont.Bold)
        self.myButton9.setFont(font)
        self.myButton9.setStyleSheet("background-color: grey")
        self.myButton9.setGeometry(180, 495, 100, 35)
        self.myButton9.clicked.connect(self.onButtonClicked9)

        self.myButton10 = QPushButton("左旋5°", self)
        palette = QPalette()
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        self.myButton10.setPalette(palette)
        font = QFont("Arial", 10, QFont.Bold)
        self.myButton10.setFont(font)
        self.myButton10.setStyleSheet("background-color: grey")
        self.myButton10.setGeometry(50, 495, 100, 35)
        self.myButton10.clicked.connect(self.onButtonClicked10)

        self.myButton11 = QPushButton("右旋10°", self)
        palette = QPalette()
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        self.myButton11.setPalette(palette)
        font = QFont("Arial", 10, QFont.Bold)
        self.myButton11.setFont(font)
        self.myButton11.setStyleSheet("background-color: grey")
        self.myButton11.setGeometry(180, 540, 100, 35)
        self.myButton11.clicked.connect(self.onButtonClicked9)

        self.myButton12 = QPushButton("左旋10°", self)
        palette = QPalette()
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        self.myButton12.setPalette(palette)
        font = QFont("Arial", 10, QFont.Bold)
        self.myButton12.setFont(font)
        self.myButton12.setStyleSheet("background-color: grey")
        self.myButton12.setGeometry(50, 540, 100, 35)
        self.myButton12.clicked.connect(self.onButtonClicked10)

        self.refreshButton = QPushButton(self)
        #self.refreshButton.setStyleSheet("background-image: url(D:/QTworks/untitled/refresh.jpg);")
        self.refreshButton.setGeometry(350, 360, 20, 20)
        icon = QIcon("D:/QTworks/untitled/refresh.jpg")
        self.refreshButton.setIcon(icon)
        #self.refreshButton.clicked.connect(self.onButtonClicked3)

        self.label5 = QLabel("小窗操作", self)
        self.label5.setGeometry(820, 410, 120, 40)
        self.label5.setStyleSheet("color: orange")
        self.label5.setAlignment(Qt.AlignCenter)
        font = QFont("Arial", 20, QFont.Bold)
        self.label5.setFont(font)

        self.myButton8 = QPushButton("-5s慢放", self)
        palette = QPalette()
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        self.myButton8.setPalette(palette)
        font = QFont("Arial", 10, QFont.Bold)
        self.myButton8.setFont(font)
        self.myButton8.setStyleSheet("background-color: blue")
        self.myButton8.setGeometry(550, 525, 180, 35)
        self.myButton8.clicked.connect(self.onButtonClicked11)

        self.myButton9 = QPushButton("-10s慢放", self)
        palette = QPalette()
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        self.myButton9.setPalette(palette)
        font = QFont("Arial", 10, QFont.Bold)
        self.myButton9.setFont(font)
        self.myButton9.setStyleSheet("background-color: blue")
        self.myButton9.setGeometry(550, 480, 180, 35)
        self.myButton9.clicked.connect(self.onButtonClicked11)

        self.myButton9 = QPushButton("放大", self)
        palette = QPalette()
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        self.myButton9.setPalette(palette)
        font = QFont("Arial", 10, QFont.Bold)
        self.myButton9.setFont(font)
        self.myButton9.setStyleSheet("background-color: blue")
        self.myButton9.setGeometry(750, 480, 180, 35)
        self.myButton9.clicked.connect(self.onButtonClicked11)

        self.myButton9 = QPushButton("设为精彩瞬间", self)
        palette = QPalette()
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        self.myButton9.setPalette(palette)
        font = QFont("Arial", 10, QFont.Bold)
        self.myButton9.setFont(font)
        self.myButton9.setStyleSheet("background-color: blue")
        self.myButton9.setGeometry(750, 525, 180, 35)
        self.myButton9.clicked.connect(self.onButtonClicked11)

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.setPen(QPen(QColor(255, 128, 0), 3, Qt.SolidLine))
        painter.drawLine(405, 41, 605, 41)

        painter.setPen(QPen(QColor(255, 255, 255), 1, Qt.SolidLine))
        painter.drawRect(35, 45, 260, 255)

        painter.setPen(QPen(QColor(255, 255, 255), 1, Qt.SolidLine))
        painter.drawRect(35, 305, 260, 140)

        painter.setPen(QPen(QColor(255, 255, 255), 1, Qt.SolidLine))
        painter.drawRect(35, 450, 260, 140)

        painter.setPen(QPen(QColor(255, 255, 255), 3, Qt.SolidLine))
        painter.drawLine(350, 420, 950, 420)
	
    def display_video_stream(self, frame=None):
        """Read frame from camera and repaint QLabel widget.
        """
        if frame is None:
            _, frame = self.capture.read()

        _, frame = self.capture.read()
        print("1")
        # if self.is_rm_img_distor:
        #     # 去除图像畸变
        #     frame = self.camera.remove_distortion(frame)
        self.image = np.copy(frame) # 更新图像信息
        self.image_label.update(self.image)

    def updateLabelS(self):
        self.labelTimeS.setText(str(int(self.labelTimeS.text()) + 1))
        if self.labelTimeS.text() == '60':
            self.labelTimeM.setText(str(int(self.labelTimeM.text()) + 1))
            self.labelTimeS.setText(str(0))

    def onButtonClicked1(self):
        global score1 
        global score2
        global scoreTemp1
        global scoreTemp2
        scoreTemp1 = score1
        scoreTemp2 = score2
        score1 += 1
        self.label1.setText(str(score1))

    def onButtonClicked2(self):
        global score1 
        global score2
        global scoreTemp1
        global scoreTemp2
        scoreTemp1 = score1
        scoreTemp2 = score2
        score2 += 1
        self.label2.setText(str(score2))

    def onButtonClicked3(self):
        global score1 
        global score2
        global scoreTemp1
        global scoreTemp2
        scoreTemp1 = score1
        scoreTemp2 = score2
        score1 += 2
        self.label1.setText(str(score1))

    def onButtonClicked4(self):
        global score1 
        global score2
        global scoreTemp1
        global scoreTemp2
        scoreTemp1 = score1
        scoreTemp2 = score2
        score2 += 2
        self.label2.setText(str(score2))

    def onButtonClicked5(self):
        global score1 
        global score2
        global scoreTemp1
        global scoreTemp2
        scoreTemp1 = score1
        scoreTemp2 = score2
        score1 += 3
        self.label1.setText(str(score1))

    def onButtonClicked6(self):
        global score1 
        global score2
        global scoreTemp1
        global scoreTemp2
        scoreTemp1 = score1
        scoreTemp2 = score2
        score2 += 3
        self.label2.setText(str(score2))

    def onButtonClicked7(self):
        global score1
        global score2
        global scoreTemp1
        global scoreTemp2
        self.label1.setText(str(scoreTemp1))
        self.label2.setText(str(scoreTemp2))
        score1 = scoreTemp1
        score2 = scoreTemp2

    def onButtonClicked8(self):
        if self.timerS.isActive():
            self.timerS.stop()
            self.myButton8.setText("继续")
        else:
            self.timerS.start()
            self.myButton8.setText("暂停")
    
    def onButtonClicked9(self):
        print("")

    def onButtonClicked10(self):
        print("")
    
    def onButtonClicked11(self):
        print("")

    def menuClicked1(self):
        print("")
    
    def loadImage(self):
            _, cv_canvas = self.capture.read()
            # cv_canvas = np.copy(frame)

            height, width, channel = cv_canvas.shape
            self.img_h = height
            self.img_w = width

            canvas_rgb = cv2.cvtColor(cv_canvas, cv2.COLOR_BGR2RGB)
            # 转换为QImage
            bytes_per_line = 3 * self.img_w
            self.q_img = QImage(canvas_rgb.data, self.img_w, self.img_h, bytes_per_line, QImage.Format.Format_RGB888)

            # pixmap = QPixmap(r"D:\cat200x192.jpg")
            pixmap = QPixmap(self.q_img)
            labelSize = self.image_label.size()
            pixmapSize = pixmap.size()

            # 计算图片和标签的宽高比
            labelRatio = labelSize.width() / labelSize.height()
            pixmapRatio = pixmapSize.width() / pixmapSize.height()

            if pixmapRatio > labelRatio:  # 按宽度进行缩小
                newWidth = labelSize.width()
                newHeight = int(newWidth / pixmapRatio)
            else:  # 按高度进行缩小
                newHeight = labelSize.height()
                newWidth = int(newHeight * pixmapRatio)

            # 缩小图片
            scaledPixmap = pixmap.scaled(newWidth, newHeight, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            # 设置缩小后的图片为标签的背景
            self.image_label.setPixmap(scaledPixmap)
            self.image_label.setScaledContents(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
