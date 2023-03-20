# kVecionosMasCercanos-KNN-
Algoritmo de k vecionos más cercanos escrito en ptthon para clasificar imagenes de acuerdo a una serie de caracteristicas extraidas


Primero con numeros y la fuente citada se crean las imagenes de numeros (0-5) que se usaran

Luego con skeleton en matlab se tranforman las imagenes dejando unicamente los skeletons de cada numero para poder procesar su codigo cadena

Luego se usa el codigo de caracteristicas para crear un csv con las caracteristicas de cada numero

Se debe crear un csv a mano con las ultimas 100 lineas del csv caracteristicas y nombrarse caracteristicas_test.csv para poder realizar un test de datos que no fueron empleados para alimentar el modelo

Finalmente se emplea el codigo knn que realiza las predicciones para cada numero en caracteristicas_test y crea un csv con las predicciones
