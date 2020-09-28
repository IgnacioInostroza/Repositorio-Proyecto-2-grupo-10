import numpy as np

g = 9.81 #kg*m/s^2


class Barra(object):

	"""Constructor para una barra.
    Los datos en orden son: nodo_i, nodo_j, radio, espesor, Modulo E, densidad, fluencia"""
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

		return None

	def calcular_area(self):
		"""Calcula el area de una barra circular"""
		return np.pi*(self.R**2-(self.R-self.t)**2)

	def calcular_largo(self, reticulado):

		return np.sqrt((self.ni[0]-self.nj[0])**2+(self.ni[1]-self.nj[1])**2)

	def calcular_peso(self, barra):
            """Entrega el peso de una barra """
            self.ρ*calcular_largo(barra)*self.calcular_area()*g