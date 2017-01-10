from __future__ import print_function
import math
import cv2
import numpy as np
import validate as vl
import showfig as sf
from matplotlib import pyplot as plt
import glob as gb

def circuilarity_check(rectangle,component,st):
	extended_rectangle = cv2.cvtColor(rectangle, cv2.COLOR_BGR2GRAY) 															# converting the image into greyscale
	ret,inverted = cv2.threshold(extended_rectangle,127,255,cv2.THRESH_BINARY_INV) 		 								# converting the image into inverted greyscale image.
	#sf.showfig(inverted,plt.get_cmap('gray'))
	point1=0
	point4=0
	temp1=0
	temp2=len(rectangle)-1
	point2=0
	point3=0
	point5=0
	while inverted[0][point1]==0:
		point1+=1
	while inverted[len(rectangle)-3][point4]==0:																						###change
		point4+=1
	while inverted[temp1][0]==0:
		temp1+=1
	while inverted[temp2][0]==0:
		temp2-=1
	temp1-=3
	temp2+=1
	temp3=int(math.floor((temp1+temp2)/2))
	while inverted[int(temp1)][int(point2)]==0:
		point2+=1
	while inverted[temp2][point3]==0 and point3 < len(rectangle[0]) :
		point3+=1
	while inverted[temp3][point5]==0:
		point5+=1
	print("#"+str(point1)+"#"+str(point2)+"#"+str(point3)+"#"+str(point4)+"#"+str(point5))

	h, w = rectangle.shape[:2]
																																# Write some Text
	font = cv2.FONT_HERSHEY_SIMPLEX
#	print (abs(point2-point1))
#	print (abs(point3-point4))
	if(component==3):
			st="N"
	if (point5-point1)<6 or (point5-point4)<6:
		st=st+"AND"
		print(st)
		cv2.putText(gb.original_image,st,(gb.x_cord,gb.y_cord+100), font, 2,(0,0,255),2,cv2.LINE_AA)
	else:
		st=st+"OR"
		print(st)
		cv2.putText(gb.original_image,st,(gb.x_cord,gb.y_cord+100), font, 2,(0,0,255),2,cv2.LINE_AA)
	return st
