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
    #@TODO verifier resultat avec les meme image sur matalab

    H=imgs_lum[0].shape[0]
    W=imgs_lum[0].shape[1]
    N=len(imgs_lum)
    weight=np.zeros((H,W,N))
    
    #compute mean value of non exposed intensity region
    means=np.mean(imgs_lum)
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
        #cv.calcHist([img],[0],None,[256],[0,256]) #OK
        #TODO WIP img_hists[:,n]=cv.calcHist([img],[0],None,[256],[0,256])
        

    return True


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
    print("fusion")
    [H, W, C, N] = imgs_rgb.shape;

    # normalize weight
    w = w + 1e-12 # avoid division by zero
    w = w/np.tile(np.sum(w,axis=2), (1, 1, N))

    # create empty pyramid
    pyr = gaussian_pyramid(np.zeros(H,W,C),lev)

    # multiresolution blending
    for n in range(N):
        # construct pyramid for each image
        pyrW = gaussian_pyramid(w[:,:,n], lev)
        pyrI = laplacian_pyramid(imgs_rgb[:,:,:, n], lev)

        for l in range(lev):
            w = np.tile(pyrW[:,:,l], (1, 1, C))
            pyr[:,:,:,l] = pyr[:,:,:,l] + w * pyrI[:,:,:,l]

    # reconstruct
    result = reconstruct_pyr(pyr)

    return result

def refine_weight(weight):
    print("refine weight")
    return True

def write(img,name):
    if len(img)==0:
        print('error : img length empty')
    elif len(img)<=1:
        cv.imwrite('../output/'+name+'.jpg', img)
        print('Write : '+name+'.jpg')
    else:    
        for index, item in enumerate(img):
            cv.imwrite('../output/'+name+'_'+str(index)+'.jpg', item)
            print('Write : '+name+'_'+str(index)+'.jpg')

def show(img,name):
    cv.imshow(name,img)
    cv.waitKey(0)
    cv.destroyAllWindows()

####################
#   Main
###################
# 1.Read multi-exposed rgb image sequence
img_fn = ["../sources/tuto/img3.jpg","../sources/tuto/img2.jpg","../sources/tuto/img1.jpg","../sources/tuto/img0.jpg"]
imgs_rgb = [cv.imread(fn) for fn in img_fn]

# 2.Compute luminance image of rgb image sequence
imgs_lum=rgb2lum(imgs_rgb)
write(imgs_lum,'rgb2lum')
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
#show(img_result,"result")
#write(img_result,"result")
