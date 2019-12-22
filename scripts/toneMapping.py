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
#img_hdr =cv.imread('./output/tutorial/hdr_debevec.hdr',cv.IMREAD_ANYCOLOR | cv.IMREAD_ANYDEPTH)
img_hdr=cv.imread('./sources/data/266/266_HDR2.hdr',cv.IMREAD_ANYCOLOR | cv.IMREAD_ANYDEPTH)
write('./output/tonemap/source.hdr', img_hdr)

gamma=1.0
saturation=1.0
l=[255]
#l=[255,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500,1600,1700,1800,1900,2000]

for lum in l :
    # OpenCV ToneMapping - https://docs.opencv.org/3.1.0/d8/d5e/classcv_1_1Tonemap.html
    # Drago
    tonemapper=cv.createTonemapDrago()
    tonemapper.setGamma(gamma)
    tonemapper.setSaturation(saturation)
    img_ldr= tonemapper.process(img_hdr.copy())
    write('./output/tonemap/ldr_Drago_gamma_'+str(tonemapper.getGamma())+'_satu_'+str(tonemapper.getSaturation())+'_lum_'+str(lum)+'.jpg',np.clip(img_ldr*lum,0,255).astype('uint8'))

    # Durand
    tonemapper=cv.createTonemapDurand()
    tonemapper.setGamma(gamma)
    tonemapper.setSaturation(saturation)
    img_ldr= tonemapper.process(img_hdr.copy())
    write('./output/tonemap/ldr_Durand_gamma_'+str(tonemapper.getGamma())+'_satu_'+str(tonemapper.getSaturation())+'_lum_'+str(lum)+'.jpg',np.clip(img_ldr*lum,0,255).astype('uint8'))

    # Mantiuk
    tonemapper=cv.createTonemapMantiuk()
    tonemapper.setGamma(gamma)
    tonemapper.setSaturation(saturation)
    img_ldr= tonemapper.process(img_hdr.copy())
    write('./output/tonemap/ldr_Mantiuk_gamma_'+str(tonemapper.getGamma())+'_satu_'+str(tonemapper.getSaturation())+'_lum_'+str(lum)+'.jpg',np.clip(img_ldr*lum,0,255).astype('uint8'))

    # Reinhard
    tonemapper=cv.createTonemapReinhard()
    tonemapper.setGamma(gamma)
    tonemapper.setLightAdaptation(0.75)
    img_ldr= tonemapper.process(img_hdr.copy())
    write('./output/tonemap/ldr_Reinhard_gamma_'+str(tonemapper.getGamma())+'_light_'+str(tonemapper.getLightAdaptation())+'_lum_'+str(lum)+'.jpg',np.clip(img_ldr*lum,0,255).astype('uint8'))

    # Operator Gamma
    img_ldr=hdri_operators.tonemapping_operator_gamma(img_hdr.copy(),gamma,1.0)
    write('./output/tonemap/ldr_hdri_gamma_'+str(gamma)+'_lum_'+str(lum)+'.jpg',np.clip(img_ldr*lum,0,255).astype('uint8'))

    # Operator exponential
    img_ldr=hdri_operators.tonemapping_operator_exponential(img_hdr.copy())
    write('./output/tonemap/ldr_hdri_exponential_lum_'+str(lum)+'.jpg',np.clip(img_ldr*lum,0,255).astype('uint8'))

    # Operator Logarithmic
    img_ldr=hdri_operators.tonemapping_operator_logarithmic(img_hdr.copy())
    write('./output/tonemap/ldr_hdri_logarithmic_lum_'+str(lum)+'.jpg',np.clip(img_ldr*lum,0,255).astype('uint8'))