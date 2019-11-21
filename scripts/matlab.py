import cv2 as cv
import numpy as np

# 1.Read multi-exposed rgb image sequence (scaling to [0,1])
img_fn = ["../sources/tuto/img3.jpg","../sources/tuto/img2.jpg","../sources/tuto/img1.jpg","../sources/tuto/img0.jpg"]
imgs_rgb = [cv.imread(fn) for fn in img_fn]

# 2.Compute luminance image of rgb image sequence
img_lum=rgb2lum(imgs_rgb)
# 3.Compute weight 1 using luminance distribution
w1=get_weight1(img_lum)
# 4.Compute weight 2 using luminance gradient
w2=get_weight2(img_lum)
# 5.Corporate weight 1 & weight 2 and refine weight with wlsFilter
p1 = 1
p2 = 1
w = np.power(w1,p1)*np.power(w2,p2)
w = refine_weight(w)
# 6.Fuse images using pyramid decomposition
lev=7
img_result=fusion_pyramid(imgs_rgb,w,lev)
# 7.Show and save
ShowAndWrite(img_result,"result")


####################
#   Functions
###################
def rgb2lum(imgs_rgb):
    img_ycrcb = cv.cvtColor(imgs_rgb, cv.COLOR_BGR2YCrCb)
    img_y = img_ycrcb[:,:,0]
    return img_y

def get_weight1(imgs_lum):
    print("get_weight1(imgs_lum)")

def get_weight2(imgs_lum):
    print("get_weight2(imgs_lum)")

def fusion_pyramid(imgs_rgb, w, lev):
    print("fusion")

def refine_weight(weight):
    print("refine weight")

def ShowAndWrite(img,name):
    cv.imwrite('../output/'+name+'.jpg', img)
    cv.imshow(name,img)
    cv.waitKey(0)
    cv.destroyAllWindows()