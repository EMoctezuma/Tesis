'''
Tesis - Simulación de procesos coalescentes 
Enrique Moctezuma González

'''

# Librerías.
import numpy as np
import matplotlib.pyplot as plt
import sympy as sy
import seaborn as sns

''' 
===============================================================================
           Intersección de trayectorias de la difusión de WF
===============================================================================

'''

''' ============================== ALGORITMO ============================== '''

# Realización de una intersección.
def interseccion_trayectorias_wf(n, t_max, x0, x1, graficacion = True):
    
    # Variables espacial y temporal.
    x = sy.Symbol('x')
    t = sy.Symbol('t')
    
    # Coeficiente de deriva.
    f = sy.sympify('0')
    f_dt = lambda posicion, tiempo: f.evalf(subs = {x: posicion, t: tiempo})
    
    # Coeficiente de difusión.
    g = sy.sympify('sqrt(x*(1-x))')
    g_Bt = lambda posicion, tiempo: g.evalf(subs = {x: posicion, t: tiempo})
    
    # Condiciones iniciales.
    X0 = [x0]
    X1 = [x1]
    
    # Intervalo de tiempo.
    intervalo = np.linspace(0, t_max, n+1)
    
    # Intersección, inicializada en None (en principio no hay intersección de 
    # las trayectorias).
    altura = None
    tiempo = None
    
    # Se simula la primer trayectoria con el método de Euler-Maruyama y la 
    # corrección para la difusión de WF.
    for i in range(1, len(intervalo)):
        Y = np.random.normal(0, 1)
        iteracion = X0[-1]+f_dt(X0[-1], intervalo[i-1])*t_max/n+g_Bt(X0[-1], 
                    intervalo[i-1])*np.sqrt(t_max/n)*Y
        
        # Frontera 1.
        if iteracion > 1:
            X0.extend([1]*(n+1-i))
            break

        # Frontera 2.
        elif iteracion < 0:
            X0.extend([0]*(n+1-i))
            break
        
        # Interior de [0,1].
        else:
            X0.append(iteracion)
        
    # Graficación.
    if graficacion:
        plt.plot(intervalo, X0, color = 'turquoise')
    
    # Segunda trayectoria.
    for i in range(1, len(intervalo)):
        Y = np.random.normal(0, 1)
        iteracion = X1[-1]+f_dt(X1[-1], intervalo[i-1])*t_max/n+g_Bt(X1[-1], 
                    intervalo[i-1])*np.sqrt(t_max/n)*Y
        
        # Frontera 1.
        if iteracion > 1:
            X1.extend([1]*(n+1-i))
            break
        
        # Frontera 0.
        elif iteracion < 0:
            X1.extend([0]*(n+1-i))
            break
        
        # Interior de [0,1].
        else:
            X1.append(iteracion)
    
    # Graficación.
    if graficacion:
        plt.plot(intervalo, X1, color = 'yellowgreen')
    
    # Verificación de la intersección.
    
    for k in range(len(X0)):
        
        # Caso en el que se cruzan.
        if X0[k] > X1[k]:
            altura = (X1[k]+X1[k-1])/2
            tiempo = (intervalo[k]+intervalo[k-1])/2
            break
        
        # Caso en el que toman el mismo valor (en las fronteras).
        elif X1[k] == X0[k]:
            altura = X1[k]
            tiempo = intervalo[k]
            break
        
    # Graficación del punto de intersección (en caso de haberlo).
    if graficacion:
        
        if altura != None:
            plt.scatter(tiempo, altura, color = 'red', zorder = 10,
                        label = 'Intersección (aprox.): ('+
                        str(np.round(float(tiempo), 4))+', '+
                        str(np.round(float(altura), 4))+')')
            plt.legend()            
        
        # Elementos de graficación.
        plt.xlabel('Tiempo')
        plt.ylabel('Posición')
        plt.grid()
        plt.show()
    
    # La función regresa las coordenadas de la intersección.
    return tiempo, altura

# Densidad de la intersección.
def densidad(no_simulaciones, n, t_max, x0, x1, variable = 'tiempo'):
    
    # Lista donde se guardará el punto de intersección.
    muestra = []
    
    for i in range(no_simulaciones):
        
        # Número de iteración en curso (comentar para no imprimir).
        print(i)  
        
        valor = interseccion_trayectorias_wf(n, t_max, x0, x1, False)

        # Coordenada de altura, si variable = 'altura'.
        if variable == 'altura':
            if valor[1] != 0 and valor[1] != 1 and valor[1] != None:
                muestra.append(valor[1])
            
        # Coordenada de tiempo, si variable = 'tiempo'.
        elif variable == 'tiempo':
            if valor[1] != 0 and valor[1] != 1 and valor[1] != None:
                muestra.append(valor[0])
      
    muestra = np.array(muestra, dtype = float)
            
    # Densidad con KDE (factor de Scott).
    sns.kdeplot(muestra, fill = True)
    
    # Elementos de graficación.
    if variable == 'tiempo':
        plt.xlabel('Tiempo')
        
    elif variable == 'altura':
        plt.xlabel('Altura')
        
    plt.ylabel('Densidad')
    plt.grid()
    plt.xlim(0, max(muestra))
    plt.show()
    
    # La función regresa la proporción de intersecciones en el interior de 
    # [0,1].
    return len(muestra)/no_simulaciones

''' ============================= PARÁMETROS ============================= '''

# Para ambas funciones:

# Número de pasos por trayectoria.
n = 1000

# Tiempo máximo de simulación.
t_max = 2

# Condiciones iniciales (x0 < x1).
x0 = 0.4
x1 = 0.6

# Para la función 'densidad':

# Número de simulaciones.
no_simulaciones = 1000

# Tiempo o altura (escribir 'tiempo' o 'altura'). El valor por defecto es 
# 'tiempo'.
variable = 'tiempo'

''' ============================== EJECUCIÓN ============================== '''

print(interseccion_trayectorias_wf(n, t_max, x0, x1))
print(densidad(no_simulaciones, n, t_max, x0, x1, variable))