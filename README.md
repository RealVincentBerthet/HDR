# HDR

By *BERTHET Vincent & QUERO Benoit*

*OpenCV v3.1.0 has been used, see [conda configuration file ](./conda/linux.yml)for dependencies*


![preview](./output/hdr.jpg)
![](./output/hdr_sample.jpg)

The aim of this project was to exoeriment features related to High Dynamic Range (HDR)


## Tutorial
[tutorial.py](./scripts/tutorial.py)
#### Debevec (Tonemap Durand)

![](./output/tutorial/ldr_debevec.jpg)       | ![](./output/tutorial/ldr_debevec_crf.jpg)
:-------------------------:|:-------------------------:
Without Crf| With Crf

#### Robertson (Tonemap Durand)
![](./output/tutorial/ldr_robertson.jpg)      | ![](./output/tutorial/ldr_robertson_crf.jpg)
:-------------------------:|:-------------------------:

#### Mertens 
![](./output/tutorial/fusion_mertens.jpg)



## Tone Mapping
[toneMapping.py](./scripts/toneMapping.py)
### cv2

Source :

| ![](./sources/data/266/DSC00267.jpg)  | ![](./sources/data/266/DSC00266.jpg) | ![](./sources/data/266/DSC00268.jpg) |
|:-------------------------:|:-------------------------:|:-------------------------:|
| Exposure time = 1/800  | Exposure time = 1/125 | Exposure time = 1/4 |

#### Drago
![](./output/tonemap/ldr_Drago_gamma_1.0_satu_1.0_lum_500.jpg)

#### Durand
![](./output/tonemap/ldr_Durand_gamma_1.0_satu_1.0_lum_700.jpg)

#### Mantiuk
![](./output/tonemap/ldr_Mantiuk_gamma_1.0_satu_1.0_lum_900.jpg)

#### Reinhard
![](./output/tonemap/ldr_Reinhard_gamma_1.0_light_0.75_lum_500.jpg)

### HDRI Operators
#### Gamma Operator
![](./output/tonemap/ldr_hdri_gamma_1.0_lum_1500.jpg)

#### Logarithmic Operator
![](./output/tonemap/ldr_hdri_logarithmic_lum_6000.jpg)

#### Exponential Operator
![](./output/tonemap/ldr_hdri_exponential_lum_255.jpg)