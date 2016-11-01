# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 15:20:18 2016

@author: LSI
"""
from IPython import get_ipython

# Clear all
get_ipython().magic('reset -sf')


import dicom
import numpy as np
import os
import cv2
from matplotlib import pyplot

def box_filt(im, box):
    [l,c]=im.shape
    [lbox, cbox]=box.shape    
    mat_filt=np.zeros(shape=(l,c),dtype='uint8')
    #Valores centrais da box
    value_h=int(np.ceil(cbox/2))-1
    value_v=int(np.ceil(lbox/2))-1
    for i in range(value_h,(c-value_h)):
        for j in range(value_v, (l-value_v)):
            aux=0
            for k in range(-(value_h), value_h+1):
                for q in range(-(value_v), value_v+1):
                    aux+=box[value_v+q,value_h+k]*im[j+q,i+k]
            mat_filt[j,i]=aux
    return mat_filt



#PathDicom = "./DOI/Prostate3T-01-0001/1.3.6.1.4.1.14519.5.2.1.7308.2101.878027069026309930088081179232/1.3.6.1.4.1.14519.5.2.1.7308.2101.294123309272114469889813649698/"
PathDicom ="./DOI/Prostate3T-01-0002/1.3.6.1.4.1.14519.5.2.1.7308.2101.174768087184217631998622694695/1.3.6.1.4.1.14519.5.2.1.7308.2101.203002521314946007603842576868"

lstFilesDCM = []  # create an empty list
for dirName, subdirList, fileList in os.walk(PathDicom):
    for filename in fileList:
        if ".dcm" in filename.lower():  # check whether the file's DICOM
            lstFilesDCM.append(os.path.join(dirName,filename))


# Get ref file
RefDs = dicom.read_file(lstFilesDCM[0])

# Load dimensions based on the number of rows, columns, and slices (along the Z axis)
ConstPixelDims = (int(RefDs.Rows), int(RefDs.Columns), len(lstFilesDCM))

# Load spacing values (in mm)
ConstPixelSpacing = (float(RefDs.PixelSpacing[0]), float(RefDs.PixelSpacing[1]), float(RefDs.SliceThickness))

x = np.arange(0.0, (ConstPixelDims[0]+1)*ConstPixelSpacing[0], ConstPixelSpacing[0])
y = np.arange(0.0, (ConstPixelDims[1]+1)*ConstPixelSpacing[1], ConstPixelSpacing[1])
z = np.arange(0.0, (ConstPixelDims[2]+1)*ConstPixelSpacing[2], ConstPixelSpacing[2])

# The array is sized based on 'ConstPixelDims'
ArrayDicom = np.zeros(ConstPixelDims, dtype=RefDs.pixel_array.dtype)

# loop through all the DICOM files
for filenameDCM in lstFilesDCM:
    # read the file
    ds = dicom.read_file(filenameDCM)
    # store the raw image data
    ArrayDicom[:, :, lstFilesDCM.index(filenameDCM)] = ds.pixel_array  
    
    
#Dois tipos de plots
im=ArrayDicom[:,:,0]

#Utilizando pcolormesh    
fig=pyplot.figure(1)
fig.suptitle('Plot através de pcolormesh', fontsize=12, fontweight='bold')
pyplot.gca().set_xlim((0,ConstPixelDims[0]))
pyplot.gca().set_ylim((0,ConstPixelDims[1]))
pyplot.axes().set_aspect('equal')
pyplot.set_cmap(pyplot.gray())
pyplot.pcolormesh(np.flipud(im))



#Utilizando imshow
fig=pyplot.figure(2)
fig.suptitle('Plot através de imshow', fontsize=12, fontweight='bold')
pyplot.imshow(im)

#im=np.uint8(ArrayDicom[:,:,6])
#im=cv2.convertScaleAbs(ArrayDicom[:,:,6])

#cv2.imwrite('MRI.png',ArrayDicom[:,:,6])

kernel_size=[3,5,7,9]

#for size in kernel_size:
#    gauss=cv2.GaussianBlur(im, (5,5), size)
#    fig=pyplot.figure
#    #fig.suptitle('Filtro Gaussiano - tamanho do kernel='+str(size), fontsize=12, fontweight='bold')
#    pyplot.imshow(gauss)
#    name='filtro_gauss_'
#    name+=str(size)
#    name+='.png'
#    pyplot.savefig(name)
#    
#    kernel = np.ones((size,size),np.uint16)
#    opening = cv2.morphologyEx(im, cv2.MORPH_OPEN, kernel)
#    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
# 
#    fig=pyplot.figure
#    #fig.suptitle('Abertura->Fechamento - tamanho do kernel='+str(size), fontsize=12, fontweight='bold')
#    pyplot.imshow(closing)
#    name='abertura_fechamento_'
#    name+=str(size)
#    name+='.png'
#    pyplot.savefig(name)

kernel = np.ones((7,7),np.uint16)
opening = cv2.morphologyEx(im, cv2.MORPH_OPEN, kernel)
closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)


# Gausian filter com fechamento e abertura um após o outro
    


fig=pyplot.figure(2)
pyplot.imshow(closing)

gauss=cv2.GaussianBlur(closing, (5,5), 7)
fig=pyplot.figure(3)
pyplot.imshow(gauss)
 
 
#box_lap=np.matrix('-1 -1 -1; -1 8 -1; -1 -1 -1')/9
#lap=box_filt(gauss, box_lap)
#fig=pyplot.figure(4)
#pyplot.imshow(lap)

 
 
#fig=pyplot.figure(4)
#fig.suptitle('Fechamento', fontsize=12, fontweight='bold')
#pyplot.imshow(closing)

# Abertura
#
#fig=pyplot.figure(5)
#fig.suptitle('Histograma', fontsize=12, fontweight='bold')
#pyplot.hist(gauss)

def binarizar(im, lim):
    [l,c]=im.shape
    mat_bin=np.zeros(shape=(l,c),dtype='uint8')
    for i in range(1,l):
        for j in range(1, c):
            if(im[i,j]<=lim):
                mat_bin[i,j]=0
            else:
                mat_bin[i,j]=255
    return mat_bin
                

valores_provaveis=gauss[50:160,160];


fig=pyplot.figure(5)
fig.suptitle('Histograma', fontsize=12, fontweight='bold')
pyplot.hist(valores_provaveis)


## Binarizar
imagem_binarizada=binarizar(gauss, 250)
fig=pyplot.figure(7)
pyplot.imshow(imagem_binarizada)



#
## Histograma
#fig=pyplot.figure(4)
#fig.suptitle('Histograma', fontsize=12, fontweight='bold')
#pyplot.hist(closing)