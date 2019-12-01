import cv2 as cv
import numpy as np
import os
#import colour
#import colour_hdri

def write8bit(img,name,dir) :
    path='../output/'+dir
    img_8bits = np.clip(img*255, 0, 255).astype('uint8')
    if not os.path.exists(path):
        os.makedirs(path)
    cv.imwrite('../output/'+dir+name+'.jpg', img_8bits)
    print('Write : '+path+name+'.jpg')

####################
#   Main
###################
# Loading images into a list
img_fn = ["../sources/tuto/img3.jpg","../sources/tuto/img2.jpg","../sources/tuto/img1.jpg","../sources/tuto/img0.jpg"]
img_list = [cv.imread(fn) for fn in img_fn]

# Create HDR with exposure fusion using Mertens 
img_hdr = cv.createMergeMertens().process(img_list)
gamma=1.0

# OpenCV ToneMapping - https://docs.opencv.org/3.1.0/d8/d5e/classcv_1_1Tonemap.html
# Drago
tonemapper=cv.createTonemapDrago()
tonemapper.setGamma(gamma)
img_tone= tonemapper.process(img_hdr.copy())
write8bit(img_tone,'tonemapDrago_gamma_'+str(tonemapper.getGamma()),'tonemap/')

# Durand
tonemapper=cv.createTonemapDurand()
tonemapper.setGamma(gamma)
img_tone= tonemapper.process(img_hdr.copy())
write8bit(img_tone,'tonemapDurand_gamma_'+str(tonemapper.getGamma()),'tonemap/')

# Mantiuk
tonemapper=cv.createTonemapMantiuk()
tonemapper.setGamma(gamma)
img_tone= tonemapper.process(img_hdr.copy())
write8bit(img_tone,'tonemapMantiuk_gamma_'+str(tonemapper.getGamma()),'tonemap/')

# Reinhard
tonemapper=cv.createTonemapReinhard()
tonemapper.setGamma(gamma)
img_tone= tonemapper.process(img_hdr.copy())
write8bit(img_tone,'tonemapReinhard_gamma_'+str(tonemapper.getGamma()),'tonemap/')

# HDRI
#test=colour_hdri.tonemapping_operator_logarithmic(img_hdr)
#test=hdri.tonemapping_operator_logarithmic(img_tone)
#write8bit(test,'test'+str(tonemapper.getGamma()),'tonemap/')