import cv2
import numpy as np
from matplotlib import pyplot as plt


def showfig(image, ucmap):
    #There is a difference in pixel ordering in OpenCV and Matplotlib.
    #OpenCV follows BGR order, while matplotlib follows RGB order.
    if len(image.shape)==3 :
        b,g,r = cv2.split(image)       # get b,g,r
        image = cv2.merge([r,g,b])     # switch it to rgb
#    image=plt.figure(figsize=(8,6),'title')
    imgplot=plt.imshow(image, ucmap)
#    plt.title('Histogram of IQ')
    imgplot.axes.get_xaxis().set_visible(False)
    imgplot.axes.get_yaxis().set_visible(False)
    plt.show()


def precompute(name):

	img = cv2.imread(name,0)			#reading an image



	ret,img2 = cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV)  # converting the image into binary image.
	#showfig(img2,plt.get_cmap('gray'))
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(20,2))  # kernel to detect vertical lines
	vertical = cv2.morphologyEx(img2, cv2.MORPH_OPEN, kernel)  # applying morphological opening operation to detect vertical lines
	vertical = cv2.dilate(vertical,kernel,iterations = 1)   #dilate the vertical lines obtained
	

	kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT,(2,20))   # kernel to detect horizontal lines
	horizontal = cv2.morphologyEx(img2, cv2.MORPH_OPEN, kernel2)   # applying morphological opening operation to detect horizontal lines
	horizontal = cv2.dilate(horizontal,kernel2,iterations = 1)    #dilate the horizontal lines obtained

	#showfig(vertical,plt.get_cmap('gray'))   # show the vertical imag
	#showfig(horizontal,plt.get_cmap('gray'))  # show the horizontal image

	img = img2 -horizontal - vertical   # subtracting horizontal and vertical lines from original image
	cv2.imwrite('image1.png',img)

	kernel3=cv2.getStructuringElement(cv2.MORPH_RECT,(20,20))  # kernel for closing operation
	#showfig(img,plt.get_cmap('gray'))				#show image after removing horizontal and vertical lines

	closing=cv2.morphologyEx(img2,cv2.MORPH_CLOSE, kernel3 )
	showfig(closing,plt.get_cmap('gray'))
	cv2.imwrite('image2.png',closing)
	cv2.imwrite("circuit1/intermediate/1_inverted.png",img2)
	cv2.imwrite("circuit1/intermediate/2_closing.png",closing)

	#flood filling

	h, w = closing.shape[:2]
	mask = np.zeros((h+2, w+2), np.uint8)
	connectivity=4
	newmaskval=255
	flags=connectivity+(newmaskval<<8)+cv2.FLOODFILL_FIXED_RANGE+cv2.FLOODFILL_MASK_ONLY
	cv2.floodFill(closing,mask,(0,0),(0,)*3, (40,)*3, (40,)*3, flags)
	showfig(mask,plt.get_cmap('gray'))
	cv2.imwrite('image3.png',mask)
	cv2.imwrite("circuit1/intermediate/3_flood_fill.png",mask)

	return mask

	'''ret,img3 = cv2.threshold(mask,127,255,cv2.THRESH_BINARY_INV)  # converting the image into binary image.
	showfig(img3,plt.get_cmap('gray'))				#show image after removing horizontal and vertical lines
	vertical = cv2.morphologyEx(img3, cv2.MORPH_OPEN, kernel)  # applying morphological opening operation to detect vertical lines
	#vertical = cv2.dilate(vertical,kernel,iterations = 1)   #dilate the vertical lines obtained

	horizontal = cv2.morphologyEx(img3, cv2.MORPH_OPEN, kernel2)   # applying morphological opening operation to detect horizontal lines
	#horizontal = cv2.dilate(horizontal,kernel2,iterations = 1)    #dilate the horizontal lines obtained

	img = horizontal + vertical-img3   # subtracting horizontal and vertical lines from original image
	showfig(img,plt.get_cmap('gray'))'''
