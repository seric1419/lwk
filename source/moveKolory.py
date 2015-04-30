####################################
#####Created by Adrian Kozica######
##################################

import cv2
import numpy as np
import random
from setting import WINDOW_NAME_1, MAIN_WINDOW_NAME, COLORS, CIRCLE_SIZE

camera_feed = cv2.VideoCapture(0)

def nothing():
    pass

class Circle:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.radius = r

def getPlayerCircle(player):
    mask = cv2.inRange(hsv, player.lower_color, player.upper_color)
    mask = cv2.erode(mask, element, iterations = 2)
    mask = cv2.dilate(mask, element2, iterations = 2)
    _, contours, hierarchy = cv2.findContours(
                            mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)  
    maximumArea = 0
    bestContour = None
    for contour in contours:
        currentArea = cv2.contourArea(contour)
        if currentArea > maximumArea:
            bestContour = contour
            maximumArea = currentArea
    if bestContour is not None:
        x,y,w,h = cv2.boundingRect(bestContour)
        cv2.drawContours(main_window, [bestContour], 0, player.color, 3)
        cir = Circle(x + w/2, y + h/2, 30)
        return cir
    return Circle(0, 0, 1)
    
        
def collisions(x, y):
    xd = x.x - y.x
    yd = x.y - y.y
    sqrRadius = (x.radius+y.radius) * (x.radius+y.radius)
    sqrDist = (xd*xd) + (yd*yd)
    if sqrDist <= sqrRadius:
        return True
    return False

class Player:
    def __init__(self, id):
        self.name = "Unnamed"
        self.active = True
        self.color = COLORS[id]
        self.lower_color = np.array([0, 0, 0])
        self.upper_color = np.array([255, 255, 255])
        self.point = Circle(100, 100, CIRCLE_SIZE)
        self.score = 0
    
    def setColor(self, low, high):
        self.lower_color = low
        self.upper_color = high
        
    def checkCollisions(self, cir):
        if collisions(cir, self.point):  
            if(self.active):
                self.score += 1
                self.active = False
            ranx = random.randrange(60, window_width - 60)
            rany = random.randrange(60, window_height - 60)
            self.point.x = ranx
            self.point.y = rany
        else:
            self.active = True
            cv2.circle(main_window, (self.point.x, self.point.y), 50, (0, 255, 0), -1)
    

player1 = Player(0)
player2 = Player(1)
player2mode = False
gamemode = False

window_width = camera_feed.get(4)
window_height = camera_feed.get(5)

HSVwindow = np.zeros((200, 500, 3), np.uint8)
cv2.namedWindow(WINDOW_NAME_1)

# Create trackbars for HSV change
cv2.createTrackbar('HLower', WINDOW_NAME_1, 0, 255, nothing)
cv2.createTrackbar('SLower', WINDOW_NAME_1, 0, 255, nothing)
cv2.createTrackbar('VLower', WINDOW_NAME_1, 0, 255, nothing)
cv2.createTrackbar('HUpper', WINDOW_NAME_1, 255, 255, nothing)
cv2.createTrackbar('SUpper', WINDOW_NAME_1, 255, 255, nothing)
cv2.createTrackbar('VUpper', WINDOW_NAME_1, 255, 255, nothing)
 
lower_color = np.array([0, 0, 0])
upper_color = np.array([255, 255, 255])

element = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
element2 = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 4))
players = []

while(1):

    _,main_window = camera_feed.read()
    hsv = cv2.cvtColor(main_window, cv2.COLOR_BGR2HSV)
    
    
    k = cv2.waitKey(5) & 0xFF
    
    if not gamemode:
        testmask = cv2.inRange(hsv, lower_color, upper_color) 
        testmask = cv2.erode(testmask, element, iterations = 2)
        testmask = cv2.dilate(testmask, element2, iterations = 2)
        cv2.imshow(WINDOW_NAME_1, HSVwindow)
        if not player2mode:
            cv2.putText(testmask, "Player 1 color:" , (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, [0, 255, 0])
        else:
            cv2.putText(testmask, "Player 2 color:" , (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, [0, 0, 255])
        cv2.imshow('mask', testmask)
        h_lower = cv2.getTrackbarPos('HLower', WINDOW_NAME_1)
        s_lower = cv2.getTrackbarPos('SLower', WINDOW_NAME_1)
        v_lower = cv2.getTrackbarPos('VLower', WINDOW_NAME_1)
        h_upper = cv2.getTrackbarPos('HUpper', WINDOW_NAME_1)
        s_upper = cv2.getTrackbarPos('SUpper', WINDOW_NAME_1)
        v_upper = cv2.getTrackbarPos('VUpper', WINDOW_NAME_1)
        lower_color = np.array([h_lower, s_lower, v_lower])
        upper_color = np.array([h_upper, s_upper, v_upper])    
        if k == 13:
            if player2mode:
                player2.setColor(lower_color, upper_color)
                cv2.destroyWindow(WINDOW_NAME_1)
                cv2.destroyWindow('mask')
                gamemode = True
            else:
                player1.setColor(lower_color, upper_color)
                player2mode = True
        
    else:    
        cir = getPlayerCircle(player1)
        cir2 = getPlayerCircle(player2)
                
        player1.checkCollisions(cir)
        player2.checkCollisions(cir2)
        
        cv2.putText(main_window, "Score: %d" % player1.score, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, [0, 255, 0])
        cv2.putText(main_window, "Score: %d" % player2.score, (450, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, [255, 0, 0])
        
        cv2.imshow(MAIN_WINDOW_NAME, main_window)    
    if k == 27:
        break
    
cv2.destroyAllWindows() 