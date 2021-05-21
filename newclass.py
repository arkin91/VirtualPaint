from cv2 import cv2
import numpy as np
from proj1 import VirtualPainter

class ColorUpdate(VirtualPainter):
    def __init__(self):
        VirtualPainter.__init__(self)
        self.winname = "TrackBars"
        self.trackbar_name = ["Hue min", "Hue max",
                              "Sat min", "Sat max", "Val min", "Val max"]

    def updateColors(self):
        #use trackbar and allow user to detect color. Make numpy array of those HSV values and use cvtColor to convert it to RGB.
        bgrarr = []
        hsvarr = []
        self.trackbarwindow()
        while True:   
            self.success, self.img = self.cap.read() 
            cv2.imshow("Webcam Feed", self.img)
            bgrarr, hsvarr = self.getColors()
            self.maskDisplay(hsvarr, self.img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        # show prompt to save the colors, if yes, write to txt files.
        print("Press y/Y to save your detected color")
        if input().lower() == 'y' :
            self.colorList.append(hsvarr)
            self.colorValues.append(bgrarr)
            self.appendColorList(hsvarr)
            self.appendColorList(bgrarr)

    def trackbarwindow(self):
        def empty(a):
            pass
        cv2.namedWindow(self.winname)
        cv2.resizeWindow(self.winname, 640, 240)
        cv2.createTrackbar(self.trackbar_name[0], self.winname, 0, 179, empty)
        cv2.createTrackbar(self.trackbar_name[1], self.winname, 88, 179, empty)
        cv2.createTrackbar(self.trackbar_name[2], self.winname, 41, 255, empty)
        cv2.createTrackbar(
            self.trackbar_name[3], self.winname, 255, 255, empty)
        cv2.createTrackbar(
            self.trackbar_name[4], self.winname, 114, 255, empty)
        cv2.createTrackbar(
            self.trackbar_name[5], self.winname, 255, 255, empty)

    def getColors(self):
        # default run will be for skin-hues, but user will be able to play around.
        h_min = cv2.getTrackbarPos(self.trackbar_name[0], self.winname)
        h_max = cv2.getTrackbarPos(self.trackbar_name[1], self.winname)
        s_min = cv2.getTrackbarPos(self.trackbar_name[2], self.winname)
        s_max = cv2.getTrackbarPos(self.trackbar_name[3], self.winname)
        v_min = cv2.getTrackbarPos(self.trackbar_name[4], self.winname)
        v_max = cv2.getTrackbarPos(self.trackbar_name[5], self.winname)

        hsvarr = np.array([h_min, h_max,  s_min, s_max, v_min, v_max])
        hsvarr1 = np.uint8([[[(h_min+h_max)/2, (s_min+s_max)/2, (v_min+v_max)/2]]])
        bgrarr = cv2.cvtColor(hsvarr1, cv2.COLOR_HSV2BGR)
        return bgrarr, hsvarr;
    
    def maskDisplay(self, hsvarr, img):
        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower = np.array([hsvarr[0], hsvarr[2], hsvarr[4]])
        upper = np.array([hsvarr[1], hsvarr[3], hsvarr[5]])
        mask = cv2.inRange(imgHSV, lower, upper)
        imgresult = cv2.bitwise_and(img, img, mask=mask)
        cv2.imshow("Masked Feed", imgresult)
    
    def appendColorList(self, arr):
        pass

    def appendColorValues(self, arr):
        pass
