import os
from PyQt5 import QtCore
import cv2
import numpy as np
import torch


class ThreadClass(QtCore.QThread):  # Define a thread class for background processing
    ImageUpdate = QtCore.pyqtSignal(object)  # Define a signal for updating the image

    def __init__(self, camIndex):
        super(ThreadClass, self).__init__()
        self.stopped = False
        self.Capture = None
        self.camIndex = camIndex

    def run(self):  # Method representing the thread's activity
        print(self.camIndex)
        global results
        self.Capture = cv2.VideoCapture(self.camIndex, cv2.CAP_DSHOW)  # Open video capture for the specified camera index
        self.Capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Set frame height and width
        self.Capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Set frame height and width
        
        self.ThreadActive = True
        print(self.ThreadActive)

        # Load the model for object detection
        model = torch.hub.load(os.getcwd(), 'custom', source='local', path='best.pt', force_reload=True) ######## torch.hub.load(os.getcwd(), 'custom', source='local', path='best.pt', force_reload=True) || torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt', force_reload=True)
        # device = 'cuda' if torch.cuda.is_available() else 'cpu'

        while self.ThreadActive: 
            try:
                ret, frame_cap = self.Capture.read()  # Read a frame from the camera
                results = model(frame_cap,size=640)  # Perform object detection
                if ret:
                    assert not isinstance(results, type(None))  # Assert results are not None
                    self.ImageUpdate.emit(np.squeeze(results.render()))  # Emit the image for update
            except AttributeError:
                pass

    def stop(self):  # Method to stop the thread
        self.stopped = True  # Set the stopped flag to True
        print(self.Capture)
        self.Capture.release()  # Release the video capture object
        
        self.ThreadActive = False  # Set the thread activity flag to False
        self.terminate()  # Terminate the thread
        self.quit()  # Quit the thread
        
    def capture(self):  # Method to capture the image
        crops = results.crop(save=True)  # Crop the image and save
        return crops  # Return cropped image
