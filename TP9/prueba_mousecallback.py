# Este programa es hecho para probar si se puede
# usar 2 veces la funcion MouseCallBack en diferentes
# ventanas de imagenes y con 2 funciones distintas
# Spoiler = Si se puede


import cv2
import numpy as np

ix, iy = -1, -1
mode = False



def draw_line(event, x, y, flags, param):
	global ix, iy, mode, img1
    
	if event == cv2.EVENT_LBUTTONDOWN:
		mode = True
		ix, iy = x, y
	
	if event == cv2.EVENT_MOUSEMOVE:
		if (mode == True):
			img1 = np.ones((512, 512, 3), np.uint8)*255
			cv2.line(img1, (ix, iy), (x, y), (0, 0, 255), 3)
		
	if event == cv2.EVENT_LBUTTONUP:
		cv2.line(img1, (ix, iy), (x, y), (0, 0, 255), 3)
		mode = False

def draw_circle(event, x, y, flags, param):
	
	if event == cv2.EVENT_LBUTTONDOWN:
		cv2.circle(img2, (x, y), 3, (0, 0, 255), -1)
	
	if event == cv2.EVENT_MOUSEMOVE:
		cv2.circle(img2, (x, y), 3, (0, 0, 255), -1)
		
	if event == cv2.EVENT_LBUTTONUP:
		cv2.circle(img2, (x, y), 3, (0, 0, 255), -1)


img1 = np.ones((512, 512, 3), np.uint8)*255
img2 = np.ones((512, 512, 3), np.uint8)		

cv2.namedWindow('image1')
cv2.namedWindow('image2')
cv2.setMouseCallback('image1', draw_line)
cv2.setMouseCallback('image2', draw_circle)

while(1):
	cv2.imshow('image1', img1)
	cv2.imshow('image2', img2)
	cv2.setMouseCallback('image1', draw_line)    # Se pone aca de vuelta para que si se cierra
	cv2.setMouseCallback('image2', draw_circle)  # la ventana se vuelva a ejecutar la función del mouse
	if cv2.waitKey(20) & 0xFF == 27: #Escape para salir
		break
		
cv2.destroyAllWindows()
