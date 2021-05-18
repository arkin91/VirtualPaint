from cv2 import cv2
import numpy as np

class NewWebcam:
    def __init__(self):
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.cap.set(3, 640)  # width set, width has id 3
        self.cap.set(4, 480)  # height set, width has id 4
        self.colorList = [[37, 88, 41, 255, 114, 255], # 0 - light green
                          [96, 147, 59, 255, 55, 255], # 1 - dark blue
                          [139, 179, 142, 255, 173, 255]] # 2 - pink
        self.colorValues = [[0, 255, 0], #green
                            [204, 0, 0], #dark blue
                            [127, 0, 255]] #pink
        self.myPoints = []
        # self.winname = "TrackBars"
        # self.trackbar_name = ["Hue min", "Hue max",
                            #   "Sat min", "Sat max", "Val min", "Val max"]

    def webcamdisplay(self):
        while True:
            self.success, self.img = self.cap.read()
            self.imgResult = self.img.copy();
            self.newPoints = self.colordetection(self.img, self.colorList, self.colorValues)
            if len(self.newPoints) != 0:
                for newP in self.newPoints:
                    self.myPoints.append(newP)
            if len(self.myPoints) != 0:
                self.drawOnCanvas(self.myPoints, self.colorValues)
            cv2.imshow("Virtual Paint", self.imgResult)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()
    
    def colordetection(self, img, colorList, colorValues):
        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        count = 0
        newPoints = []
        for color in colorList:
            lower = np.array([color[0], color[2], color[4]])
            upper = np.array([color[1], color[3], color[5]])
            mask = cv2.inRange(imgHSV, lower, upper)
            x,y = self.getContours(mask)
            cv2.circle(self.imgResult,(x,y),5,colorValues[count],cv2.FILLED)
            if( x!= 0 and y != 0):#because this loop cycles through all 3 masks, 2 of which will return 0,0.
                newPoints.append([x,y,count])
            count += 1
        return newPoints
            
    def getContours(self, mask):
        contours, heirarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        x, y, w, h = 0,0,0,0
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 200:
                # cv2.drawContours(self.imgResult, cnt, -1, (255, 0, 0), 2)
                perimeter = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.02*perimeter, True)
                x, y, w, h = cv2.boundingRect(approx)
        return x+w//2,y

    def drawOnCanvas(self, myPoints, colorValues):
        for point in myPoints:
            cv2.circle(self.imgResult,(point[0],point[1]),5,colorValues[point[2]],cv2.FILLED)

    # def updateColorList(self, colorList, colorValues):
    #     #use trackbar and allow user to detect color. Make numpy array of those HSV values and use cvtColor to convert it to RGB.
    #     rgbarr, hsvarr = self.inputColorList()
    #     self.colorList.append(hsvarr)
    #     self.colorValues.append(rgbarr)

    #     pass

    # def inputColorList(self):
    #     # default run will be for skin-hues, but user will be able to play around.
    #     self.trackbarwindow()
    #     h_min = cv2.getTrackbarPos(self.trackbar_name[0], self.winname)
    #     h_max = cv2.getTrackbarPos(self.trackbar_name[1], self.winname)
    #     s_min = cv2.getTrackbarPos(self.trackbar_name[2], self.winname)
    #     s_max = cv2.getTrackbarPos(self.trackbar_name[3], self.winname)
    #     v_min = cv2.getTrackbarPos(self.trackbar_name[4], self.winname)
    #     v_max = cv2.getTrackbarPos(self.trackbar_name[5], self.winname)

    #     hsvarr = np.array([h_min, h_max,  s_min, s_max, v_min, v_max])
    #     hsvarr1 = np.array([(h_min+h_max)/2, (s_min+s_max)/2, (v_min+v_max)/2])
    #     rgbarr = cv2.cvtColor(hsvarr1, cv2.COLOR_HSV2BGR)
    #     return rgbarr, hsvarr;
    
    # def trackbarwindow(self):
    #     def empty(a):
    #         pass
    #     cv2.namedWindow(self.winname)
    #     cv2.resizeWindow(self.winname, 640, 240)
    #     cv2.createTrackbar(self.trackbar_name[0], self.winname, 0, 179, empty)
    #     cv2.createTrackbar(self.trackbar_name[1], self.winname, 88, 179, empty)
    #     cv2.createTrackbar(self.trackbar_name[2], self.winname, 41, 255, empty)
    #     cv2.createTrackbar(
    #         self.trackbar_name[3], self.winname, 255, 255, empty)
    #     cv2.createTrackbar(
    #         self.trackbar_name[4], self.winname, 114, 255, empty)
    #     cv2.createTrackbar(
    #         self.trackbar_name[5], self.winname, 255, 255, empty)
