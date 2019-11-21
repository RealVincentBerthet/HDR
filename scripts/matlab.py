import cv2 as cv
import numpy as np

####################
#   Functions
###################
def rgb2lum(imgs_rgb):
    imgs_ycbcr=[cv.cvtColor(img, cv.COLOR_BGR2YCrCb) for img in imgs_rgb]
    imgs_lum=[img[:,:,0] for img in imgs_ycbcr]
    return imgs_lum

def get_weight1(imgs_lum):
    print("get_weight1(imgs_lum)")
    return True

def get_weight2(imgs_lum):
    print("get_weight2(imgs_lum)")
    return True

def fusion_pyramid(imgs_rgb, w, lev):
    print("fusion")
    return True

def refine_weight(weight):
    print("refine weight")
    return True

def Write(img,name):
    cv.imwrite('../output/'+name+'.jpg', img)

def Show(img,name):
    cv.imshow(name,img)
    cv.waitKey(0)
    cv.destroyAllWindows()

####################
#   Main
###################
# 1.Read multi-exposed rgb image sequence (scaling to [0,1])
img_fn = ["../sources/tuto/img3.jpg","../sources/tuto/img2.jpg","../sources/tuto/img1.jpg","../sources/tuto/img0.jpg"]
imgs_rgb = [cv.imread(fn) for fn in img_fn]

# 2.Compute luminance image of rgb image sequence
imgs_lum=rgb2lum(imgs_rgb)
imgs_lum=[img/255.0 for img in imgs_lum]

# 3.Compute weight 1 using luminance distribution
w1=get_weight1(imgs_lum)

# 4.Compute weight 2 using luminance gradient
w2=get_weight2(imgs_lum)

# 5.Corporate weight 1 & weight 2 and refine weight with wlsFilter
p1 = 1
p2 = 1
w = np.power(w1,p1)*np.power(w2,p2)
w = refine_weight(w)

# 6.Fuse images using pyramid decomposition
lev=7
img_result=fusion_pyramid(imgs_rgb,w,lev)

# 7.Show and save
#Show(img_result,"result")
#Write(img_result,"result")
