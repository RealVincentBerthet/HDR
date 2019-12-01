import cv2 as cv
import numpy as np
import os
#import colour
#import colour_hdri


def write(path,img) :
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    cv.imwrite(path,img)
    print('Write : '+path)

####################
#   Main
###################
# Generate HDR image
img_fn = ["./sources/tuto/img3.jpg","./sources/tuto/img2.jpg","./sources/tuto/img1.jpg","./sources/tuto/img0.jpg"]
exposure_times = np.array([15.0, 2.5, 0.25, 0.0333], dtype=np.float32)
img_list = [cv.imread(fn) for fn in img_fn]

debevec=cv.createMergeDebevec()
#calibrateDebevec = cv.createCalibrateDebevec()
#responseDebevec = calibrateDebevec.process(img_list, exposure_times.copy())
img_hdr = debevec.process(img_list, exposure_times.copy())
#img_hdr =cv.imread('./output/tutorial/hdr_debevec.hdr',cv.CV_32FC3) #@TODO Loading NOK ???
#img_hdr=cv.imread('./sources/data/234/234_HDR2.hdr') # Load HDR image
write('./output/tonemap/source.hdr', img_hdr)

gamma=1.0

# OpenCV ToneMapping - https://docs.opencv.org/3.1.0/d8/d5e/classcv_1_1Tonemap.html
# Drago
tonemapper=cv.createTonemapDrago()
tonemapper.setGamma(gamma)
img_ldr= tonemapper.process(img_hdr.copy())
write('./output/tonemap/ldr_Drago_gamma_'+str(tonemapper.getGamma())+'.jpg',img_ldr*255)

# Durand
tonemapper=cv.createTonemapDurand()
tonemapper.setGamma(gamma)
img_ldr= tonemapper.process(img_hdr.copy())
write('./output/tonemap/ldr_Durand_gamma_'+str(tonemapper.getGamma())+'.jpg',img_ldr*255)

# Mantiuk
tonemapper=cv.createTonemapMantiuk()
tonemapper.setGamma(gamma)
img_ldr= tonemapper.process(img_hdr.copy())
write('./output/tonemap/ldr_Mantiuk_gamma_'+str(tonemapper.getGamma())+'.jpg',img_ldr*255)

# Reinhard
tonemapper=cv.createTonemapReinhard()
tonemapper.setGamma(gamma)
img_ldr= tonemapper.process(img_hdr.copy())
write('./output/tonemap/ldr_Reinhard_gamma_'+str(tonemapper.getGamma())+'.jpg',img_ldr*255)

# HDRI Operators
#test=colour_hdri.tonemapping_operator_logarithmic(img_hdr)
#test=hdri.tonemapping_operator_logarithmic(img_ldr)
