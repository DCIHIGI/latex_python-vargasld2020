#PAQUETES
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math 
import glob
import re
import os
from sklearn.linear_model import LinearRegression 

#ABRIENDO Y LEYENDO ARCHIVOS
print('\n\t\tARCHIVOS A ANALIZAR')
files = glob.glob('./ListasNominales/*.txt')
print('\n',files,'\n\n')

#ACOMODANDO ARCHIVOS
date = []
date_ = []
files_ = []

for i,file in enumerate(files):
    date.append(re.findall(r'\d+',file)[0])

print('\t\tARCHIVOS ACOMODADOS POR FECHA\n')    
temp = sorted(range(len(date)),key=date.__getitem__)

for i in temp:
    date_.append(date[i])
    print(date[i],files[i],'\n')
    files_.append(files[i])

#FILTRANDO ARCHIVOS POR MUNICIPIO
for i,file in enumerate(files_):
    data = pd.read_csv(file)
    data = data[1:]
    data = data[data['ENTIDAD']==11][1:]
    mpo = data.groupby(['MUNICIPIO']).sum()
    if i == 0:
        if 'LISTA_NAL' in mpo.columns:
            dfmpo = pd.DataFrame(mpo['LISTA_NAL'])
        if 'LISTA_NACIONAL' in mpo.columns:
            dfmpo = pd.DataFrame(mpo['LISTA_NACIONAL'])
        if 'LISTA' in mpo.columns:
            dfmpo = pd.DataFrame(mpo['LISTA'])
    else:
        if 'LISTA_NAL' in mpo.columns:
            dfmpo[date_[i]] = mpo['LISTA_NAL']
        if 'LISTA_NACIONAL' in mpo.columns:
            dfmpo[date_[i]] = mpo['LISTA_NACIONAL']
        if 'LISTA' in mpo.columns:
            dfmpo[date_[i]] = mpo['LISTA']
            
#FILTRANDO ARCHIVOS POR SECCIÓN
for i,file in enumerate(files_):
    data = pd.read_csv(file)
    data = data[1:]
    data = data[data['ENTIDAD']==11][1:]
    mpo = data.groupby(['SECCION']).sum()
    if i == 0:
        if 'LISTA_NAL' in mpo.columns:
            dfsec = pd.DataFrame(mpo['LISTA_NAL'])
        if 'LISTA_NACIONAL' in mpo.columns:
            dfsec = pd.DataFrame(mpo['LISTA_NACIONAL'])
        if 'LISTA' in mpo.columns:
            dfsec = pd.DataFrame(mpo['LISTA'])
    else:
        if 'LISTA_NAL' in mpo.columns:
            dfsec[date_[i]] = mpo['LISTA_NAL']
        if 'LISTA_NACIONAL' in mpo.columns:
            dfsec[date_[i]] = mpo['LISTA_NACIONAL']
        if 'LISTA' in mpo.columns:
            dfsec[date_[i]] = mpo['LISTA']            

#IMPRIMIENDO DATOS FILTRADOS
print('\n\n\t\tTABLA POR MUNICIPIO\n\n',dfmpo.head(10))
print('\n\t\tTABLA POR SECCION\n\n',dfsec.head(10))

#REGRESIÓN LINEAL Y PREDICCIÓN
mpopl = np.asarray(dfmpo)
predl = []
for i in range(len(mpopl)):
    x = np.arange(len(mpopl[i]))
    m,b = np.polyfit(x, mpopl[i], 1, w=mpopl[i])
    pred = m*(x[-2]+2) + b
    predl.append(pred)

dfmpo['PRED_LIN'] = predl
print('\n\n\t\tINCLUYENDO LA PREDICCIÓN LINEAL\n\n',dfmpo.head(10))

dicm = np.array(dfmpo['202012'])
predic = np.array(predl)
div = np.divide(predic,dicm)
prom = np.mean(div)
dics = np.array(dfsec['202012'])
rnd = np.ceil(dics)
dfsec['202102'] = rnd
casillas = rnd/750
casillastot = np.ceil(casillas)
resultado = int(np.nansum(casillastot))

print('\n\n\t\tRESULTADO DEL ANÁLISIS\n')
plt.figure(figsize=(14,7))
plt.plot(dfmpo.iloc[0])
plt.title('LISTA POR MUNICIPIO')
plt.xlabel('Fecha')
plt.ylabel('Lista')
plt.yscale('log')
plt.show()

plt.figure(figsize=(14,7))
plt.plot(dfsec.iloc[0])
plt.title('LISTA POR SECCIÓN')
plt.xlabel('Fecha')
plt.ylabel('Lista')
plt.yscale('log')
plt.show()

print('\n\nEl número de casillas a instalar en febrero 2021 es: ',resultado)            
    
 

    
    