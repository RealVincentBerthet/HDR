# HDR

*BERTHET Vincent*

*QUERO Benoit*

## Tutorial
[tutorial.py](scripts/tutorial.py)
#### Debevec (Tonemap Durand)
Luminance physique
![](output/tutorial/ldr_debevec.jpg)
#### Robertson (Tonemap Durand)
Luminance physique
![](output/tutorial/ldr_robertson.jpg)
#### Mertens 
Brigthness
![](output/tutorial/fusion_mertens.jpg)



## Tone Mapping
[toneMapping.py](scripts/toneMapping.py)
HDR image used is the mertens generated in previous tutorial
### cv2
#### Drago
![](output/tonemap/tonemapDrago_gamma_1.0.jpg)

#### Durand
![](output/tonemap/tonemapDurand_gamma_1.0.jpg)

#### Mantiuk
![](output/tonemap/tonemapMantiuk_gamma_1.0.jpg)

#### Reinhard
![](output/tonemap/tonemapReinhard_gamma_1.0.jpg)

### HDRI @TODO
## Tone Mapping inverse