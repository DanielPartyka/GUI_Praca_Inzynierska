import cv2
import scipy.io
import numpy as np
from PIL import Image

img = cv2.imread('../Images/gifgit.png')
h, w, c = img.shape

alhpa = 1.0
beta = 20
image = cv2.convertScaleAbs(img,alpha=alhpa,beta=beta)

window_name = 'Image'

mat = scipy.io.loadmat('../MatReading/block01CordDef.mat')
nColumns = mat['block01CordDef']['nColumns'][0][0][0][0]
nRows = mat['block01CordDef']['nRows'][0][0][0][0]
""""
    (x0, y0) (x1, y1)
"""""
nColumns = mat['block01CordDef']['nColumns'][0][0][0][0]
nRows = mat['block01CordDef']['nRows'][0][0][0][0]

# x0 left corner green block
start_x0_cord_green = 0
# x0 left corner red block
start_x0_cord_red = 14
# y0 start top margin
y0 = 0
# x1 cord
x1_cord = 0

padding = 4

width_of_block = int(w / nColumns)
height_of_block = int((h+(nRows*5)) / nRows)

print(height_of_block)

thickness = 1
iteration = 0
block_width = width_of_block
block_width_red = width_of_block + start_x0_cord_red

for rows in range(0,nRows):
    iteration += 1
    if iteration > 1:
        y0 += height_of_block-5
        block_width = width_of_block
        start_x0_cord_green = 0
        start_x0_cord_red = 15
        block_width_red = width_of_block + start_x0_cord_red
    for columns in range(0,nColumns):
        if iteration % 2 != 0:
            image = cv2.rectangle(image,(start_x0_cord_green + padding,y0),(block_width,height_of_block+y0), (0,255,0), thickness)
            start_x0_cord_green += width_of_block
            block_width += width_of_block
        else:
            image = cv2.rectangle(image, (start_x0_cord_red + padding, y0), (block_width_red, height_of_block + y0), (0,0,255),thickness)
            start_x0_cord_red += width_of_block
            block_width_red += width_of_block

cv2.imshow(window_name, image)
cv2.waitKey(0)
cv2.destroyAllWindows()