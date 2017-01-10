from __future__ import print_function
import cv2
import numpy as np
import validate as vl
import showfig as sf
import recognition as rp
import circularity as cr
import glob as gb
import code2
import code
from matplotlib import pyplot as plt
import math
import string
import sys

#name= raw_input("Ask user for something.")
name = 'b1.png'
print(name)
original_image=cv2.imread(name)
gb.init(original_image)          												# Call only once																		# reading original image
greyscale_image = code.precompute(name)																																# reading greyscale image
line_image= cv2.cvtColor(gb.original_image, cv2.COLOR_BGR2GRAY) 
ret,line_image_inv=cv2.threshold(greyscale_image,127,255,cv2.THRESH_BINARY_INV)
ret,inverted_greyscale = cv2.threshold(greyscale_image,127,255,cv2.THRESH_BINARY_INV)  								# converting the greyscale image into inverted greyscale image.
cv2.imwrite('image4.png',inverted_greyscale)
sf.showfig(inverted_greyscale,plt.get_cmap('gray'))				#testing

kernel = np.ones((10,10),np.uint8) 																																		# kernel for opening operation								
opening = cv2.morphologyEx(inverted_greyscale, cv2.MORPH_OPEN, kernel) 											# applying opening morphological operation to remove the noise from the image
cv2.imwrite('image5.png',opening)																									
sf.showfig(opening,plt.get_cmap('gray'))							#testing
cv2.imwrite("circuit1/intermediate/4_opening_after_floodfill.png", opening)

ha1,contours,ha2=cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)						# finding contour

gate_counter=0
for i in contours:
	if vl.validate(i):																																										#validating the contour in opening image
		#print("&&&")
		x_cord,y_cord,width,height = cv2.boundingRect(i)
		print(str(width)+" "+str(height))
		if (width/height<4):																																							#ratio validation for contour (to emit false contour)
			#print("@@@@")
			#print(str(width)+" "+str(height))
			gb.x_cord=x_cord
			gb.y_cord=y_cord
			limit=int(math.ceil(height/15))
			rectangle = gb.original_image[y_cord+limit:y_cord+height-limit,x_cord-20:x_cord+width]										#cropping the gate

			extended_rectangle = gb.original_image[y_cord-15:y_cord+height+15,x_cord-30:x_cord+width+15]				#cropping the gate with extended dimension
			sf.showfig(rectangle,plt.get_cmap('gray'))
			segmented_gate = "smp"+str(gate_counter)+".png"																								#string to name cropped image
			cv2.imwrite("circuit1/gate/gate"+str(gate_counter+1)+"/1_rectangle"+str(gate_counter)+".png", rectangle)
			cv2.imwrite("circuit1/gate/gate"+str(gate_counter+1	)+"/2_extended_rectangle"+str(gate_counter)+".png", extended_rectangle)
			cv2.imwrite(segmented_gate,rectangle)
			gate_counter=gate_counter+1																																	#updating the number of gates found
			rp.recognition(extended_rectangle,rectangle,gate_counter)																											#recognition and labeling of gates
			cv2.rectangle(gb.original_image,(x_cord-7,y_cord-7),(x_cord+width+7,y_cord+height+7),(0,0,255),7)				#bounding the gates on original image
			for r1 in range(x_cord-4,x_cord+width+5):
				for r2 in range(y_cord-4,y_cord+height+5):
					line_image_inv[r2][r1]=0

sf.showfig(line_image_inv,plt.get_cmap('gray'))
cv2.imwrite('image7.png',line_image_inv)
cv2.imwrite('image6.png',gb.original_image)

code2.line_code(name)
#sf.showfig(gb.original_image,None)
cv2.imwrite('image6.png',gb.original_image)