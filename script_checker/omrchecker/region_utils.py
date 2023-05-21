"""
print(roi)
The code in here is used to get the radius of an image
The first value (405) represents the x-coordinate of the top-left corner of the ROI.
The second value (149) represents the y-coordinate of the top-left corner of the ROI.
The third value (636) represents the width of the ROI.
The fourth value (407) represents the height of the ROI.

ROI: (242, 314, 58, 141)
ROI: (243, 483, 59, 142)
ROI: (331, 312, 58, 143)
ROI: (334, 483, 55, 143)
ROI: (421, 312, 55, 143)
ROI: (421, 482, 58, 142)
ROI: (508, 313, 55, 142)
ROI: (507, 482, 57, 142)
ROI: (594, 311, 56, 142)
ROI: (593, 482, 59, 141)
"""

import cv2

im = cv2.imread("image.jpg")
# Resize the image to 700 by 700
im = cv2.resize(im, (700, 700))

regions = {}  # Dictionary to store multiple regions

while True:
    # Select ROI
    roi = cv2.selectROI(im)

    if roi == (0, 0, 0, 0):
        # If ROI selection is canceled (all values are zero), exit the loop
        break

    print("ROI:", roi)

    im_cropped = im[int(roi[1]):int(roi[1] + roi[3]),
                 int(roi[0]):int(roi[0] + roi[2])]

    # Store the cropped image in the dictionary with the ROI as the key
    regions[roi] = im_cropped

    cv2.imshow("Cropped Image", im_cropped)
    cv2.waitKey(0)

cv2.destroyAllWindows()

# Print all regions
for roi, cropped_image in regions.items():
    print("ROI:", roi)
    print("Cropped Image Shape:", cropped_image.shape)
