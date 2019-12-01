import cv2 as cv
import numpy as np
import os

def write(path,img) :
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    cv.imwrite(path,img)
    print('Write : '+path)

####################
#   Main
###################
# Generate HDR image
img_fn = ["../sources/tuto/img3.jpg","../sources/tuto/img2.jpg","../sources/tuto/img1.jpg","../sources/tuto/img0.jpg"]
exposure_times = np.array([15.0, 2.5, 0.25, 0.0333], dtype=np.float32)
img_list = [cv.imread(fn) for fn in img_fn]

debevec=cv.createMergeDebevec()
calibrateDebevec = cv.createCalibrateDebevec()
img_hdr = debevec.process(img_list, exposure_times.copy())
write('../output/tonemapInverse/hdrDebevec.hdr',img_hdr)

