from cv2 import cv2
import numpy as np
from numpy.core.fromnumeric import size

class VirtualPainter:
    def __init__(self):
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.cap.set(3, 640)  # width set, width has id 3
        self.cap.set(4, 480)  # height set, width has id 4
        self.colorList = self.setcolorList()
        self.colorValues = self.setcolorValues()
        self.myPoints = []
        
    def setcolorList(self):
        colorList = []
        with open("colorList.txt") as file:
            for line in file:
                line = line.strip()
                colorList.append(line.split(" "))
        for i in range(0, len(colorList)):
            colorList[i] = list(map(int, colorList[i]))
        return colorList

    def setcolorValues(self):
        colorValues = []
        with open("colorValues.txt") as file:
            for line in file:
                line = line.strip()
                colorValues.append(line.split(" "))
        for i in range(0, len(colorValues)):
            colorValues[i] = list(map(int, colorValues[i]))
        return colorValues

    def diaplayPaint(self):
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
    
