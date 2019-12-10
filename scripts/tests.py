import cv2 as cv
import numpy as np



def gaussian_kernel(size=5, sigma=0.4):
    return cv.getGaussianKernel(ksize=size, sigma=sigma)


def image_reduce(image):
    kernel = gaussian_kernel()
    out_image = cv.filter2D(image, cv.CV_8UC3, kernel)
    out_image = cv.resize(out_image, None, fx=0.5, fy=0.5)
    return out_image

def image_reduce_w(image):
    kernel = gaussian_kernel()
    out_image = cv.filter2D(image, -1, kernel)
    out_image = cv.resize(out_image, None, fx=0.5, fy=0.5)
    return out_image

def image_expand(image):
    kernel = gaussian_kernel()
    out_image = cv.resize(image, None, fx=2, fy=2)
    out_image = cv.filter2D(out_image, cv.CV_8UC3, kernel)
    return out_image

def gaussian_pyramid_w(img, depth):
    G = img.copy()
    gp = [G]
    for i in range(depth):
        G = image_reduce_w(G)
        gp.append(G)
    return gp

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
        # print("GE" + str(GE.shape))
        # print("gp[i-1]" + str(gp[i - 1].shape))
        # dimx = gp[i - 1].shape[1]
        # dimy = gp[i - 1].shape[0]
        # print(str(dimx)+" "+str(dimy))
        # print("GE0" + str(GE[:,:,1].shape))
        # GE[:,:,0] = cv.resize(GE[:,:,0], (dimx,dimy))
        # GE[:,:,1] = cv.resize(GE[:,:,1], (dimx,dimy))
        # GE[:,:,2] = cv.resize(GE[:,:,2], (dimx,dimy))


        L = cv.subtract(gp[i-1], GE)
        lp = [L] + lp
    return lp


def reconstruct_pyr(pyramid):
    depth = len(pyramid)
    collapsed = pyramid[depth-1]
    for i in range(depth-2, -1, -1):
        # print("collapsed" + str(image_expand(collapsed).shape))
        # print("pyr" + str(pyramid[i].shape))

        collapsed = cv.add(image_expand(collapsed), pyramid[i], None, None, cv.CV_8UC3)
    return collapsed


def fusion_pyramid(imgs_rgb, w, lev):
    H = imgs_rgb[0].shape[0]
    W = imgs_rgb[0].shape[1]
    C = imgs_rgb[0].shape[2]
    N = len(imgs_rgb)

    #  # normalize weight
    w = w + np.exp(-12)  # avoid division by zero
    sum = np.sum(w, axis=2)
    sum = np.expand_dims(sum, 2)
    w = w / np.tile(sum, (1, 1, N))

    # create empty pyramid
    blank_image = np.zeros((H, W, C), np.uint8)
    pyr = gaussian_pyramid(blank_image, lev)

    # multiresolution blending
    for n in range(N):
        # construct pyramid for each image
        pyrW = gaussian_pyramid_w(w[:, :, n], lev)
        pyrI = laplacian_pyramid(imgs_rgb[n], lev)

        for l in range(lev):
            pyrW[l] = np.expand_dims(pyrW[l], 2)
            ww = np.tile(pyrW[l], (1, 1, C))
            print(l)
            print(w.shape)
            print(pyrI[l].shape)
            pyr[l] = pyr[l] + ww * pyrI[l]

    # reconstruct
    print("héé")
    print(len(pyr))
    result = reconstruct_pyr(pyr)

    return result

#------------------------------------------------------------------------------------



img_fn = ["./sources/lena.png"]
imgs_rgb = [cv.imread(fn) for fn in img_fn]
H = imgs_rgb[0].shape[0]
W = imgs_rgb[0].shape[1]
C = imgs_rgb[0].shape[2]

weight = np.zeros((H, W, 4))
weight[:,:,:] = 0.1

lev = 5

print(weight.shape)

img_result=fusion_pyramid(imgs_rgb,weight,lev)
print(img_result.shape)
cv.imwrite("a.png", img_result)
#
# test = np.zeros((5, 5, 3))
# test[:,:,0]=0.2
# print(test.shape)
# sum = np.sum(test, axis=2)
# print(sum.shape)
# sum = np.expand_dims(sum, 2)
# print(sum.shape)
# test = np.tile(sum, (1, 1, 10))
# print(test.shape)
# print(np.tile(np.sum(test, axis=2), (1, 1, 3)))