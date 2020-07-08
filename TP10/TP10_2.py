#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

import cv2
import glob
import pickle

images = glob.glob('tmp/*.jpg')
correctedImg = 0
i=0

with open ('cameraMtx.pickle', "rb") as cameraMtx_file:
    cameraMtx = pickle.load(cameraMtx_file)

with open ('distCoeffs.pickle', "rb") as distCoeffs_file:
    distCoeffs = pickle.load(distCoeffs_file)

for fname in images:
    img = cv2.imread(fname)
    correctedImg = cv2.undistort(img, cameraMtx, distCoeffs, correctedImg)
    cv2.imwrite('{:>2}.jpg'.format(i), correctedImg)
    i+=1