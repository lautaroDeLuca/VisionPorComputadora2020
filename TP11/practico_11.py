import cv2
import numpy as np

MIN_MATCH_COUNT = 10

img1 = cv2.imread('imagen002.jpg') # Leemos la imagen 1
img2 = cv2.imread('imagen001.jpg') # Leemos la imagen 2

sift_dscr = cv2.SIFT_create() # Inicializamos el detector y el descriptor

kp1, des1 = sift_dscr.detectAndCompute(img1, None) # Encontramos los puntos claves y los descriptores con SIFT en la imagen 1
kp2, des2 = sift_dscr.detectAndCompute(img2, None) # Encontramos los puntos claves y los descriptores con SIFT en la imagen 2

cv2.drawKeypoints(img1, kp1, img1)
cv2.drawKeypoints(img2, kp2, img2)
cv2.imshow('Puntos de interes en imagen 1', img1)
cv2.imshow('Puntos de interes en imagen 2', img2)
cv2.waitKey(20)

img1 = cv2.imread('imagen002.jpg') # Leemos la imagen 1
img2 = cv2.imread('imagen001.jpg') # Leemos la imagen 2

matcher = cv2.BFMatcher_create(cv2.NORM_L2)
matches = matcher.knnMatch(des1, des2, k=2)

good = []
for m in matches:
	if m[0].distance < 0.7*m[1].distance:
		good.append([m[0]])
		print('m = ',m)
		#print('good = ', good[i-1])

print('goods = ', good)
		
img = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good, None, flags = 2)
#cv2.imshow('Correspondencias - Matches', img)
#cv2.waitKey(20)

if( len(good) > MIN_MATCH_COUNT):
	src_pts = np.float32([ kp1[m[0].queryIdx].pt for m in good ]).reshape(-1, 1, 2)
	dst_pts = np.float32([ kp2[m[0].trainIdx].pt for m in good ]).reshape(-1, 1, 2)
	
#print('src_pts = ', src_pts)	

H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

h, w, d = img1.shape
print('hwd = ', h, ' ', w, ' ', d)
dst = cv2.warpPerspective(img1, H, (w, h))

cv2.imshow('Correspondencias - Matches', img)
cv2.imshow('perspective', dst)

alpha = 0.5
blend = np.array( dst * alpha + img2 * (1 - alpha), dtype = np.uint8)

cv2.imshow('Sangrado', blend)

cv2.waitKey()

	
