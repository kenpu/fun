import cv
import Image

cam = cv.CaptureFromCAM(0)

# Get CV image
cv_im = cv.QueryFrame(cam)
size = cv.GetSize(cv_im)

# Convert to 
(r, g, b) = [cv.CreateImage(size, cv_im.depth, 1) for i in range(3)]
cv.Split(cv_im, b, g, r, None)
cv.Merge(r, g, b, None, cv_im)

pil_im = Image.fromstring('RGB', size, cv_im.tostring())
pil_im.show()

del cam
