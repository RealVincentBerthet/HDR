import cv2 as cv
import numpy as np
# Loading exposure images into a list
img_fn = ["exposure_fusion/samples/peyrou_over.jpg", "exposure_fusion/samples/peyrou_under.jpg", "exposure_fusion/samples/peyrou_over.jpg"]
img_list = [cv.imread(fn) for fn in img_fn]
#exposure_times = np.array([15.0, 2.5, 0.25], dtype=np.float32)


# Exposure fusion using Mertens
merge_mertens = cv.createMergeMertens()
res_mertens = merge_mertens.process(img_list)

# Convert datatype to 8-bit and save
res_mertens_8bit = np.clip(res_mertens*255, 0, 255).astype('uint8')
cv.imwrite("output/fusion_mertens.jpg", res_mertens_8bit)