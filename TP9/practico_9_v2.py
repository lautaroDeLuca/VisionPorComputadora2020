import cv2
import numpy as np
import math

medicion = False # True cuando se esta midiendo 
ix, iy = -1, -1  # Punto inicial en x e y
fx, fy = -1, -1  # Punto final en x e y

mm_x_px_X = 0    # milimetros/pixel en la dirección X
mm_x_px_Y = 0    # milimetros/pixel en la direccion Y

img = cv2.imread('imagen_utiles.png')
alto, ancho = img.shape[:2]  # Va primero el alto en la tupla por que shape te entrega primero las filas(alto) y luego las columnas(ancho)
tamaño_img = (ancho, alto)
img2 = np.ones((ancho, alto, 3), np.uint8) # Se inicializa una imagen en negro, en esta variable se guardará la imagen rectificada
# se deberia poner primero el alto(filas) y luego el ancho(columnas)
# pero se ha puesto cruzado, para que quede un rectangulo horizontal y la imagen 
# que tiene mas resolución en vertical que la pantalla entre en la ventana y centrada

def linea_de_medicion(event, x, y, flags, param): # Función de Mouse para medir objetos en imagen rectificada
	global ix, iy, medicion, fx, fy, img2            
    
	if event == cv2.EVENT_LBUTTONDOWN:
		medicion = True
		ix, iy = x, y
	
	if event == cv2.EVENT_MOUSEMOVE:
		if (medicion == True):
			img2 = cv2.imread('imagen_rectificada.png') # Esto es para que actualice la imagen y vaya borrando las lineas
			cv2.line(img2, (ix, iy), (x, y), (0, 0, 255), 2)
			
		else:
			pass
		
	if event == cv2.EVENT_LBUTTONUP:
		fx, fy = x, y
		if (medicion == True):
			cv2.line(img2, (ix, iy), (fx, fy), (0, 0, 255), 2)
			
			medida = float(math.sqrt((mm_x_px_X * (fx-ix))**2 + (mm_x_px_Y * (fy-iy))**2))
			print (medida)
			
			medicion = False
			
			
PO = np.float32([[0, 0], [0, 0], [0, 0], [0, 0]]) # Inicialización de puntos origen, serán luego cargados
                                                  # con los 4 puntos de la imagen a rectificar
contador = 0	# Para que cargue solo 4 puntos
			
def puntos_para_rectificar(event, x, y, flags, param): # Funcion de Mouse para elegir 4 puntos y rectificar imagen
	global PO, contador
	
	if event == cv2.EVENT_LBUTTONUP:
		if(contador < 4):     
			cv2.circle(img, (x, y), 3, (0, 0, 255), -1)
			PO[contador][0] = x
			PO[contador][1] = y
			contador = contador + 1
			cv2.imshow('image1', img)

def homografia(img, pts1F, pts2D, size): # Puntos Fuente y Destino 
    M = cv2.getPerspectiveTransform(pts1F, pts2D)
    homograf = cv2.warpPerspective(img, M, (size[0], size[1]))

    return homograf


cv2.namedWindow('image1', cv2.WINDOW_NORMAL)
cv2.namedWindow('image2', cv2.WINDOW_NORMAL)
cv2.setMouseCallback('image1', puntos_para_rectificar)
cv2.setMouseCallback('image2', linea_de_medicion)

img = np.ones((ancho, alto, 3), np.uint8) # Creo imagen con ancho y alto invertido para centrar imagen
cv2.imshow('image1', img)
cv2.waitKey(60) # Es necesario para darle tiempo a que cargue la imagen con ancho y alto invertido
img = cv2.imread('imagen_utiles.png')


while(1):
	
	cv2.imshow('image1', img)
	cv2.imshow('image2', img2)
	
	if (contador > 3):
		
		PD = np.float32([[PO[0][0], PO[0][1]], [PO[1][0], PO[0][1]], [PO[1][0], PO[2][1]], [PO[0][0], PO[2][1]]])
		# PD son los puntos destino en donde caeran los puntos origenes de la img original en la nueva imagen rectificada	
		print (tamaño_img)
		print ('ancho= ', ancho)
		print ('alto= ', alto)
		img = cv2.imread('imagen_utiles.png') #Para que borre los puntos seleccionados con anterioridad
		img2 = homografia(img, PO, PD, tamaño_img)
		cv2.imwrite('imagen_rectificada.png', img2) # Para guardar imagen original rectificada y luego poder levantarla con imread
		
		contador = 0
		
		patron_mm_X = float(input('Ingrese la distancia en milimetros correspondientes del punto 1 al punto 2: '))
		patron_px_X = float(PO[1][0]-PO[0][0])
		mm_x_px_X = float(patron_mm_X/patron_px_X)
		
		patron_mm_Y = float(input('Ingrese la distancia en milimetros correspondientes del punto 2 al punto 3: '))
		patron_px_Y = float(PO[2][1]-PO[0][1])
		mm_x_px_Y = float(patron_mm_Y/patron_px_Y)
		
		
	if cv2.waitKey(20) & 0xFF == 27: #Escape para salir
		break
		
cv2.destroyAllWindows()
