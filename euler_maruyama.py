'''
Tesis - Simulación de procesos coalescentes 
Enrique Moctezuma González

'''

# Librerías.
import sympy as sy
import numpy as np
import matplotlib.pyplot as plt


''' 
===============================================================================
                       Método de Euler-Maruyama  
===============================================================================

'''

''' ============================== ALGORITMO ============================== '''

def euler_maruyama(n, t_max, x0, f, g, graficacion = True):
    
    # Variables introducidas como elementos de Sympy.
    x = sy.Symbol('x')
    t = sy.Symbol('t')
    
    # Funciones introducidas como elementos de Sympy.
    
    # Coeficiente de deriva.
    f = sy.sympify(f)
    f_dt = lambda posicion, tiempo: f.evalf(subs = {x: posicion, t: tiempo})
    
    # Coeficiente de difusión.
    g = sy.sympify(g)
    g_Bt = lambda posicion, tiempo: g.evalf(subs = {x: posicion, t: tiempo})
    
    # Condición inicial.
    X = [x0]
    
    # Intervalo temporal de simulación.
    tiempos = np.linspace(0, t_max, n)
    
    # Esquema iterativo de Euler-Maruyama.
    for i in range(1, len(tiempos)):
        Y = np.random.normal(0, 1)
        X.append(X[-1]+f_dt(X[-1], tiempos[-1])*t_max/n+
                 g_Bt(X[-1], tiempos[-1])*np.sqrt(t_max/n)*Y)

    # Elementos de graficación.
    if graficacion:
        plt.plot(np.linspace(0, t_max, n), X, 
                 label = 'Trayectoria del proceso')
        plt.xlabel('Tiempo')
        plt.ylabel('Valor')
        plt.grid()
        plt.legend()
        plt.show()
    
    # La función regresa la lista con los valores del proceso.
    return X

''' ============================= PARÁMETROS ============================= '''

# Número de pasos.
n = 1000

# Máximo del intervalo de tiempo.
t_max = 5

# Condición inicial.
x0 = 3

# Coeficiente de deriva (ingresar como cadena de caracteres).
f = '-2*x'

# Coeficiente de difusión (ingresar como cadena de caracteres).
g = '0.5'

# Graficación.
graficacion = True

''' ============================== EJECUCIÓN ============================== '''

print(euler_maruyama(n, t_max, x0, f, g, graficacion))