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
        self.Ndimensiones = 2
        self.restricciones = {}

    def agregar_nodo(self, x, y,z=0):
        if self.Nodos +1 > Reticulado.__NodosInit__:
            self.xyz.resize((self.Nodos+1,3))
        self.xyz[self.Nodos,:]= [x,y,z]
        self.Nodos+=1
        if z != 0 :
            self.Ndimensiones = 3

    
    def agregar_barra(self,barra):
        self.barras.append(barra)

    def obtener_coordenada_nodal(self, nodo): 
        if nodo >= self.Nodos:
            return
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
        """Agrega una restriccion, dado el nodo, grado de libertad y valor 
        del desplazamiento de dicho grado de libertad
        """
        
        if nodo not in self.restricciones:
            self.restricciones[nodo]= [[gdl,valor]]
        else:
            self.restricciones[nodo].append([gdl,valor])



    def agregar_fuerza(self, nodo, gdl, valor):
        """Agrega una fuerza, dado el nodo, grado de libertad y valor 
        del la fuerza en la direccion de dicho GDL
        """
        if nodo not in self.cargas:
            self.cargas[nodo]= [[gdl,valor]]
        else:
            self.cargas[nodo].append([gdl,valor])


    def ensamblar_sistema(self):
        """Ensambla el sistema de ecuaciones"""
        
        Ngdl = self.Nodos * self.Ndimensiones

        self.K = np.zeros((Ngdl,Ngdl), dtype=np.double)
        self.f = np.zeros((Ngdl), dtype=np.double)
        self.u = np.zeros((Ngdl), dtype=np.double)
        
        for i in self.barras:
            elemento=obtener_rigidez(i)      # metodo arcaico y poco optimizado pero sencillo para digerir
            
            self.K[2*i.ni,2*i.ni]       +=elemento[0,0]     #zona barras nodo 1 a nodo 1
            self.K[2*i.ni,2*i.ni+1]     +=elemento[0,1]
            self.K[2*i.ni+1,2*i.ni]     +=elemento[1,0]
            self.K[2*i.ni+1,2*i.ni+1]   +=elemento[1,1]
            
            
            self.K[2*i.nj,2*i.nj]       +=elemento[2,2]    #zona barras nodo 2 a nodo 2
            self.K[2*i.nj,2*i.nj+1]     +=elemento[2,3]
            self.K[2*i.nj+1,2*i.nj]     +=elemento[3,2]
            self.K[2*i.nj+1,2*i.nj+1]   +=elemento[3,3]
            
            
            
            self.K[2*i.ni,2*i.nj]     +=elemento[0,2]       #zona barras nodo 1 a nodo 2
            self.K[2*i.ni,2*i.nj+1]   +=elemento[0,3]
            self.K[2*i.ni+1,2*i.nj]   +=elemento[1,2]
            self.K[2*i.ni+1,2*i.nj+1] +=elemento[1,3]
            

            self.K[2*i.nj,2*i.ni]     +=elemento[2,0]      #zona barras nodo 2 a nodo 1
            self.K[2*i.nj,2*i.ni+1]   +=elemento[2,1]
            self.K[2*i.nj+1,2*i.ni]   +=elemento[3,0]
            self.K[2*i.nj+1,2*i.ni+1] +=elemento[3,1]
            



    def resolver_sistema(self):
        """Resuelve el sistema de ecuaciones.
        La solucion queda guardada en self.u
        """

        # 0 : Aplicar restricciones
        Ngdl = self.Nodos * self.Ndimensiones
        gdl_libres = np.arange(Ngdl)
        gdl_restringidos = []

        #Identificar gdl_restringidos y llenar u 
        # en valores conocidos.
        #
        # Hint: la funcion numpy.setdiff1d es util


        #Agregar cargas nodales a vector de cargas 
        for nodo in self.cargas:
            for carga in self.cargas[nodo]:
                gdl = carga[0]
                valor = carga[1]
                gdl_global = 2*nodo + gdl
                


        #1 Particionar:
        #       K en Kff, Kfc, Kcf y Kcc.
        #       f en ff y fc
        #       u en uf y uc
        

        # Resolver para obtener uf -->  Kff uf = ff - Kfc*uc
        
        #Asignar uf al vector solucion
        self.u[gdl_libres] = uf

        #Marcar internamente que se tiene solucion
        self.tiene_solucion = True

    def obtener_desplazamiento_nodal(self, n):
        """Entrega desplazamientos en el nodo n como un vector numpy de (2x1) o (3x1)
        """
        dofs = [2*n, 2*n+1]
        return self.u[dofs]



    def recuperar_fuerzas(self):
        """Una vez resuelto el sistema de ecuaciones, se forma un
        vector con todas las fuerzas de las barras. Devuelve un 
        arreglo numpy de (Nbarras x 1)
        """
        
        fuerzas = np.zeros((len(self.barras)), dtype=np.double)
        for i,b in enumerate(self.barras):
            fuerzas[i] = b.obtener_fuerza(self)

        return fuerzas





    def __str__( self ):
        q= "Informacion reticulado \n \n"
        q+= "El peso total del enrrejado es de: "+ str(self.calcular_peso_total())+" Kg"
        q+= 2*"\n"
        q+="Los nodos y sus ubicaciones son: \n"
        for i in range(self.Nodos):
            q += f"   {i} : ({self.xyz[i,0]} , {self.xyz[i,1]} , {self.xyz[i,2]}) \n"
        q+= "\n "
        
        q+= "Las barras conectan los nodos de la siguiente forma: \n"
        for i,b in enumerate(self.barras):
            n= b.obtener_conectividad()
            q+= f"   {i}: [ {n[0]} <---> {n[1]} ] "
            q+= "\n"
        q+= 2*"\n"
        
        q+= " Las restricciones del sistema son: \n"
        for i in self.restricciones:
            q+= f"{i} : {self.restricciones[i]} \n"
        q+="\n"
        
        q+= " Las cargas sobre el sistema son: \n"
        for i in self.cargas:
            q+= f"{i} : {self.cargas[i]} \n"
        q+="\n"
        
        return q