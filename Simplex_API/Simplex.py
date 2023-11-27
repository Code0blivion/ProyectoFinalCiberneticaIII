import numpy as np
import sympy as sp

class MetodoSimplex:
  #------------------------Método simplex base---------------------------
  def dividirfila(self,a,b):
    return sp.Matrix([a[i]/b[i] for i in range(len(a))])
  def mulfila(self, a,b):
    return sp.Matrix([a[i]*b[i] for i in range(len(a))])
  
  def solve(self,M,sim,H, resultado=None):

    #Lista donde se almacenan las matrices temporales y el resultado
    if resultado==None:
      resultado = [[list(i) for i in np.block([np.array([H+['~']],dtype='str').T,np.array(M,dtype='str')])]]

    M=sp.Matrix(M)
    #Selecciona el pivote
    ve=np.argmax((M.subs(sp.symbols('M'),1e4))[-1,:-1])
    vs=np.argmin([(i if i>0 else np.inf) for i in np.array(M[:-1,-1],dtype='float64')/np.array(M[:-1,ve],dtype='float64')])
    #Hace el remplazo de la variable
    H[vs]=sim[ve]
    M[vs,:]=M[vs,:]/M[vs,ve]
    #Hace ceros en la columna del pivote
    for i in range(M.shape[0]):
      #Realiza el procedimiento solo si la fila no es la del pivote
      if i!=vs:
        M[i,:]=M[i,:]*M[vs,ve]-M[vs,:]*M[i,ve]

    #Guarda la matriz temporal en la lista de resultados
    resultado.append([list(i) for i in np.block([np.array([H+['~']],dtype='str').T,np.array(M,dtype='str')])])
  
    #Verifica si hay numeros positivos en la ultima fila exceptuando el resultado en p
    if len(np.array((M.subs(sp.symbols('M'),1e4))[-1,:-1],dtype="float64")[np.array((M.subs(sp.symbols('M'),1e4))[-1,:-1],dtype="float64")>0])>0:
      #Si hay positivos mayores a cero llama a la funcion pero con la nueva matriz
      return self.solve(M,sim,H,resultado)
    #a grega a H un valor resultado para devolver un diccionario con los valores
    H.append("Resultado")
    M[-1,-1]=abs(M[-1,-1])
    #Guardar los resultados finales en la lista de resultados
    #resultado.append({H[i]: M[i,-1] for i in range(len(H))}) 
    #print(resultado[-1])
    return resultado, [[H[i],str(M[i,-1])] for i in range(len(H))]
  

  #Devuelve la información que necesita el metodo simplex base
  def inicializarProblema(self, func_obj, restricciones, igualdades, tipos_restriccion):

    sim = []
    H = []
    M = 1e2
    K = []
    

    #En el siguiente codigo se intenta obtener sim

    #Añadir variables no basicas
    for i in range(len(restricciones[0])):
        sim.append('x'+str((i+1)))
    
    #Añadir variables artificiales y de holgura
    bas = []
    a_ind = 0
    h_ind = 0

    for item in tipos_restriccion:
        if item == '=':
            a_ind = a_ind + 1
            bas.append('a'+str(a_ind))         
        elif item == '<=':
            h_ind = h_ind + 1
            bas.append('h'+str(h_ind))       
        elif item == '>=':
            a_ind = a_ind + 1
            h_ind = h_ind + 1
            bas.append('a'+str(a_ind))           
            bas.append('h'+str(h_ind))
            

    bas.sort()

    sim.extend(bas)

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
    #print("K:",K)

    #Sacar la ultima fila de K
    z = [str(item) for item in func_obj] 

    for i in range(a_ind):
      z.append("M")
    
    for i in range(h_ind):
       z.append(str(0))

    #print(z)

    simbolos = sp.symbols((*sim,'M'))

    dict_sim = {str(simbolo) : simbolo for simbolo in simbolos}

    #print(simbolos)

    #Obtener fila de la función objetivo con las variables artificiales multiplicadas por M agregadas e igualada a 0
    z = [-1*eval(item, dict_sim) for item in z]
    z.append(0)
    #print(z)

    #Verificar que haya variables artificiales
    if a_ind > 0:
      #Eliminar las variables artificiales
      cont_a = a_ind
      for restriccion in K:
        if restriccion[len(func_obj)+a_ind-cont_a] != 0 and cont_a > 0:
          z = [z[i] + (-z[len(func_obj)+a_ind-cont_a]/restriccion[len(func_obj)+a_ind-cont_a])*restriccion[i] for i in range(len(z))]
          cont_a = cont_a - 1

    #print(z)

    #Se completa la matriz K
    K.append(z)

    print("K:",K)

    #Hallar H
    h_compl = set()
    for num, item in enumerate(sim):
      if z[num] != 0:
         h_compl.add(item)

    H = list(set(sim)-h_compl)
    
    H.sort()
    print("H:",H)
    return K, sim, H

    """
    sim = ['x1','x2','a1','a2','h1','h2']
    H=['a1','a2','h2']
    M=1e2
    K=[[3,1,1,0,0,0,3],
    [4,3,0,1,-1,0,6],
    [1,2,0,0,0,1,4],
    [7*M-4,4*M-1,0,0,-M,0,9*M]]
    #solver.solve(K,sim,H)
    """
    


