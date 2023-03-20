# Author: Overxfl0w13 #
# KNN para representaciones vectoriales #
# https://gist.github.com/jogonba2/04a7f8cbe1237fe47090

import pandas as pd
import numpy as np
def p_distance(v1,v2,p=2): 
	
	""" Calcula las distancias de la familia Lp, http://gyazo.com/b4183c93c58575351334366e3c07370b .
		Se asumen parámetros correctamente introducidos.
	
		Parámetros
		v1 -- vector 1
		v2 -- vector 2
		p  -- indicador de la distancia a emplear según la familia Lp
	"""
	s = 0
	if p!=0:
		for x in range(len(v2)): s += (v1[x]-v2[x])**p
		return s**(1.0/p)
	else:
		return max(map(abs,[v1[x]-v2[x] for x in range(len(v1))]))

def extract_class(stest,k_neighbours,samples_train,p):
	""" Extrae la clase correcta en función de la maxima cantidad de vecinos a mínima distancia de la muestra de test,
    a igualdad de vecinos mínimos, se calcula por mínima distancia.
    Se asumen parámetros correctamente introducidos.
    
    Parámetros 
    stest 		  -- muestra de test a clasificar
    k_neighbours  -- k vecinos a menor distancia de la muestra stest
    samples_train -- muestras de entrenamiento en caso de que se requiera desempate
    p             -- indicador de la distancia a emplear según la familia Lp
    """ 
	hash_neigh = {}
	for k_neigh in k_neighbours: 
		if k_neigh[0][1] not in hash_neigh: hash_neigh[k_neigh[0][1]] = 1
		else: hash_neigh[k_neigh[0][1]] += 1
	c_max = max(hash_neigh,key=hash_neigh.get)
	# Si hay alguna otra clase con el mismo número de vecinos, desempatar con el vecino de menor distancia entre las clases y la muestra #
	c_equals = [c_max]
	for key in hash_neigh: 
		if hash_neigh[key]==c_max: c_equals.append(key)
	min_distance = float('inf')
	for cls in c_equals:
		for v in samples_train:
			if v[1]==cls:
				dist = p_distance(stest,v[0])
				if dist<min_distance: min_distance,c_max = dist,cls
	return c_max
		
	
def knn(samples_test,samples_train,k,p):
	""" Clasifica las muestras de test en funcion de las muestras de entrenamiento. 
	Se asumen parámetros correctamente introducidos.
	
	Parámetros
	samples_test  -- muestras a clasificar
	samples_train -- prototipos iniciales (muestras de entrenamiento ya clasificadas)
	k             -- nº de vecinos a emplear en el clasificador
	p             -- indicador de la distancia a emplear según la familia Lp
	
	Excepciones
	...
	"""
	pred = pd.DataFrame()
	predicciones = []
	for stest in samples_test:
		k_neigh = []
		for strain in samples_train:
			# Si los k-vecinos aun no se han rellenado, llenarlos. #
			if len(k_neigh)<k: k_neigh.append([strain,p_distance(stest,strain[0],p)])
			# Si ya hay k-vecinos seleccionados, mirar si mejora la distancia en comparación al vecino con máxima distancia. #
			else: 
				dist = p_distance(stest,strain[0],p)
				m    = max(k_neigh,key=lambda x: x[1])
				if dist<m[1]: k_neigh[k_neigh.index(m)]=[strain,dist]
		#print("Muestra",stest,"clasificada en la clase",extract_class(stest,k_neigh,samples_train,p))
		predicciones.append(extract_class(stest,k_neigh,samples_train,p))
		#print(predicciones[-1])
		
	pred['predicciones']=predicciones
	return pred

if __name__ == "__main__":
    k=int(input('cuantos vecinos se tomaran en cuenta: '))
#    p=float(input('que metrica se usara (d. euclidiana =2): '))
    data = pd.read_csv("caracteristicas.csv")
    c = data.drop(['numero'],axis=1)
    numeros = data['numero']

    new_val = c.to_records(index=False)
    output = list(new_val)
    output2 = list(numeros)

    combinada = list(zip(output, output2))
    
    test = pd.read_csv("caracteristicas_test.csv")
    caracteristicas_test = test.drop(['numero'],axis=1)
    numeros_t = test['numero']
    
    new_val_t = caracteristicas_test.to_records(index=False)
    output_t = list(new_val_t)
    
    pred = knn(output_t,combinada,k,2)
    pred = pd.concat([pred, numeros_t], axis=1)
    condiciones = [pred['predicciones']== pred['numero'],pred['predicciones']!= pred['numero']]
    opciones = [1, 0]
    pred['aciertos'] = np. select(condiciones, opciones)
    pred.to_csv('predicciones.csv', header=True, index=False)
    print(pred)
    print(pred['aciertos'].sum())

