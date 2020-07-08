import cv2

img = cv2.imread('hoja.jpg', 0)

#for i in range(0,len(img)):
#   print(img[i],"\n")

umbral = 200

for i, fila in enumerate(img):
    for j, columna in enumerate(fila):
        if (columna > umbral):
            img[i][j] = 255
        else:
            img[i][j] = 0

cv2.imwrite('resultado2.png', img)
