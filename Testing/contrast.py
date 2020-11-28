import cv2

image = cv2.imread('../Mojobrazek.png')
alhpa = 50
beta = 15

adjusted = cv2.convertScaleAbs(image,alpha=alhpa,beta=beta)

cv2.imshow('fixed',adjusted)
cv2.waitKey()