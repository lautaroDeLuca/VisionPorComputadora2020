import cv2
import numpy as np


mode = False # False para rectificar imagen, True para medición de objetos

def draw(event, x, y, flags, param):
	global ix, iy, mode, fx, fy              # ix = x inicial , fx = x final
    
    if event == cv2.EVENT_LBUTTONDOWN:
		if (mode == True):
			ix, iy = x, y
		else:
			pass
	
	if event == cv2.EVENT_MOUSEMOVE:
		if (mode == True):
			img2 = cv2.imread('imagen_rectificada.png')
			cv2.line(img2, (ix, iy), (x, y), (0, 0, 255), 3)
			
		else:
			pass
		
	if event == cv2.EVENT_LBUTTONUP:
		fx, fy = x, y
		if (mode == True):
			cv2.line(img2, (ix, iy), (fx, fy), (0, 0, 255), 3)
			
			#
			# Calculo de distancia en pixeles por pitagoras
			# Conversion de esa distancia a milimetros de la realidad
			# Imprimir la medida seleccionada con el mouse en pixeles y mm
			#
			
		else:
			cv2.circle(img2, (x, y), 3, (0, 0, 255), -1)
			
			
			
			

def homografia(img, pts1F, pts2D, size): # Puntos Fuente y Destino
    M = cv2.getPerspectiveTransform(pts1F, pts2D)
    homograf = cv2.warpPerspective(img, M, (sizex, sizey))

    return homograf



img = cv2.imread('imagen_utiles.png')
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw)
cv2.imshow('image', img)
