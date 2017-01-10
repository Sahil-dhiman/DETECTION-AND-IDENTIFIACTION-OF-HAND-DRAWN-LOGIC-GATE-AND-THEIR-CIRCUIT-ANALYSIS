from __future__ import print_function
import cv2
import numpy as np
from matplotlib import pyplot as plt

def validate(cnt):
    rect=cv2.minAreaRect(cnt)
    box=cv2.boxPoints(rect)
    box=np.int0(box)
    output=False
    width=rect[1][0]
    height=rect[1][1]
    if (height*width)>200 :
        return True
    return output
