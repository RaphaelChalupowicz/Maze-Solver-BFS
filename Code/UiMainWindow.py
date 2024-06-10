import threading

from PyQt5 import QtWidgets, QtGui, QtCore
import cv2
import time
import tkinter as tk
from tkinter import filedialog
from Point import *
from BFSPathFinder import *
from ThreadClass import *

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtMultimedia import QCameraInfo
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QHBoxLayout, QWidget, QVBoxLayout


class UiMainWindow(object):
    def setupUi(self, mainWindow):
        # region -Setup All UI-

        # region -MainWindow UI-
        mainWindow.setObjectName("MainWindow")
        mainWindow.resize(800, 600)
        mainWindow.setStyleSheet("background-color: rgb(90, 90, 90);")  # BG COLOR!
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        # endregion

        # region -Create a vertical layout for the central widget & Some Spaces For the separation of the UI's-
        layout = QVBoxLayout(self.centralwidget)
        layout.setAlignment(QtCore.Qt.AlignCenter)  # Center-align the layout

        layout2 = QHBoxLayout()  # """"""top buttons layout
        layout3 = QHBoxLayout()  # """"""main display layout

        # Create a spacer to push layout2 to the top-right
        spacer = QWidget()
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        
        spacer2 = QWidget()  # """"""space between top and main display layout's
        spacer2.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        spacer3 = QWidget()  # """"""righter space inside main display layout
        spacer3.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        spacer4 = QWidget()  # """"""lefter space inside main display layout
        spacer4.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.centralwidget.setObjectName("centralwidget")

        # endregion
        
        # region -Camera List UI-
        self.online_cam = QCameraInfo.availableCameras() # setting an array of all available cameras connected!

        self.camlist = QtWidgets.QComboBox(self.centralwidget)
        self.camlist.setGeometry(QtCore.QRect(660, 10, 100, 21))
        self.camlist.setMinimumSize(QtCore.QSize(200, 0))
        self.camlist.setMaximumSize(QtCore.QSize(1000, 16777215))
        self.camlist.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.camlist.setObjectName("camlist")

        self.camlist.addItems([c.description() for c in self.online_cam]) #adding all availeble camera's to the camera list ui!
        # endregion

        # region -Camera Text UI-
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(420, 10, 231, 21))
        self.label.setMinimumSize(QtCore.QSize(70, 0))
        self.label.setMaximumSize(QtCore.QSize(70, 16777215))
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        # endregion
       
        # region -Button Start UI-
        self.btn_start = QtWidgets.QPushButton(self.centralwidget)
        self.btn_start.setGeometry(QtCore.QRect(540, 10, 56, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_start.setFont(font)
        self.btn_start.setStyleSheet("background-color: rgb(40, 200, 40);")
        self.btn_start.setObjectName("btn_start")
        self.btn_start.setEnabled(True)
        self.btn_start.clicked.connect(self.startWebCam)  # Press Start Button
        # endregion

        # region -Button Stop UI-
        self.btn_stop = QtWidgets.QPushButton(self.centralwidget)
        self.btn_stop.setGeometry(QtCore.QRect(470, 10, 56, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_stop.setFont(font)
        self.btn_stop.setStyleSheet("background-color: rgb(200, 40, 40);")
        self.btn_stop.setObjectName("btn_stop")
        self.btn_stop.setEnabled(False)
        self.btn_stop.clicked.connect(self.stopWebcam)  # Press Stop Button
        # endregion

        # region -Button Capture Maze UI-
        self.btn_capture = QtWidgets.QPushButton(self.centralwidget)
        self.btn_capture.setGeometry(QtCore.QRect(400, 10, 56, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_capture.setFont(font)
        self.btn_capture.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.btn_capture.setObjectName("btn_capture")
        self.btn_capture.setEnabled(False)
        self.btn_capture.clicked.connect(self.captureClickButton)
        # endregion

        # region -Button Select Image From File UI-
        self.btn_select_img_file = QtWidgets.QPushButton(self.centralwidget)
        self.btn_select_img_file.setGeometry(QtCore.QRect(400, 10, 56, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_select_img_file.setFont(font)
        self.btn_select_img_file.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.btn_select_img_file.setObjectName("btn_selectImgFile")
        self.btn_select_img_file.clicked.connect(self.selectImage)
        # endregion

        # region -Add All Created UI to Widget & set size-
        self.btn_capture.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        layout2.addWidget(self.btn_capture)  # """"""
        self.btn_select_img_file.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        layout2.addWidget(self.btn_select_img_file)  # """"""
        self.btn_stop.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        layout2.addWidget(self.btn_stop)  # """"""
        self.btn_start.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        layout2.addWidget(self.btn_start)  # """"""
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        layout2.addWidget(self.label)  # """"""
        self.camlist.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        layout2.addWidget(self.camlist)  # """"""

        layout.addLayout(layout2)  # """"""
        layout.addWidget(spacer2)
        # endregion

        # region -Preveiw Camera Live UI-
        self.disp_main = QtWidgets.QLabel(self.centralwidget)
        layout3.addWidget(self.disp_main)
        self.disp_main.setMinimumSize(QtCore.QSize(581, 581))  #
        self.disp_main.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.disp_main.setStyleSheet("background-color: rgb(246, 247, 247);")
        self.disp_main.setAlignment(QtCore.Qt.AlignCenter)
        self.disp_main.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)  # !#!#!#!#!#!
        self.disp_main.setObjectName("disp_main")
        layout.addLayout(layout3)
        # endregion

        # region -More UI-
        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 18))
        self.menubar.setObjectName("menubar")
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)
        # endregion
        
        # region -Set the size policy of the layout to Expanding-
        layout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        # endregion

        self.retranslateUi(mainWindow)  # Call set text to specific ui elements
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

        # endregion

    def retranslateUi(self, mainWindow):
        # region -Translate & Set all text inside UI-
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "camera: "))
        self.btn_start.setText(_translate("MainWindow", "Start"))
        self.disp_main.setText(_translate("MainWindow", "Main Source"))
        self.btn_stop.setText(_translate("MainWindow", "Stop"))
        self.btn_capture.setText(_translate("MainWindow", "Capture Maze"))
        self.btn_select_img_file.setText(_translate("MainWindow", "Select Image File"))
        # endregion

    def opencvEmit(self, image):
        # QPixmap format
        original = self.formatCvtQt(image)
        # Numpy Array format
        self.CopyImage = image[0:719, 0:1278]
        
        self.disp_main.setPixmap(original)
        self.disp_main.setScaledContents(True)

    def formatCvtQt(self, image):
        rgb_img = cv2.cvtColor(src=image,code=cv2.COLOR_BGR2RGB)
        rgb_img = cv2.rectangle(rgb_img, pt1=(0,0), pt2=(1278,719), color=(0,255,255), thickness=2)

        h, w, ch = rgb_img.shape
        bytes_per_line = ch * w
        cvt2QtFormat = QImage(rgb_img.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(cvt2QtFormat)

        return pixmap

    def startWebCam(self):
        try:
            print("HELLO WORLD!  " + self.camlist.currentText())
            self.btn_stop.setEnabled(True)
            self.btn_start.setEnabled(False)
            self.camlist.setEnabled(False)
            self.btn_select_img_file.setEnabled(False)
            self.btn_capture.setEnabled(True)

            camIndex = self.camlist.currentIndex()
        
            # Opencv QThread
            self.Worker1_Opencv = ThreadClass(camIndex)
            self.Worker1_Opencv.ImageUpdate.connect(self.opencvEmit)
            self.Worker1_Opencv.start()

        except Exception as error:
            pass

    def stopWebcam(self):
        self.btn_start.setEnabled(True)
        self.camlist.setEnabled(True)
        self.btn_select_img_file.setEnabled(True)
        self.btn_stop.setEnabled(False)
        self.btn_capture.setEnabled(False)
        self.disp_main.setPixmap(QtGui.QPixmap()) #clears the main display off camera view!!
        self.disp_main.setText(QtCore.QCoreApplication.translate("MainWindow", "Main Source"))
        self.Worker1_Opencv.stop()

    def resizeImage(self, img):
        r = 0.65
        hd, wd = img.shape[:2]
        return cv2.resize(img, (1920, 1080))  #"""(int(hd*2), int(r*wd*2))"""

    def getPointsAndFindPath(self, event, pX, pY, flags, param):

        global img, start, end, pointCounter
        selectedPointSize = 2

        if(pointCounter == 2):
            pointCounter = 0

        if event == cv2.EVENT_LBUTTONUP:        # this event accures only after the left mouse button is released.
            
            if pointCounter == 0:  # if this is the first registered point it will set the location selected to the start point
                
                cv2.rectangle(img, (pX - selectedPointSize, pY - selectedPointSize), (pX + selectedPointSize, pY + selectedPointSize), (0, 0, 255), -1)  # Creates the red starting point
                
                start = Point(pX, pY)  # sets the starting position and saves it

                print("start = ", start.x, start.y)

                pointCounter += 1

            elif pointCounter == 1:          # if this is the seccond registered point it will set the location selected to the end point
                
                cv2.rectangle(img, (pX - selectedPointSize, pY - selectedPointSize), (pX + selectedPointSize, pY + selectedPointSize), (0, 200, 50), -1) # Creates the green ending point
                
                end = Point(pX, pY)  # sets the finishing position and saves it
                
                print("end = ", end.x, end.y)
                
                pointCounter += 1
                
                t2 = time.time()

                path_finder = BFSPathFinder(img, h, w)  # init BFS search
                path_finder.find_path(start, end)  # starts BFS search
            
                img = self.resizeImage(img)
                print(time.time()-t2)

    def displayImage(self):
        print("Here!1")
        global img, pointCounter
        pointCounter = 0
        times = 0
        # print(img)

        cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
        cv2.imshow("Image", img)

        print("Here!3")

        cv2.setMouseCallback('Image', self.getPointsAndFindPath)
        while True:
            cv2.imshow("Image", img)
            cv2.waitKey(1)
            key = cv2.waitKey(1)
            if cv2.getWindowProperty("Image", cv2.WND_PROP_VISIBLE) < 1:
                print("ALL WINDOWS ARE CLOSED")
                cv2.destroyAllWindows()
                break
            """if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            elif cv2.waitKey(1) & times == 0:
                times == 1
            elif times == 1:
                break
            elif cv2.getWindowProperty('Image', cv2.WND_PROP_VISIBLE) < 1: 
                print("ALL WINDOWS ARE CLOSED") """


    def takeSnapshot(self, filename):
        global h,w, img

        # if filename != None:
        try:
            print(filename)

            img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
            img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)  # Was "cv2.ADAPTIVE_THRESH_MEAN_C"

            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            #plt.show(img)

            h, w = img.shape[:2]
            print("Select start and end points : ")
            
            self.displayImage()

            """print("Here!")
            mazeFileThread = threading.Thread(target=self.displayImage, args=())
            mazeFileThread.daemon = True
            mazeFileThread.start()"""
        except:
            print("Error")
    
    def captureClickButton(self):
        crops = self.Worker1_Opencv.capture() #TO SAVE CROPED Version Of Maze
        print(crops)
            
        try:
            self.takeSnapshot(crops[0]['path'])
        except IndexError:
            print("IndexError: list index out of range")

    def selectImage(self):
        filename = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("png files","*.png"),("all files","*.*")))

        try:
           print(filename)
           self.takeSnapshot(filename)
        except:
            print("File is empty")




