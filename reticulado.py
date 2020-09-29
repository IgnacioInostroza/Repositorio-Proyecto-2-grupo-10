import numpy as np


class Reticulado(object):
    """Definicion de un reticulado"""
    __NodosInit__=100

    def __init__(self):
        super(Reticulado, self).__init__()

        self.xyz=np.zeros((Reticulado.__NodosInit__,3),dtype=np.double)
        self.Nodos = 0
        self.barras = []
        self.cargas = {}
        self.restricciones = {}

    def agregar_nodo(self, x, y,z=0):
        if self.Nodos +1 > Reticulado.__NodosInit__:
            self.xyz.resize((self.Nodos+1,3))
        self.xyz[self.Nodos,:]= [x,y,z]
        self.Nodos+=1

    
    def agregar_barra(self,barra):
        self.barras.append(barra)

    def obtener_coordenada_nodal(self, nodo): 
        if nodo >= self.Nodos:
            return self.xyz[nodo,:]
        else:
            return self.xyz[nodo,:]

    def calcular_peso_total(self):
        W=0.
        for i in self.barras:
            W+= i.calcular_peso(self)
        return W

    def obtener_nodos(self):
        return self.xyz[0:self.Nodos,:].copy()

    def obtener_barras(self):
        return self.barras

    def agregar_restriccion(self, nodo, gdl, valor=0.0):

        return None

    def agregar_fuerza(self, nodo, gdl, valor):

        return None

    def ensamblar_sistema(self):

        return None

    def resolver_sistema(self):

        return None

    def recuperar_fuerzas(self):

        return None
    
    def __str__( self ):
        q= "Informacion reticulado \n \n"
        q+="Los nodos y sus ubicaciones son: \n"
        for i in range(self.Nodos):
            q += f"   {i} : ({self.xyz[i,0]}, {self.xyz[i,1]}, {self.xyz[i,2]},) \n"
        q+= "\n "
        q+= "Las barras conectan los nodos de la siguiente forma: \n"
        for i,b in enumerate(self.barras):
            n= b.obtener_conectividad()
            q+= f"   {i}: [ {n[0]} <---> {n[1]} ] "
            q+= "\n"
        q+= "\n"
        q+= "El peso total del enrejado es de: "+ str(self.calcular_peso_total())+" Kg"
        return q
    
        