import numpy as np
import cv2

#import image in color
img_color = cv2.imread('c:/Users/Gvargas/Documents/Springboard Data Science Bootcamp/Springboard/capstone/ocr_capstone/Data/filled_test.jpg')

print(img_color.shape)
#resize image
img_color = cv2.resize(img_color,(int(img_color.shape[0]/5),int(img_color.shape[1]/8)))
#import image in grayscale
img_gray = cv2.imread('c:/Users/Gvargas/Documents/Springboard Data Science Bootcamp/Springboard/capstone/ocr_capstone/Data/filled_test.jpg',0)
#resize gray image
img_gray = cv2.resize(img_gray,(int(img_gray.shape[0]/5),int(img_gray.shape[1]/8)))

#Thresholding
ret, t_binary = cv2.threshold(img_gray,100,255,cv2.THRESH_BINARY)
thr = cv2.adaptiveThreshold(img_gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,3,8)

#remove noise from adaptive thresh
kernel = np.ones((5,5), dtype = np.uint8)
thr_open = cv2.morphologyEx(thr,cv2.MORPH_OPEN,kernel)

while True:
    cv2.imshow('color',img_color)
    cv2.imshow('gray', img_gray)
    cv2.imshow('thresh_binary', t_binary)
    cv2.imshow('adaptive', thr)
    cv2.imshow('adaptive_open', thr_open)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cv2.destroyAllWindows()