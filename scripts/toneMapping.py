import cv2 as cv
import numpy as np
import os
import hdri_operators

print('OpenCV v'+str(cv.__version__))

def write(path,img) :
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    cv.imwrite(path,img)
    print('Write : '+path)

####################
#   Main
###################
# Load HDR image
img_hdr =cv.imread('./output/tutorial/hdr_debevec.hdr',cv.IMREAD_ANYCOLOR | cv.IMREAD_ANYDEPTH)
#img_hdr=cv.imread('./sources/data/234/234_HDR2.hdr',cv.IMREAD_ANYCOLOR | cv.IMREAD_ANYDEPTH)
write('./output/tonemap/source.hdr', img_hdr)

gamma=1.0

# OpenCV ToneMapping - https://docs.opencv.org/3.1.0/d8/d5e/classcv_1_1Tonemap.html
# Drago
tonemapper=cv.createTonemapDrago()
tonemapper.setGamma(gamma)
img_ldr= tonemapper.process(img_hdr.copy())
write('./output/tonemap/ldr_Drago_gamma_'+str(tonemapper.getGamma())+'.jpg',np.clip(img_ldr*255,0,255).astype('uint8'))

# Durand
tonemapper=cv.createTonemapDurand()
tonemapper.setGamma(gamma)
img_ldr= tonemapper.process(img_hdr.copy())
write('./output/tonemap/ldr_Durand_gamma_'+str(tonemapper.getGamma())+'.jpg',np.clip(img_ldr*255,0,255).astype('uint8'))

# Mantiuk
tonemapper=cv.createTonemapMantiuk()
tonemapper.setGamma(gamma)
img_ldr= tonemapper.process(img_hdr.copy())
write('./output/tonemap/ldr_Mantiuk_gamma_'+str(tonemapper.getGamma())+'.jpg',np.clip(img_ldr*255,0,255).astype('uint8'))

# Reinhard
tonemapper=cv.createTonemapReinhard()
tonemapper.setGamma(gamma)
img_ldr= tonemapper.process(img_hdr.copy())
write('./output/tonemap/ldr_Reinhard_gamma_'+str(tonemapper.getGamma())+'.jpg',np.clip(img_ldr*255,0,255).astype('uint8'))

# Operator Gamma
img_ldr=hdri_operators.tonemapping_operator_gamma(img_hdr.copy())
write('./output/tonemap/ldr_hdri_gamma.jpg',img_ldr)

# Operator exponential
img_ldr=hdri_operators.tonemapping_operator_exponential(img_hdr.copy())
write('./output/tonemap/ldr_hdri_exponential.jpg',np.clip(img_ldr*255,0,255).astype('uint8'))

# Operator Logarithmic
img_ldr=hdri_operators.tonemapping_operator_logarithmic(img_hdr.copy())
write('./output/tonemap/ldr_hdri_logarithmic.jpg',np.clip(img_ldr*255,0,255).astype('uint8'))