import cv2
import numpy as np

drawing = False # true if mouse is pressed
ix, iy = -1, -1 # Puntos iniciales de x e y
dx, dy = 0, 0 # Diferencia entre punto inicial y final en x e y
img = cv2.imread('messi5.jpg', 0)

def draw(event, x, y, flags, param):
    global ix, iy, drawing, dx, dy, img

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing is True:
            img = cv2.imread('messi5.jpg', 0) # Para que el rectangulo dibujado anteriormente se borre
            cv2.rectangle(img, (ix, iy), (x, y), (0, 255, 0), 1)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.rectangle (img, (ix,iy), (x, y), (0, 255, 0), 1)
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

img = cv2.imread('messi5.jpg', 0)
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
        img = cv2.imread('messi5.jpg',0)
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

    elif k == ord('q'):
        break

cv2.destroyAllWindows()

