#! /usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np

import cv2
import glob
import pickle

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objp = np.zeros((8*11,3), np.float32)
objp [:,:2] = np.mgrid [0:11,0:8].T.reshape( -1 , 2)

objpoints = []
imgpoints = []

images = glob.glob('tmp/*.jpg')

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret,corners = cv2.findChessboardCorners(gray,(11,8), None)
    if ret is True:
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gray,corners,(11,11) , (-1 ,-1) , criteria)
        imgpoints.append(corners2)
        img = cv2.drawChessboardCorners(img,(11,8) ,corners2, ret)
        cv2.imshow('img', img)
        cv2.waitKey(300)
cv2.destroyAllWindows()

ret,cameraMtx,distCoeffs,rvecs,tvecs = cv2.calibrateCamera(objpoints,imgpoints,gray.shape[:: -1],None,None)

with open ('cameraMtx.pickle', "wb") as matrix_file:
    pickle.dump(cameraMtx, matrix_file, pickle.HIGHEST_PROTOCOL)
with open ('distCoeffs.pickle', "wb") as coeffs_file:
    pickle.dump(distCoeffs, coeffs_file, pickle.HIGHEST_PROTOCOL)