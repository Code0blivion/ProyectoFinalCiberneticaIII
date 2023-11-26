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
    no_bas = []
    a_ind = 0
    h_ind = 0

    for item in tipos_restriccion:
        if item == '=':
            a_ind = a_ind + 1
            no_bas.append('a'+str(a_ind))         
        elif item == '<=':
            h_ind = h_ind + 1
            no_bas.append('h'+str(h_ind))       
        elif item == '>=':
            a_ind = a_ind + 1
            h_ind = h_ind + 1
            no_bas.append('a'+str(a_ind))           
            no_bas.append('h'+str(h_ind))
            

    no_bas.sort()

    sim.extend(no_bas)

    #En el siguiente codigo se intenta obtener K 
    curr_ind_a = len(restricciones[1])
    curr_ind_h = len(restricciones[1]) + a_ind
    for i,restriccion in enumerate(restricciones):
      rest = restriccion
      flag_a = False
      flag_h = False
      for j in range(len(sim)-len(rest)):
        if tipos_restriccion[i] == '=': 
          if len(rest) == curr_ind_a and not flag_a:
            rest.append(1)
            curr_ind_a = len(rest)
            flag_a = True
          else:
            rest.append(0)
        elif tipos_restriccion[i] == '<=':
            if len(rest) == curr_ind_h and not flag_h:
              rest.append(1)
              curr_ind_h = len(rest)
              flag_h = True
            else:
              rest.append(0)
        elif tipos_restriccion[i] == '>=':
          if len(rest) == curr_ind_a and not flag_a:
            rest.append(1)
            curr_ind_a = len(rest)
            flag_a = True
          elif len(rest) == curr_ind_h and not flag_h:
              rest.append(-1)
              curr_ind_h = len(rest)
              flag_h = True
          else:
            rest.append(0)
      
      rest.append(igualdades[i])
      K.append(rest)

    print("sim:",sim)
    print("K:",K)

    #Sacar la ultima fila de K
    z = func_obj

    for i in range(a_ind):
      z.append("Ma"+str(i+1))
    
    print(z)



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
    


