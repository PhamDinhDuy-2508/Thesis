#
#
# import os
# import cv2
# import numpy as np
# import mediapipe as mp
# mp_selfie_segmentation = mp.solutions.selfie_segmentation
#
# selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)
#
# def remove() :
#     image_path = 'D:\Python\Thesis\images'
#     images = os.listdir(image_path)
#
#     image_index= 3
#     bg_image = cv2.imread(image_path+'/'+images[image_index])
#
#     image =  cv2.imread("D:\Shape_Steel_C_3.png")
#     cv2.imshow("test" , image)
#     cv2.waitKey(0)
#     frame = cv2.flip(image, 1)
#     height, width, channel = frame.shape
#
#     RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#
#     # get the result
#     results = selfie_segmentation.process(RGB)
#
#     # extract segmented mask
#     mask = results.segmentation_mask
#
#     # it returns true or false where the condition applies in the mask
#     condition = np.stack(
#         (results.segmentation_mask,) * 3, axis=-1) > 0.6
#
#     # resize the background image to the same size of the original frame
#     bg_image = cv2.resize(bg_image, (width, height))
#
#     # combine frame and background image using the condition
#     output_image = np.where(condition, frame, bg_image)
#
#     # show outputs
#     # cv2.imshow("mask", mask)
#     cv2.imshow("Output", output_image)
#     cv2.imshow("Frame", frame)
#
#     cv2.waitKey(0)
#
#     # if 'd' key is pressed then change the background image
#
# if __name__ == '__main__':
#     remove()
#
#
import cv2
import numpy as np

# Read image
img = cv2.imread('D:\Shape_steel_4.png')
hh, ww = img.shape[:2]

# threshold on white
# Define lower and uppper limits
lower = np.array([200, 200, 200])
upper = np.array([255, 255, 255])

# Create mask to only select black
thresh = cv2.inRange(img, lower, upper)

# apply morphology
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20,20))
morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
cv2.imshow("ker" , img)
cv2.waitKey(0)
# get contours
contours = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = contours[0] if len(contours) == 2 else contours[1]

# draw white contours on black background as mask
mask = np.zeros((hh,ww), dtype=np.uint8)
for cntr in contours:
    cv2.drawContours(mask, [cntr], 0, (255,255,255), -1)

# get convex hull
points = np.column_stack(np.where(thresh.transpose() > 0))
hullpts = cv2.convexHull(points)
((centx,centy), (width,height), angle) = cv2.fitEllipse(hullpts)
print("center x,y:",centx,centy)
print("diameters:",width,height)
print("orientation angle:",angle)

# draw convex hull on image
hull = img.copy()
cv2.polylines(hull, [hullpts], True, (0,0,255), 1)

# create new circle mask from ellipse
circle = np.zeros((hh,ww), dtype=np.uint8)
cx = int(centx)
cy = int(centy)
radius = (width+height)/4
cv2.circle(circle, (cx,cy), int(radius), 255, -1)


# erode circle a bit to avoid a white ring
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (6,6))
circle = cv2.morphologyEx(circle, cv2.MORPH_ERODE, kernel)

# combine inverted morph and circle
mask2 = cv2.bitwise_and(255-morph, 255-morph, mask=circle)

# apply mask to image
result = cv2.bitwise_and(img, img, mask=mask2)

# save results

cv2.waitKey(0)
cv2.destroyAllWindows()