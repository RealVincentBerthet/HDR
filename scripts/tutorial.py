import cv2 as cv
import numpy as np
import os

def write8bit(img,name,dir) :
    path='../output/'+dir
    img_8bits = np.clip(img*255, 0, 255).astype('uint8')
    if not os.path.exists(path):
        os.makedirs(path)
    cv.imwrite('../output/'+dir+name+'.jpg', img_8bits)
    print('Write : '+path+name+'.jpg')

# 1.Loading exposure images into a list
img_fn = ["../sources/tuto/img3.jpg","../sources/tuto/img2.jpg","../sources/tuto/img1.jpg","../sources/tuto/img0.jpg"]
img_list = [cv.imread(fn) for fn in img_fn]
exposure_times = np.array([15.0, 2.5, 0.25, 0.0333], dtype=np.float32)

# 2.Merge exposures to HDR image
merge_debevec = cv.createMergeDebevec()
hdr_debevec = merge_debevec.process(img_list, times=exposure_times.copy())
merge_robertson = cv.createMergeRobertson()
hdr_robertson = merge_robertson.process(img_list, times=exposure_times.copy())

# 3.Tonemap HDR image
tonemap1 = cv.createTonemapDurand(gamma=2.2)
res_debevec = tonemap1.process(hdr_debevec.copy())
tonemap2 = cv.createTonemapDurand(gamma=1.3)
res_robertson = tonemap2.process(hdr_robertson.copy())

# 4.Exposure fusion using Mertens
merge_mertens = cv.createMergeMertens()
res_mertens = merge_mertens.process(img_list)

# 5.Estimate camera response function (CRF)
cal_debevec = cv.createCalibrateDebevec()
crf_debevec = cal_debevec.process(img_list, times=exposure_times)
hdr_debevec = merge_debevec.process(img_list, times=exposure_times.copy(), response=crf_debevec.copy())
cal_robertson = cv.createCalibrateRobertson()
crf_robertson = cal_robertson.process(img_list, times=exposure_times)
hdr_robertson = merge_robertson.process(img_list, times=exposure_times.copy(), response=crf_robertson.copy())

# 6.Convert datatype to 8-bit and save
write8bit(res_debevec,'ldr_debevec','tutorial/')
write8bit(res_robertson,'res_robertson','tutorial/')
write8bit(res_mertens,'res_mertens','tutorial/')
