import cv2 as cv
import numpy as np
import os

####################
#   Functions
###################
def write(path,img):
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    if len(img)==0:
        print('error : img length empty')
    elif len(img)<=1:
        cv.imwrite(path, img)
        print('Write : '+path)
    else:    
        for index, item in enumerate(img):
            tpath=os.path.dirname(path)+'/'+str(index)+'_'+os.path.basename(path)
            cv.imwrite(tpath, item)
            print('Write : '+tpath)

def rgb2lum(imgs_rgb):
    imgs_ycbcr=[cv.cvtColor(img, cv.COLOR_BGR2YCrCb) for img in imgs_rgb]
    imgs_lum=[img[:,:,0] for img in imgs_ycbcr]
    return imgs_lum

def get_weight1(imgs_lum):
    H=imgs_lum[0].shape[0]
    W=imgs_lum[0].shape[1]
    N=len(imgs_lum)
    weight=np.zeros((H,W,N))
    
    #compute mean value of non exposed intensity region
    means=[np.mean(img) for img in imgs_lum]

    #compute sigma value of non exposed intensity region
    sigmas=np.zeros(N)
    sigmas[0]=(means[1]-means[0])/2
    for n in range(1,N-1) :
        sigmas[n]=(means[n+1]-means[n-1])/4
    sigmas[N-1]=(means[N-1]-means[N-2])/2

    #compute weight map of each image in luminance image sequence
    for n in range(0,N) :
        weight[:,:,n] =np.exp(-0.5*(np.power(imgs_lum[n]-(1-means[n]),2)/sigmas[n]/sigmas[n]))
    
    return weight

def get_weight2(imgs_lum):
    H=imgs_lum[0].shape[0]
    W=imgs_lum[0].shape[1]
    N=len(imgs_lum)
    img_hists=np.zeros((256,N))

    for n in range(0,N) :
        img=np.uint8(255*imgs_lum[n])
        img_hists[:,n], _ = np.histogram(img.ravel(),256,[0,256])

    #img_hists =img_hists/np.matlib.repmat(sum(img_hists,0)) #@TODO
    #img_hists =img_hists/repmat(sum(img_hists,1),[256 1]) #matlab
    

    gradient_for_ij=np.zeros((H,W,N))
    eps=np.exp(-12)
    for n in range(0,N) :
        for i in range(0,H) :
            for j in range (0,W) :
                idx=np.ceil(255*imgs_lum[i,j,n])+1
                gradient_for_ij[i,j,n]=1/img_hists[idx,n]+eps
    
    
    gradient_for_ij_max=np.zeros((H,W))

    for n in range(0,N) :
        gradient_for_ij_max=np.sum(gradient_for_ij_max,gradient_for_ij[:,:,n])+eps

    #weight = gradient_for_ij./repmat(gradient_for_ij_max,[1 1 N]); #@TODO
    
    return True

def refine_weight(weight):
    H=weight[0].shape[0]
    W=weight[0].shape[1]
    N=len(weight)
    w = np.zeros((H,W,N))

    for n in range(0,N) :
        w[:,:,n] = cv.GaussianBlur(w[:,:,n],ksize=(5,5),sigmaX=5)
    
    return w

def gaussian_kernel(size=5, sigma=0.4):
    return cv.getGaussianKernel(ksize=size, sigma=sigma)


def image_reduce(image):
    kernel = gaussian_kernel()
    out_image = cv.filter2D(image, cv.CV_8UC3, kernel)
    out_image = cv.resize(out_image, None, fx=0.5, fy=0.5)
    return out_image


def image_expand(image):
    kernel = gaussian_kernel()
    out_image = cv.resize(image, None, fx=2, fy=2)
    out_image = cv.filter2D(out_image, cv.CV_8UC3, kernel)
    return out_image


def gaussian_pyramid(img, depth):
    G = img.copy()
    gp = [G]
    for i in range(depth):
        G = image_reduce(G)
        gp.append(G)
    return gp


def laplacian_pyramid(img, depth):
    gp = gaussian_pyramid(img, depth+1)
    lp = [gp[depth-1]]
    for i in range(depth-1, 0, -1):
        GE = image_expand(gp[i])
        L = cv.subtract(gp[i-1], GE)
        lp = [L] + lp
    return lp


def reconstruct_pyr(pyramid):
    depth = len(pyramid)
    collapsed = pyramid[depth-1]
    for i in range(depth-2, -1, -1):
        collapsed = cv.add(image_expand(collapsed), pyramid[i])
    return collapsed


def fusion_pyramid(imgs_rgb, w, lev):
    H=imgs_rgb[0].shape[0]
    W=imgs_rgb[0].shape[1]
    C=imgs_rgb[0].shape[2]
    N=len(imgs_rgb)

    #  # normalize weight
    w = w +  np.exp(-12) # avoid division by zero


   # w=w/np.tile()

    # w = w/np.tile(np.sum(w,axis=2), (1, 1, N))

    # # create empty pyramid
    # pyr = gaussian_pyramid(np.zeros(H,W,C),lev)

    # # multiresolution blending
    # for n in range(N):
    #     # construct pyramid for each image
    #     pyrW = gaussian_pyramid(w[:,:,n], lev)
    #     pyrI = laplacian_pyramid(imgs_rgb[:,:,:, n], lev)

    #     for l in range(lev):
    #         w = np.tile(pyrW[:,:,l], (1, 1, C))
    #         pyr[:,:,:,l] = pyr[:,:,:,l] + w * pyrI[:,:,:,l]

    # reconstruct
    # result = reconstruct_pyr(pyr)
    return True

####################
#   Main
###################
# 1.Read multi-exposed rgb image sequence - OK
#img_fn = ["../sources/tuto/img3.jpg","../sources/tuto/img2.jpg","../sources/tuto/img1.jpg","../sources/tuto/img0.jpg"]
img_fn = ["./sources/image_sequence/A.png","./sources/image_sequence/B.png","./sources/image_sequence/C.png","./sources/image_sequence/D.png"]
imgs_rgb = [cv.imread(fn) for fn in img_fn]

# 2.Compute luminance image of rgb image sequence - OK
imgs_lum=rgb2lum(imgs_rgb)
write('./output/exposure/rgb2lum.jpg',imgs_lum)
imgs_lum=[img/255.0 for img in imgs_lum] # scaling to [0,1]

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
#write('./output/result.jpg',img_result)
