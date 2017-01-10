from __future__ import print_function
import cv2
import numpy as np
import validate as vl
import showfig as sf
import circularity as cr
import glob as gb
import test
import math
from matplotlib import pyplot as plt


def recognition(extended_rectangle, rectangle, gate_counter):
    sf.showfig(extended_rectangle, plt.get_cmap('gray'))         #testing

    kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 4))  # kernel to detect horizontal lines
    kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 1))  # kernel to detect horizontal lines
    kernel3 = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 5))  # kernel to detect horizontal lines
    greyscale_gate = cv2.cvtColor(extended_rectangle, cv2.COLOR_BGR2GRAY)  # converting the gate image to greyscale
    sf.showfig(greyscale_gate,plt.get_cmap('gray'))
    cv2.imwrite("circuit1/gate/gate" + str(gate_counter) + "/3_inverted" + str(gate_counter) + ".png", greyscale_gate)
   # cv2.imwrite("circuit1/gate/closing.png", closing)
    ret, inverted_greyscale = cv2.threshold(greyscale_gate, 127, 255,
                                            cv2.THRESH_BINARY_INV)  # converting the greyscale image into inverted greyscale image.
    # inverted_greyscale = cv2.morphologyEx(inverted_greyscale, cv2.MORPH_CLOSE, kernel2)
    inverted_greyscale = cv2.morphologyEx(inverted_greyscale, cv2.MORPH_CLOSE, kernel1)
    inverted_greyscale = cv2.morphologyEx(inverted_greyscale, cv2.MORPH_CLOSE, kernel3)
    sf.showfig(inverted_greyscale, plt.get_cmap('gray'))
    cv2.imwrite("circuit1/gate/gate" + str(gate_counter) + "/4_closing" + str(gate_counter) + ".png", inverted_greyscale)
    height_mask, width_mask = inverted_greyscale.shape[:2]
    mask = np.zeros((height_mask + 2, width_mask + 2), np.uint8)  # mask for flood-filling
    connectivity = 4
    newmaskval = 255

    cv2.floodFill(inverted_greyscale, mask, (0, 0), 255)  # flood-filling from above point
    cv2.floodFill(inverted_greyscale, mask, (width_mask - 2, height_mask - 2), 255)  # flood-filling from down point

    sf.showfig(inverted_greyscale, plt.get_cmap('gray'))
    cv2.imwrite("circuit1/gate/gate" + str(gate_counter) + "/5_floodfill" + str(gate_counter) + ".png", inverted_greyscale)
    test.func1(inverted_greyscale,extended_rectangle)

    ret, inverted = cv2.threshold(inverted_greyscale, 127, 255,
                                  cv2.THRESH_BINARY_INV)  # inverted image after flood-filing
    ha1, contours, ha2 = cv2.findContours(inverted, cv2.RETR_EXTERNAL,
                                          cv2.CHAIN_APPROX_SIMPLE)  # contour for checking connected component

    component = len(contours)  # number of component
    print(component)
    st = ""
    font = cv2.FONT_HERSHEY_SIMPLEX
    if component >= 4:  # condition for checking nxor gate  (connected component = 4)
        temp = []  # local variable for storing component attributes (x-cord,y-cord,w,h)
        for ct in contours:
            temp1 = []
            temp1 = cv2.boundingRect(ct)
            temp.append(temp1)
        temp = sorted(temp, key=lambda x: (x[0]))
        if inverted_greyscale[temp[1][1]][temp[1][0]+temp[1][2]] ==0 and inverted_greyscale[temp[1][0]+temp[1][2]][temp[1][1]+temp[1][2]] ==0:
            print("GATE NOT VALID")
           # exit()
        cv2.putText(gb.original_image, 'NXOR', (gb.x_cord, gb.y_cord + 100), font, 2, (0, 0, 255), 2, cv2.LINE_AA)
        st = "NXOR"
        print(st)
    if component == 3:  # condition for checking nand/nor/xor (connected component = 3)
        temp = []  # local variable for storing component attributes (x-cord,y-cord,w,h)
        for ct in contours:
            temp1 = []
            temp1 = cv2.boundingRect(ct)
            temp.append(temp1)
        temp = sorted(temp, key=lambda x: (x[0]))
        if inverted_greyscale[temp[1][1]][temp[1][0]+temp[1][2]]==0 and inverted_greyscale[temp[1][1]+temp[1][3]][temp[1][0]+temp[1][2]] ==0:
            print("GATE NOT VALID")
            #exit()
        #		print(str(temp[0][0])+str(temp[1][0])+str(temp[2][0]))
        if temp[1][2] * temp[1][3] < temp[2][2] * temp[2][3]:  # considering 2 and 3 component of gate(comparing area)
            print(str(int(math.floor(gb.x_cord + temp[1][2] / 2))) + " " + str(int(math.floor(gb.y_cord + 100))))
            print("XOR")
            try:
                cv2.putText(gb.original_image, "XOR", (gb.x_cord, gb.y_cord + 100), font, 2,(0, 0, 255), 2, cv2.LINE_AA)  # labeling the recognized gate
            except Exception as e:
                print ("error")
            st = "XOR"
        else:
            st = cr.circuilarity_check(rectangle, component, st)
    if component == 2:  # condition for checking and/or/not gate (connected component = 2)
        x1, y1, w1, h1 = cv2.boundingRect(contours[0])  # x-cord,y-cord,width,height of component 1
        x2, y2, w2, h2 = cv2.boundingRect(contours[1])
        # print(str(x1)+" "+str(w1*h1)+" "+str(x2)+" "+str(w2*h2))
        if x1 < x2 and w1 * h1 < w2 * h2:  # checking whether gate is 'not'/('or','and')
            st = cr.circuilarity_check(rectangle, component, st)
            if inverted_greyscale[y2][x2+w2] == 0 and inverted_greyscale[y2 + h1][x2+w2] == 0:
                print("GATE NOT VALID")
                #exit()
        elif x2 < x1 and w2 * h2 < w1 * h1:
            st = cr.circuilarity_check(rectangle, component, st)
            if inverted_greyscale[y1][x1 + w1] == 0 and inverted_greyscale[y1 + h1][x1 + w1] == 0:
                print("GATE NOT VALID")
                exit()
        else:
            print("NOT")
            cv2.putText(gb.original_image, 'NOT', (gb.x_cord , gb.y_cord + 100), font, 2,
                        (0, 0, 255), 2, cv2.LINE_AA)
            st = "NOT"
        #	print(st+"###")
    if component == 1:
        cv2.putText(gb.original_image, 'NOT', (gb.x_cord , gb.y_cord + 100), font, 2,
                    (0, 0, 255), 2, cv2.LINE_AA)
        st = "NOT"
    gb.insert(gb.gate(st, gb.x_cord, gb.y_cord, len(extended_rectangle), len(extended_rectangle[0]), len(gb.gates)))

