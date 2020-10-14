from reticulado import Reticulado
from barra import Barra
from graficar3d import ver_reticulado_3d
from math import *

# Unidades base
m = 1.
kg = 1.
s = 1. 

#Unidades derivadas
N = kg*m/s**2
cm = 0.01*m
mm = 0.001*m
KN = 1000*N

Pa = N / m**2
KPa = 1000*Pa
MPa = 1000*KPa
GPa = 1000*MPa

#Parametros

L = 5.0  *m
H = 3.5  *m
B = 2.0 *m


#Inicializar modelo
ret = Reticulado()      


#Nodos
ret.agregar_nodo(0     , 0   ,  0         )  
ret.agregar_nodo(L     , 0   ,  0         )
ret.agregar_nodo(2*L   , 0   ,  0         )
ret.agregar_nodo(3*L   , 0   ,  0         )
ret.agregar_nodo(L/2   , B/2 , H          )
ret.agregar_nodo(3*L/2 , B/2 , H          )
ret.agregar_nodo(5*L/2 , B/2 , H          )
ret.agregar_nodo(0     , B   , 0          )
ret.agregar_nodo(L     , B   , 0          )
ret.agregar_nodo(2*L   , B   , 0          )
ret.agregar_nodo(3*L   , B   , 0          )



#Barras

props = [8*cm, 5*mm, 200*GPa, 7600*kg/m**3, 420*MPa]


ret.agregar_barra(Barra(0, 1, *props))   # Hor 1
ret.agregar_barra(Barra(1, 2, *props))   
ret.agregar_barra(Barra(2, 3, *props))

ret.agregar_barra(Barra(0, 8, *props))   #Diag 1
ret.agregar_barra(Barra(1, 9, *props))
ret.agregar_barra(Barra(2, 10, *props))

ret.agregar_barra(Barra(0, 4, *props))   #diag vertical 1.1
ret.agregar_barra(Barra(1,5,  *props))
ret.agregar_barra(Barra(2,6 , *props))

ret.agregar_barra(Barra(1, 4, *props))   #diag vertical 1.2
ret.agregar_barra(Barra(2,5,  *props))
ret.agregar_barra(Barra(3,6,  *props))

ret.agregar_barra(Barra(0, 7, *props))   #Lateral
ret.agregar_barra(Barra(1,8 , *props))
ret.agregar_barra(Barra(2,9,  *props))
ret.agregar_barra(Barra(3,10,  *props))

ret.agregar_barra(Barra(1,7,  *props))   #Hor 2
ret.agregar_barra(Barra(2,8,  *props))
ret.agregar_barra(Barra(3,9,  *props))

ret.agregar_barra(Barra(7,8,  *props))   #Diag 2
ret.agregar_barra(Barra(8,9,  *props))
ret.agregar_barra(Barra(9,10,  *props))

ret.agregar_barra(Barra(4,7,  *props))   #diag vertical 2.1
ret.agregar_barra(Barra(5,8,  *props))
ret.agregar_barra(Barra(6,9,  *props))

ret.agregar_barra(Barra(4,8,  *props))   #diag vertical 2.2
ret.agregar_barra(Barra(5,9,  *props))
ret.agregar_barra(Barra(6,10,  *props))

ret.agregar_barra(Barra(4,5,  *props))   #Hor arriba
ret.agregar_barra(Barra(5,6,  *props))




ret.agregar_restriccion(0, 0, 0)  #Nodo 0 FIjo
ret.agregar_restriccion(0, 1, 0)
ret.agregar_restriccion(0, 2, 0)

ret.agregar_restriccion(7, 0, 0)  #Nodo 7 FIjo
ret.agregar_restriccion(7, 1, 0)
ret.agregar_restriccion(7, 2, 0)

ret.agregar_restriccion(3, 1, 0)  #Nodo 3 deslizable en x
ret.agregar_restriccion(3, 2, 0)

ret.agregar_restriccion(10, 1, 0)  #Nodo 10 deslizable en x
ret.agregar_restriccion(10, 2, 0)


peso1 = ret.calcular_peso_total()

print(f"peso 1 = {peso1}")





ret.ensamblar_sistema()
ret.resolver_sistema()
f = ret.recuperar_fuerzas()
fu = ret.recuperar_factores_de_utilizacion(f)


ver_reticulado_3d(ret, 
    opciones_nodos = {
        "usar_posicion_deformada": True,
        "factor_amplificacion_deformada": 30.,
    },
    opciones_barras = {
        "color_barras_por_dato": True,
        "ver_numeros_de_barras": False,
        "ver_dato_en_barras": True,
        "dato": fu,
        "color_fondo": [1,1,1,0.4]
    })


barras = ret.obtener_barras()
barras_a_rediseñar = range(len(barras))
for i in barras_a_rediseñar:
    print("\n",f[i] )
    print( "factor utilizacion=",barras[i].obtener_factor_utilizacion(f[i]))
    barras[i].rediseñar(f[i])
    print( "factor utilizacion=",barras[i].obtener_factor_utilizacion(f[i]))





ret.ensamblar_sistema()
ret.resolver_sistema()
f1 = ret.recuperar_fuerzas()
fu1 = ret.recuperar_factores_de_utilizacion(f)

peso2 = ret.calcular_peso_total()

print(f"peso 2 = {peso2}")
print (f"Diferencia de peso = {abs((peso1- peso2)/1000)} Ton")

ver_reticulado_3d(ret, 
    opciones_nodos = {
        "usar_posicion_deformada": True,
        "factor_amplificacion_deformada": 30.,
    },
    opciones_barras = {
        "color_barras_por_dato": True,
        "ver_numeros_de_barras": False,
        "ver_dato_en_barras": True,
        "dato": fu1,
        "color_fondo": [1,1,1,0.4]
    })