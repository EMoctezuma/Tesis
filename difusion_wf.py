'''
Tesis - Simulación de procesos coalescentes 
Enrique Moctezuma González

'''

# Librerías.
import numpy as np
import matplotlib.pyplot as plt
import sympy as sy

''' 
===============================================================================
         Método de Euler-Maruyama adaptado a la difusión de WF
===============================================================================

'''

''' ============================== ALGORITMO ============================== '''

def euler_maruyama_wf(n, t_max, x0, graficacion = True):
    
    # Variables espacial y temporal.
    x = sy.Symbol('x')
    t = sy.Symbol('t')
    
    # Coeficiente de deriva (preestablecido).
    f = sy.sympify('0')
    f_dt = lambda posicion, tiempo: f.evalf(subs = {x: posicion, t: tiempo})
    
    # Coeficiente de difusion (preestablecido).
    g = sy.sympify('sqrt(x*(1-x))')
    g_Bt = lambda posicion, tiempo: g.evalf(subs = {x: posicion, t: tiempo})
    
    # Condición inicial.
    X = [x0]
    
    # Intervalo de tiempo.
    intervalo = np.linspace(0, t_max, n+1)
    
    # Se simula la trayectoria con el método de Euler-Maruyama.
    for i in range(1, len(intervalo)):
        Y = np.random.normal(0, 1)
        iteracion = X[-1]+f_dt(X[-1], intervalo[i-1])*t_max/n+g_Bt(X[-1], 
                    intervalo[i-1])*np.sqrt(t_max/n)*Y
        
        # Modificación del algoritmo.
       
        # Frontera 1.
        if iteracion > 1:
            X.extend([1]*(n+1-i))
            break

        # Frontera 0.
        elif iteracion < 0:
            X.extend([0]*(n+1-i))
            break
        
        # En otro caso, se agrega el valor generado a la lista.
        else:
            X.append(iteracion)
        
    # Graficación.
    if graficacion:
        plt.plot(intervalo, X)
        
    # Elementos de graficación.
    plt.xlabel('Tiempo')
    plt.ylabel('Posición')
    plt.grid()
     
    # La función regresa el vector de valores que tomó la trayectoria.
    return X

''' ============================= PARÁMETROS ============================= '''

# Número de pasos de la trayectoria.
n = 1000

# Tiempo máximo de simulación.
t_max = 3

# Condición inicial.
x0 = 0.5

# Graficación.
graficacion = True

''' ============================== EJECUCIÓN ============================== '''

print(euler_maruyama_wf(n, t_max, x0, graficacion))