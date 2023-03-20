# https://ojskrede.github.io/inf4300/notes/week_04/
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv
import chain_code as cc
import pandas as pd

data = pd.read_csv("mnist.csv", header = None) #lee el csv
data_not = data[data[0] < 6] #selecciona los numeros 0,1,2,3,4,5 descartando los demas
caracteristicas = pd.DataFrame() #crea un df
caracteristicas['numero'] = data_not[0][:500] #se llena la primer columna del df con los numeros
tortuosidades=[] #lista de tortuosidades
largo=[] # largo de los skeleton de cada numero
areas=[]
perimetros=[]
areaboxs=[]
#angulos=[]
extensiones=[]
compacidades=[]


background = 0

for i in range(500): #iteramos sobre las imagenes de skeletons para extraer las caracteristicas
    name='nuevo_numero'+str(i)+'.png'
    image=cv.imread(name, cv.IMREAD_GRAYSCALE)
    if len(np.unique(image)) == 2:
      bg, fg = np.unique(image)
      image[image == bg] = background
      image[image == fg] = 255
    chain_code, boundary_pixels, tortuosidad = cc.trace_boundary(image, background)
    image_with_boundary = np.copy(image)
    for x, y in boundary_pixels:
      image_with_boundary[x, y] = 150
    tortuosidades.append(tortuosidad)
    largo.append(len(chain_code))
    #print(name,tortuosidad)
    
for i in range(500): #iteramos sobre las imagenes para extraer las caracteristicas
    name='numero'+str(i)+'.png'
    img=cv.imread(name, cv.IMREAD_GRAYSCALE)
    ret,thresh = cv.threshold(img,127,255,0)
    contours,hierarchy = cv.findContours(thresh, 1, 2)
    cnt = contours[0]
    area = cv.contourArea(cnt)
    perimeter = float(cv.arcLength(cnt,True))
    rect = cv.minAreaRect(cnt)
    box = cv.boxPoints(rect)
    box = np.int0(box)
    areabox = cv.contourArea(box)
    x,y,w,h = cv.boundingRect(cnt)
    rect_area = w*h
    compacidad= rect_area/(area+0.01)
    extension = float(area)/rect_area
    #angle = cv.fitEllipse(cnt)
    areas.append(area)
    perimetros.append(perimeter)
    areaboxs.append(areabox)
    extensiones.append(extension)
    compacidades.append(compacidad)
   # angulos.append(angle)

caracteristicas['tortuosidad']=tortuosidades
caracteristicas['largo']=largo
caracteristicas['area']=areas
caracteristicas['perimetro']=perimetros
caracteristicas['areabox']=areaboxs
#caracteristicas['compacidad']=compacidades

caracteristicas.to_csv('caracteristicas.csv', header=True, index=False)

