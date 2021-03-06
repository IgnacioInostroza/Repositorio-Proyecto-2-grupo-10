import numpy as np
import math

g = 9.81 #kg*m/s^2


class Barra(object):

    """Constructor para una barra"""
    def __init__(self, ni, nj, R, t, E, ρ, σy):
        super(Barra, self).__init__()
        self.ni = ni
        self.nj = nj
        self.R = R
        self.t = t
        self.E = E
        self.ρ = ρ
        self.σy = σy

    def obtener_conectividad(self):
        return [self.ni, self.nj]

    def calcular_area(self):
        A = np.pi*(self.R**2) - np.pi*((self.R-self.t)**2)
        return A

    def calcular_largo(self, reticulado):
        """Devuelve el largo de la barra. 
        ret: instancia de objeto tipo reticulado
        """
        xi = reticulado.obtener_coordenada_nodal(self.ni)
        xj = reticulado.obtener_coordenada_nodal(self.nj)
        dij = xi-xj
        return np.sqrt(np.dot(dij,dij))
    

    def calcular_peso(self, reticulado):
        """Devuelve el largo de la barra. 
        ret: instancia de objeto tipo reticulado
        """
        L = self.calcular_largo(reticulado)
        A = self.calcular_area()
        return self.ρ * A * L * g


    def obtener_rigidez(self, ret):
        """Devuelve la rigidez ke del elemento. Arreglo numpy de (4x4)
        ret: instancia de objeto tipo reticulado
        """
        L = self.calcular_largo(ret)
        A = self.calcular_area(ret)
        k = self.E * A / L
        
        xi = ret.obtener_coordenada_nodal(self.ni)
        xj = ret.obtener_coordenada_nodal(self.nj)
        
        x1 = xi[0]
        y1 = xi[1]
        x2 = xj[0]
        y2 = xj[1]
        
        x = x2 - x1
        y = y2 - y1
        
        thetha = math.atan2(y, x) * (180.0 / math.pi)   #Angulo en grados
        
        T0 = [-math.cos(thetha), -math.sin(thetha), math.cos(thetha), math.sin(thetha)]
        ke = T0.T @ T0 * k

        return ke

    def obtener_vector_de_cargas(self, ret):
        """Devuelve el vector de cargas nodales fe del elemento. Vector numpy de (4x1)
        ret: instancia de objeto tipo reticulado
        """
        P = self.calcular_peso(ret)
        fy = np.array([0, -1, 0, -1])
        fe = fy.T * P/2 
        
        return fe


    def obtener_fuerza(self, ret):
        """Devuelve la fuerza se que debe resistir la barra. Un escalar tipo double. 
        ret: instancia de objeto tipo reticulado
        """
        L = self.calcular_largo(ret)
        A = self.calcular_area(ret)
        D = ret.obtener_desplazamiento_nodal(ret)
        se = A * self.E / L*D

        return se
