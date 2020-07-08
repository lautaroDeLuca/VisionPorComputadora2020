import sys
import cv2

if (len(sys.argv) > 1):
    filename = sys.argv[1]
else:
    print('Pass a filename as first argument')
    sys.exit(0)

cap = cv2.VideoCapture(filename)
W = int(cap.get(3))
H = int(cap.get(4))
FPS = cap.get(5)
delay = int((1/FPS)*1000)
print('El ancho es', W, '\nEl alto es', H, '\nLos FPS son', FPS)
print('Los ms del delay son', delay)

fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
framesize = (W, H)
out = cv2.VideoWriter('output.avi', fourcc, FPS, framesize, 0)
# El ultimo argumento pasado es el color, true = color, false = grises.

while (cap.isOpened()):
    ret, frame = cap.read()
    if ret is True:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        out.write(gray)
        cv2.imshow('Image gray', gray)
        if cv2.waitKey(delay) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
out.release()
cv2.destroyAllWindows()
