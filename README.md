# Python Paragraph Extractor
## Introduction
For this program, the goal is to develop a program capable of identifying and extracting paragraphs from captured images of multiple research papers, followed by arranging them in the correct sequence. Additionally, the program must ignore existing tables and graphics which should not be considered as paragraphs. The program contains multiple functions to separate and extract the paragraphs, which include HSV filtering, object masking, adaptive thresholding, contour detection, contour filtering by area, morphological operation (closing), rectangle drawing over regions of interest, and extractions of detected regions. OpenCV library is required for the program to work; you can install by entering `pip install opencv-python` in your IPython console.

## Methodology
 ![image](https://github.com/user-attachments/assets/f959bb9b-9607-40b8-b50e-795bfe7d92bf)

The following diagram illustrates the steps used to extract the paragraphs. 

## Step-by-step explanation
1)	Image Loading
The image file is read.
2)	Graphics Removal
In this step, the HSV (Hue, Saturation, Value) range is defined to filter out the coloured graphics. The graphics are converted to HSV, and a mask is created to remove them. 
3)	Convert to Grayscale
After removing coloured graphics, the image can be converted to grayscale. Converting the image to grayscale simplifies the image data, reducing it from three color channels (Red, Green, Blue) to a single channel. This makes the image easier to process and analyze.
4)	Table Detection and Removal
The next step involves filtering out the tables. Adaptive thresholding is applied to the greyscale image. Contour detection is used to detect the outer boundaries of the tables. A mask is created, and the tables are then filled with white as they are to be ignored in paragraph extraction.
5)	Morphological Closing Operation (Closing Gaps)
After applying adaptive thresholding again, closing morphological operation (dilation then erosion) is applied to close gaps between letters and words. This ensures the whole paragraphs are detected correctly instead of individual letters/words.
6)	Find Paragraph Contours and Sort Based on Y-coordinates
After closing, contours of the paragraphs are detected again. Contours are filtered by area, keeping only contours greater than 500. The contours are then sorted based on Y-coordinates (top to bottom). 
7)	Draw Rectangles Around Paragraph Contours
Each detected paragraph contour is enclosed in a rectangle. This helps in visualizing the detected paragraphs and serves as a precursor to the extraction step.
8)	Extract the Paragraphs and Save as Separate Images
The regions of the image enclosed by the bounding rectangles are extracted as separate images in a specified folder “extraction”.
9)	Visualization
The final step involves visualizing the results using matplotlib, showing the transformation of the image and correctly extracted paragraphs.

