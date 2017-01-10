import cv2
import numpy as np
import showfig as sf
from matplotlib import pyplot as plt

def func(filename,org):
    #filename = 'A1.png'
    #img = cv2.imread(filename)
    gray = cv2.cvtColor(filename,cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    corners = cv2.goodFeaturesToTrack(gray, 100, 0.08, 10)
    corners = np.int0(corners)
    for corner in corners:
        x, y = corner.ravel()
        cv2.circle(org, (x, y), 3, 255, -1)
    sf.showfig(org  ,None)
    cv2.imwrite('t1.png',org)

def func1(filename,org):
    #gray = cv2.cvtColor(filename, cv2.COLOR_BGR2GRAY)
    #kernel = np.ones((6, 6), np.uint8)
    #gray = cv2.dilate(gray, kernel, iterations=1)
    #sf.showfig(gray,plt.get_cmap('gray'))
    gray = np.float32(filename)
    dst = cv2.cornerHarris(gray, 2, 3, 0.18)

    # result is dilated for marking the corners, not important
    dst = cv2.dilate(dst, None)

    # Threshold for an optimal value, it may vary depending on the image.
    org[dst > 0.01 * dst.max()] = [0, 0, 255]
    sf.showfig(org, None)                                                  #testing
    cv2.imwrite('t1.png', org)