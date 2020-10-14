# Repositorio Proyecto 2 grupo 10
 
Para el rediseño de las barras se decidió tomar en cuanto todas la barras para el rediseño, y luego mostrar 1 barra por cada grupo de barras, tomando un grupo como las barras con la misma dirección, es decir las que unen los siguientes nodos:
(0,1) (0,8), (0,4) , (0,7) y (4,5)

Finalizando el rediseño los radios finales de estas barras en [m] son:
* 0.0025035
* 0.00201362
* 0.0196233
* 0.01957615
* 0.00868926





la función de rediseño de la barra se basa en el es el sistema de optimización de scipy, utilizando las funciones 

Esta función busca minimizar la diferencia entre el valor de la fuerza ejercida en la barra y la fuerza máxima que esta puede ejercer en su rango elástico, multiplicado por un factor de minoración de 0.9
Cuando la fuerza entregada es de compresión además se toma en cuenta la restricción del pandeo, donde la barra debe presentar un área (e inercia) suficiente para no ser afectada por una falla de pandeo. 
Al encontrar el valor de radio que iguale el valor de fuerza entregada se actualiza el valor de este. Se decidió que el radio mínimo  de cada barra no puede ser inferior a 1 cm.


En relación a la nueva distribución de FU, para mejorar aún más el costo o peso de la estructura, sería necesaria la implementación de una función que optimiza automáticamente la sección transversal de las barras que tienen un FU menor, o bien quitar aquellas que no aporten significativamente al reticulado.

