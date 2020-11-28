import numpy as np
from PIL import Image, ImageEnhance
import cv2


image_o = Image.open('../Images/SBC_2014-12-05_13h20m14_19726142_5µm_AR42_S_0037.tif')

im = image_o.crop((2766,7258,3688,8165))

im.save('Image.png')

imadz = cv2.imread('Image.png')[...,::-1]

alhpa = 50
beta = 15

adjusted = cv2.convertScaleAbs(imadz,alpha=alhpa,beta=beta)

cv2.imshow('fixed',adjusted)
cv2.waitKey()