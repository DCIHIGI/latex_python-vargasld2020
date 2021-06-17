#PAQUETES
import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd
from sklearn.linear_model import LinearRegression

#ABRIR ARCHIVO
df = pd.read_excel('migrantesynomig.xlsx')

#AGREGANDO COLUMNAS
def PoblacionTotal (fila):
    pobtot = fila['MIG_TOT'] + fila['NO_MIG_TOT']
    return pobtot

df['POB_TOT'] = df.apply(PoblacionTotal, axis=1)

def Porcentaje (fila):
    pctg = round((fila['MIG_TOT']*100)/fila['POB_TOT'])
    return pctg

df['POR_MIG'] = df.apply(Porcentaje, axis=1)

#FILTRANDO
dfc = df[['ENTIDAD','MIG_TOT','NO_MIG_TOT','AÑO','POB_TOT','POR_MIG']]
dff = dfc.groupby(['ENTIDAD','AÑO'])[['MIG_TOT','NO_MIG_TOT','POB_TOT','POR_MIG']].mean()
dfp = dff.groupby(['AÑO'])[['MIG_TOT','NO_MIG_TOT','POB_TOT']].sum()
dflr = dfc.groupby(['AÑO'])[['AÑO','MIG_TOT','NO_MIG_TOT','POB_TOT']].sum()
 
#IMPRIMIENDO ARCHIVO
print('\t\tTABLA GENERAL DE MIGRANTES Y NO MIGRANTES POR ENTIDAD Y AÑO\n\n',dff.head(15),'\n...\n\n')


print('\t-----------------------------------------------------------------------\t\n')

#GRAFICANDO
print('GRÁFICA DE MIGRANTES 1990-2010 EN MÉXICO')
dfp['MIG_TOT'].plot()
plt.ylabel('MIGRANTES (10mill por unidad)')
plt.title('MIGRANTES 1990-2010 MÉXICO')
plt.show()

print('\n\nGRÁFICA DE NO MIGRANTES 1990-2010 EN MÉXICO')
dfp['NO_MIG_TOT'].plot()
plt.ylabel('NO MIGRANTES (10mill por unidad)')
plt.title('NO MIGRANTES 1990-2010 MÉXICO')
plt.show()

print('\n\t-----------------------------------------------------------------------\t\n')

#ESTIMACIÓN LINEAL Y PREDICCIÓN

print('\t\tTABLA DE MIGRANTES Y NO MIGRANTES POR AÑO\n\n',dfp,'\n')

X = np.array(dflr['AÑO']).reshape(-1,1)
Y = np.array(dflr['MIG_TOT'])
regresion = LinearRegression()
regresion.fit(X,Y)
X_new = np.array([64640,64960]).reshape(-1,1)
Y_new = regresion.predict(X_new)

x = np.array(dflr['AÑO']).reshape(-1,1)
y = np.array(dflr['NO_MIG_TOT'])
regresion = LinearRegression()
regresion.fit(x,y)
x_new = np.array([64640,64960]).reshape(-1,1)
y_new = regresion.predict(x_new)

x1 = np.array(dflr['AÑO']).reshape(-1,1)
y1 = np.array(dflr['POB_TOT'])
regresion = LinearRegression()
regresion.fit(x1,y1)
x1_new = np.array([64640,64960]).reshape(-1,1)
y1_new = regresion.predict(x1_new)

print('\t-----------------------------------------------------------------------\t\n')

print('\t\tPREDICCION PARA INICIOS DE DÉCADAS\n')

pct20 = (Y_new[0]*100)/y1_new[0]
pct30 = (Y_new[1]*100)/y1_new[1]    

print('Migrantes totales a inicios de 2020: ',round(Y_new[0]))
print('Migrantes totales a inicios de 2030: ',round(Y_new[1]))

print('\n\nNo Migrantes totales a inicios de 2020: ',round(y_new[0]))
print('No Migrantes totales a inicios de 2030: ',round(y_new[1]))

print('\n\nLa población total a inicios de 2020 será: ',round(y1_new[0]))
print('La población total a inicios de 2030 será: ',round(y1_new[1]))

print('\n\nEl porcentaje de migrantes en Méixco en el año 2020 es de ',pct20,'%')
print('El porcentaje de migrantes en México en el año 2030 es de ',pct30,'%')

#FIN DEL CÓDIGO
print('\n\t\tFIN DEL CÓDIGO :)')









