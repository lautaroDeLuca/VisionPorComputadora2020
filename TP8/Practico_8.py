import cv2
import numpy as np

mode = False
drawing = False # true if mouse is pressed
ix, iy = -1, -1 # Puntos iniciales de x e y
dx, dy = 0, 0 # Diferencia entre punto inicial y final en x e y
img = cv2.imread('cancha2.jpg', 0)
alto, ancho = img.shape[:2]
Puntos = np.float32([[0, 0], [0, 0], [0, 0], [0, 0]])
contador = 0
orden_affin = False
orden_homografia = False


def draw(event, x, y, flags, param):
    global ix, iy, drawing, dx, dy, img, mode, contador

    if event == cv2.EVENT_LBUTTONDOWN:
        if mode is False:
            drawing = True
            ix, iy = x, y
        else:
            pass
        
    elif event == cv2.EVENT_MOUSEMOVE:
        if mode is False:
            if drawing is True:
                img = cv2.imread('cancha2.jpg', 0) # Para que el rectangulo dibujado anteriormente se borre
                cv2.rectangle(img, (ix, iy), (x, y), (0, 255, 0), 1)
        else:
            pass

    elif event == cv2.EVENT_LBUTTONUP:
        if mode is False:
            drawing = False
            cv2.rectangle(img, (ix,iy), (x, y), (0, 255, 0), 1)
            if ((y > iy) & (x > ix)): # Para que el rectangulo pueda ser tomado en cualquier dirección!
                dy = y - iy
                dx = x - ix
            elif ((y < iy) & (x < ix)):
                dy = iy - y
                dx = ix - x
                ix = x
                iy = y
            elif ((y < iy) & (x > ix)):
                dy = iy - y
                dx = x - ix
                iy = y
            else:
                dy = y - iy
                dx = ix - x
                ix = x
        else:
            if (contador < 4) & ((orden_affin == True) | (orden_homografia == True)):     
                cv2.circle(img, (x, y), 3, (0, 0, 255), -1)
                Puntos[contador][0] = x
                Puntos[contador][1] = y
                contador = contador + 1
                

def euclidean(image, angle, tx, ty, center = None, scale = 1.0):
    (h, w) = image.shape[:2]
    print(h, w)

    if center is None:
        center = (w/2, h/2)

    R = cv2.getRotationMatrix2D(center, angle, scale)

    M = np.float32([[R[0, 0], R[0, 1], tx], [R[1, 0], R[1, 1], ty]])

    print(M)

    euclideana = cv2.warpAffine(image, M, (w, h))

    return euclideana

def affine(pts_dest, pts_fuente, imagen, dsize):
    M = cv2.getAffineTransform(pts_dest, pts_fuente)
    afin = cv2.warpAffine(imagen, M, dsize)           # El dsize se pone en forma de imagen (WxH, ejemplo 640x480) 
                                                     # No en forma de matriz (Fila x Columna que seria HxW, ejemplo 480x640) 
    return afin


def homografia(img, pts1F, pts2D, size): # Puntos Fuente y Destino 
    M = cv2.getPerspectiveTransform(pts1F, pts2D)
    homograf = cv2.warpPerspective(img, M, (sizex, sizey))

    return homograf

img = cv2.imread('cancha2.jpg', 0)
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw)

while (1):
    cv2.imshow('image', img)
    k = cv2.waitKey(1) & 0xFF

    if ((k == ord('g')) & ((dy | dx) != 0)): # Si se aprieta g y la diferencia en x o en y es distinta de cero
                                             # para evitar se apriete g y no se haya seleccionado
                                             # una porcion de la imagen todavía, esto daría error ya que
                                             # tendriamos una matriz sin ningun elemento
        img2 = np.zeros((dy, dx), np.uint8)
        for i in range(0, dy):
            for j in range(0, dx):
                img2 [i][j] = img [iy+i][ix+j]
        cv2.imwrite('imagenrecortada.png', img2)
        break

    elif k == ord('r'):
        img = cv2.imread('cancha2.jpg',0)
        dx = 0
        dy = 0

    elif ((k == ord('e')) & ((dy | dx) != 0)):
        img2 = np.zeros((dy, dx), np.uint8)
        for i in range(0, dy):
            for j in range(0, dx):
                img2 [i][j] = img [iy+i][ix+j]

        angulo = int(input('Ingrese el ángulo: '))
        traslacionx = int(input('Ingrese la traslacion en x: '))
        traslaciony = int(input('Ingrese la traslacion en y: '))
        tranf = euclidean(img2, angulo, traslacionx, traslaciony)
        cv2.imwrite('imageneuclideada.png', tranf)
        break

    elif ((k == ord('s')) & ((dy | dx) != 0)):
        img2 = np.zeros((dy, dx), np.uint8)
        for i in range(0, dy):
            for j in range(0, dx):
                img2 [i][j] = img [iy+i][ix+j]

        angulo = int(input('Ingrese el ángulo: '))
        traslacionx = int(input('Ingrese la traslacion en x: '))
        traslaciony = int(input('Ingrese la traslacion en y: '))
        s = float(input('Ingrese el escalado de la imagen: '))
        tranf = euclidean(img2, angulo, traslacionx, traslaciony, scale = s)
        cv2.imwrite('imagensimil.png', tranf)
        break

    elif k == ord('a'):
        
        mode = True
        orden_affin = True 
        Puntos = np.float32([[0, 0], [0, 0], [0, 0], [0, 0]])
        contador = 0
        
    if ((contador > 2) & (orden_affin == True)):
        
        orden_affin = False
        print('ya estan los 3 valores')
        PD3 = Puntos[:3, :3]
        print('PD3 =', PD3)
        img = cv2.imread('cancha2.jpg', 0) # Para que no queden 3 puntos en la imagen
        
        img_fuente = cv2.imread('PS5.png', 0) # Imagen a pegar(fuente_source)
        cv2.imshow('imagen fuente', img_fuente)
        alto_fuente, ancho_fuente = img_fuente.shape[:2]
        PF3 = np.float32([[0, 0], [ancho_fuente - 1, 0], [ancho_fuente - 1, alto_fuente - 1]]) # Puntos de vertice de imagen fuente a pegar
                                                                                               # Sup_Izq, Sup_Der e Inf_Der        
        print('PF3 =', PF3)
        img_fuente_afin = affine(PF3, PD3, img_fuente, (ancho, alto))
        cv2.imshow('imagen fuente afin', img_fuente_afin)       
        thr = 1
        ret, mask = cv2.threshold(img_fuente_afin, thr, 255, cv2.THRESH_BINARY_INV)        
        imgdest_hueco = cv2.bitwise_and(img, img, mask = mask) # A la imagen destino deja en color negro(valor 0)
                                                               # la parte donde se va a incrustar la imagen fuente
        cv2.imshow('imagen hueco', imgdest_hueco)
        cv2.imshow('mascara', mask)
        imgfinal = cv2.add(imgdest_hueco, img_fuente_afin)     # Suma de ambas imagenes
        cv2.imshow('imagen incrustada', imgfinal)
        mode = False

    elif k == ord('h'):
        mode = True
        orden_homografia = True
        Puntos = np.float32([[0, 0], [0, 0], [0, 0], [0, 0]])
        contador = 0


    if ((contador > 3) & (orden_homografia == True)):
        
        orden_homografia = False
        print('ya estan los 4 valores')
        PF4 = Puntos          # 4 Puntos Fuente seleccionados en la imagen, que van a ir a una nueva imagen destino
        print('PF4 =', PF4) 
        img = cv2.imread('cancha2.jpg', 0) # Para que no queden 4 puntos en la imagen
        
        sizex = int(input('Ingrese el tamaño de la imagen rectificada en x:'))
        sizey = int(input('Ingrese el tamaño de la imagen rectificada en y:'))
        PD4 = np.float32([[0, 0], [sizex-1, 0], [sizex-1, sizey-1], [0, sizey-1]])
        
        #PD4 = np.float32([[100, 100], [sizex-100, 100], [sizex-100, sizey-100], [100, sizey-100]])
        # La linea anterior fue para probar que: si se rectifica la parte de la imagen seleccionada
        # con tamaño menor al de la imagen de salida, lo que sobra en la imagen de salida lo completa
        # con los pixeles alrededor de la porcion seleccionada de la imagen original, y esto tambien
        # estará rectificada.
        # Por lo tanto para rectificar toda una imagen hay 2 opciones
        # 1) Se elige un tamaño de salida mucho mayor
        # 2) Se elige el mismo tamaño de salida que la imagen a rectificar
        #    pero la parte de la imagen elegida se debe localizar en la img rectificada
        #    en un espacio igual o menor en pixeles de los que ocupa en la img original
        # Pero si dejo los puntos origen igual a los destinos y le doy el mismo tamaño
        # nunca se aplica la transformación. Para rectificar los puntos destino, estos deberian
        # estar sobre la misma fila de pixeles el 1er punto con el 2do, mientras que el 2do con el 3er
        # en la misma columna y el 3er con el 4to en la misma fila mas abajo y el 4to con el 1er en la misma columna.
        
        
        print('PD4 =', PD4)
        
        img_rect = homografia(img, PF4, PD4, (sizex, sizey))
        cv2.imshow('Imagen Rectificada', img_rect)

        mode = False

    elif k == ord('q'):
        break

cv2.destroyAllWindows()
