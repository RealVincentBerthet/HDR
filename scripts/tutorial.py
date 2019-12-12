import cv2 as cv
import numpy as np
import os

def write(path,img):
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
        
    cv.imwrite(path, img)
    print('Write : '+path)

# 1.Loading exposure images into a list
#img_fn = ["./sources/tuto/img3.jpg","./sources/tuto/img2.jpg","./sources/tuto/img1.jpg","./sources/tuto/img0.jpg"]
#exposure_times = np.array([15.0, 2.5, 0.25, 0.0333], dtype=np.float32)
# img_fn = ["./sources/data/260/DSC00260.jpg","./sources/data/260/DSC00261.jpg","./sources/data/260/DSC00262.jpg"]
# exposure_times = np.array([0.01, 0.003125, 0.03333333333], dtype=np.float32)
# img_fn = ["./sources/data/272/DSC00272.jpg","./sources/data/272/DSC00273.jpg","./sources/data/272/DSC00274.jpg"]
# exposure_times = np.array([0.0125, 0.005, 0.04], dtype=np.float32)
img_fn = ["./sources/data/269/DSC00269.jpg","./sources/data/269/DSC00270.jpg","./sources/data/269/DSC00271.jpg"]
exposure_times = np.array([0.01, 0.0025, 0.025], dtype=np.float32)
#img_fn = ["./sources/Benoit/IMG_2206.JPG","./sources/Benoit/IMG_2208.JPG","./sources/Benoit/IMG_2207.JPG"]
#exposure_times = np.array([0.001169591, 0.03030303, 0.058823529], dtype=np.float32)
img_list = [cv.imread(fn) for fn in img_fn]


alignMTB = cv.createAlignMTB()
alignMTB.process(img_list, img_list)

# 2.Merge exposures to HDR image
cal_debevec = cv.createCalibrateDebevec()
crf_debevec = cal_debevec.process(img_list, times=exposure_times)
merge_debevec = cv.createMergeDebevec()
hdr_debevec_crf = merge_debevec.process(img_list, times=exposure_times.copy(),response=crf_debevec.copy())
write('./output/tutorial/hdr_debevec_crf.hdr',hdr_debevec_crf)
hdr_debevec = merge_debevec.process(img_list, times=exposure_times.copy())
write('./output/tutorial/hdr_debevec.hdr',hdr_debevec)

cal_robertson = cv.createCalibrateRobertson()
crf_robertson = cal_robertson.process(img_list, times=exposure_times)
merge_robertson = cv.createMergeRobertson()
hdr_robertson_crf = merge_robertson.process(img_list, times=exposure_times.copy(), response=crf_robertson.copy())
write('./output/tutorial/hdr_robertson_crf.hdr',hdr_robertson_crf)
hdr_robertson = merge_robertson.process(img_list, times=exposure_times.copy())
write('./output/tutorial/hdr_robertson.hdr',hdr_robertson)

# 3.Tonemap HDR image
tonemap1 = cv.createTonemapDurand(gamma=2.2)
ldr_debevec = tonemap1.process(hdr_debevec.copy())
write('./output/tutorial/ldr_debevec.jpg',np.clip(ldr_debevec*255,0,255).astype('uint8'))
ldr_debevec = tonemap1.process(hdr_debevec_crf.copy())
write('./output/tutorial/ldr_debevec_crf.jpg',np.clip(ldr_debevec*255,0,255).astype('uint8'))

tonemap2 = cv.createTonemapDurand(gamma=1.3)
ldr_robertson = tonemap2.process(hdr_robertson.copy())
write('./output/tutorial/ldr_robertson.jpg',np.clip(ldr_robertson*255,0,255).astype('uint8'))
ldr_robertson = tonemap1.process(hdr_robertson_crf.copy())
write('./output/tutorial/ldr_robertson_crf.jpg',np.clip(ldr_robertson*255,0,255).astype('uint8'))

merge_mertens = cv.createMergeMertens()
ldr_mertens = merge_mertens.process(img_list)
write('./output/tutorial/fusion_mertens.jpg',np.clip(ldr_mertens*255,0,255).astype('uint8'))