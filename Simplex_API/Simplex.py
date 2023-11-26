import numpy as np
import sympy as sp

class MetodoSimplex:
  #------------------------Método simplex base---------------------------
  def dividirfila(self,a,b):
    return sp.Matrix([a[i]/b[i] for i in range(len(a))])
  def mulfila(self, a,b):
    return sp.Matrix([a[i]*b[i] for i in range(len(a))])
  
  def solve(self,M,sim,H):

    #Lista donde se almacenan las matrices temporales y el resultado
    resultado = [] 

    M=sp.Matrix(M)
    #Selecciona el pivote
    ve=np.argmax((M.subs(sp.symbols('M'),1e4))[-1,:-1])
    vs=np.argmin([(i if i>0 else np.inf) for i in self.dividirfila(M[:-1,-1],M[:-1,ve])])
    #Hace el remplazo de la variable
    H[vs]=sim[ve]
    M[vs,:]=M[vs,:]/M[vs,ve]
    #Hace ceros en la columna del pivote
    for i in range(M.shape[0]):
      #Realiza el procedimiento solo si la fila no es la del pivote
      if i!=vs:
        M[i,:]=M[i,:]*M[vs,ve]-M[vs,:]*M[i,ve]

    #Guarda la matriz temporal en la lista de resultados
    resultado.append(M)
  
    #Verifica si hay numeros positivos en la ultima fila exceptuando el resultado en p
    if len(np.array((M.subs(sp.symbols('M'),1e4))[-1,:-1],dtype="float64")[np.array((M.subs(sp.symbols('M'),1e4))[-1,:-1],dtype="float64")>0])>0:
      #Si hay positivos mayores a cero llama a la funcion pero con la nueva matriz
      return self.solve(M,sim,H)
    #a grega a H un valor resultado para devolver un diccionario con los valores
    H.append("Resultado")
    M[-1,-1]=abs(M[-1,-1])
    #Guardar los resultados finales en la lista de resultados
    resultado.append({H[i]: M[i,-1] for i in range(len(H))}) 
    print(resultado[-1])
    return resultado
  

  #Devuelve la información que necesita el metodo simplex base
  def inicializarProblema(self, func_obj, restricciones, igualdades, tipos_restriccion):

    sim = []
    H = []
    M = 1e2
    K = []
    

    #En el siguiente codigo se intenta obtener sim

    #Añadir variables basicas
    for i in range(len(restricciones[0])):
        sim.append('x'+str((i+1)))
    
    #Añadir variables artificiales y de holgura
    a_ind = 1
    h_ind = 1

    for item in tipos_restriccion:
        if item == '=':
            sim.append('a'+str(a_ind))
            a_ind = a_ind + 1
        elif item == '<=':
            sim.append('h'+str(h_ind))
            h_ind = h_ind + 1
        elif item == '>=':
            sim.append('a'+str(a_ind))
            a_ind = a_ind + 1
            sim.append('h'+str(h_ind))
            h_ind = h_ind + 1

    #En el siguiente codigo se intenta obtener K 
    curr_ind = len(restricciones[1])
    for i,restriccion in enumerate(restricciones):
       rest = restriccion
       for j in range(len(sim)-len(rest)):
          if tipos_restriccion[i] == '=':
            rest.append(1)
            #FPendiente



    """
    sim = [x1,x2,a1,a2,h1,h2]
    H=['a1','a2','h2']
    M=1e2
    K=[[3,1,1,0,0,0,3],
    [4,3,0,1,-1,0,6],
    [1,2,0,0,0,1,4],
    [7*M-4,4*M-1,0,0,-M,0,9*M]]
    #solver.solve(K,sim,H)
    """
    


