# HDR
*21/10/19*

## HVS
The **dynamic range** is a dimensionless quantity that can be used to refer to several different physical measures
* For a display, this is the ratio of the **maximum** and **minimum** luminance that it is capable of emitting

* For an image this is the ratio of the **largets** and **smallest** pixel value

Current display devices (CRT, LCD), are not able to reproduce a range of luminance near the capability of the HVS. Real world environments contain a range of illumination much larger that can be represented by 8bit images (2 orders of magnitude). HVS is able to adapt to lighting conditions varying by nearly 10 orders of magnitude.

A human can perceive approximately 46.5 stops, this ratio is called **Static Contrast Range**. At any given time the eye can only see a range of 10 stops of light called Dynamic Contrast Range (about 20 stops in shadow). HDR camera 14-18 fstop claimed to 4k capture

## HDR image capture

**HDR scenes can be capture :**
* From **Virtual scenes** by rendering

* Using current sensor technology by **taking multiple exposures** with varying exposure times and by combining them to form a single image **assuming the knowledge of the CRF**


**CRF unknown :** 

* CRF can be estimate (Debevec and Malik)

* Can use Exposure Fusion (Mertens) method to fuse an exposure bracketed into a high quality LDR image **without generating an HDR image**


**Camera Response Function** model to overall process by which the **irradiance** of an image point is converted to n image **brightness**

**Irradiance :** is the radiant flux arriving from all possible directions per unit of area (power incident)

**Radiance :** Is the flux leaving a point on a surface (power emitted)

**Brigthness :** Is the perceived luminance of an object

EMoR 4 coeff to capture more than 99.5 % of the energy

**Exposure fusion :** Differently exposed images are fused using a Laplacian decomposition of the images and a Gaussian pyramid of the weight maps, which represent measures such as constrast saturation

## HDR image formats

**Output referred :** The data stored depends on the output devices which are, for most of them low in dynamic range

**Scene referred :** We aim to store data as close as possible to the real scene, ie independent of the display but depending on the camera OETF (converts the linear scene light into a signal) characteristic. A transformation called tone mapping is required to map the data to the specificity of the output

**\*.hdr :** Each pixel is stored as 4 bytes (32 bits/pixels : RGBE). The pixel data may be stored uncompressed or using a straightforward run length encoding scheme

## Tone Mapping

Tone Mapping is the **process of reducing the dynamic range** of an image for display.

From scene referred image to display referred image with different intents :
* **Reproducing the visual scenes** as faithfully as possible (by mapping colors to a restricted color space)
* **Simulating the limitations and properties** of the visual system
* **Providing the best subjective quality**

Global or local operators (TMO) based on **photoreceptor models** , **illumination and relectance separation**