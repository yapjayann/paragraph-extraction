# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 17:11:55 2023

@author: Dell
"""
#Task b: Paragraphs Extraction
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the image 
img = cv2.imread('005.png')

#Remove the graphics
#since the graphics are coloured, can filter them out before convert to grayscale
# Define HSV range for colors to be removed
lower_bound = np.array([1, 1, 1])
upper_bound = np.array([254, 254, 254])

# Convert BGR image to HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Create a mask to filter out colors
color_mask = cv2.inRange(hsv, lower_bound, upper_bound)

# Apply the mask to remove colored areas
img_no_color = cv2.bitwise_and(img, img, mask=~color_mask)

# Convert to grayscale
gray = cv2.cvtColor(img_no_color, cv2.COLOR_BGR2GRAY)

# Apply adaptive thresholding
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv2.THRESH_BINARY_INV, 41, 8)

# Get contours (used for detecting tables)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_NONE)

# Create a mask for filling the table boxes
table_mask = np.zeros_like(gray)

# Fill only the table boxes in the mask
cv2.drawContours(table_mask, contours, -1, (255), thickness=cv2.FILLED)

# Create a copy of the original image to fill only the table boxes
img_with_tables_filled = img.copy()

# Fill only the table boxes in the original image
img_with_tables_filled[table_mask == 255] = 255

# Convert the filled image to grayscale
gray_filled = cv2.cvtColor(img_with_tables_filled, cv2.COLOR_BGR2GRAY)

# Now we have removed the tables

# Apply adaptive thresholding again
thresh_filled = cv2.adaptiveThreshold(gray_filled, 255,
                                      cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv2.THRESH_BINARY_INV, 41, 8)

# Closing morphological operation to close gaps between letters and words
kernel = np.ones((35, 35), np.uint8)
closing = cv2.morphologyEx(thresh_filled, cv2.MORPH_CLOSE, kernel)

# Find contours again after closing
contours_after_closing, _ = cv2.findContours(closing, cv2.RETR_EXTERNAL,
                                             cv2.CHAIN_APPROX_NONE)

# Filter contours after closing
filtered_contours_after_closing = [
    contour for contour in contours_after_closing
    if cv2.contourArea(contour) > 500
]

# Sort contours based on their y-coordinate
sorted_contours = sorted(filtered_contours_after_closing,
                         key=lambda c: cv2.boundingRect(c)[1])

# Draw rectangles around paragraphs on the copied image
img_with_rectangles = img.copy()
for contour in sorted_contours:
    rect = cv2.minAreaRect(contour)
    box = cv2.boxPoints(rect)
    box = np.intp(box)
    cv2.drawContours(img_with_rectangles, [box], 0, (255, 0, 255), 3)

# Path to a separate folder to save extracted paragraphs (change if needed)
path = "extractions"

# Save each paragraph as a separate image
for i, contour in enumerate(sorted_contours):
    x, y, w, h = cv2.boundingRect(contour)
    paragraph = img[y:y + h, x:x + w]
    cv2.imwrite(f'{path}\\paragraph_{i+1}.png', paragraph)

# To visualize the results
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title('Original image')
plt.show()

plt.imshow(thresh, cmap='gray')
plt.title('Thresholded image')
plt.show()

plt.imshow(closing, cmap='gray')
plt.title('After Closing')
plt.show()

plt.imshow(cv2.cvtColor(img_with_rectangles, cv2.COLOR_BGR2RGB))
plt.title('Detected Paragraphs')
plt.show()

