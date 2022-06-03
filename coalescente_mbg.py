'''
Tesis - Simulación de procesos coalescentes 
Enrique Moctezuma González

'''

# Librerías.
import numpy as np
import matplotlib.pyplot as plt
import sympy as sy
import sys

''' 
===============================================================================
                           Coalescente de MBGs 
===============================================================================

'''

''' ============================== ALGORITMO ============================== '''

# Método de Euler-Maruyama.
def euler_maruyama(n, t_max, x0, f, g, graficacion=True):
    
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

# Simulación del coalescente.
def coalescente_mbg(k, n, t_max, x_max, mu, sigma):
    
    # Coeficientes de deriva y difusión.
    f = str(mu)+'*x'
    g = str(sigma)+'*x'
    
    # Inicialización.
    registro = np.reshape([None]*(k*n), (k, n))
    particion = np.linspace(0, x_max, k+1)
    particion = np.delete(particion, 0)
    indices = np.arange(k)
    
    # Permutación aleatoria.
    np.random.shuffle(indices)
    
    for i in indices:
        
        # Simulación de la i-ésima trayectoria.
        trayectoria = euler_maruyama(n, t_max, particion[i], f, g, False)
        
        # Inicialización de las trayectorias superior e inferior.
        trayectoria_sup = [sys.maxsize]*n
        trayectoria_inf = [-1]*n
        
        # Asignación de las nuevas trayectorias superior e inferior.
        
        # Trayectoria superior.
        for j in range(k-i-2, -1, -1):
            if registro[j, 0] != None:
                trayectoria_sup = registro[j, :]
                break
        
        # Trayectoria inferior.
        for j in range(k-i, k):
            if registro[j, 0] != None:
                trayectoria_inf = registro[j, :]
                break
            
        registro[k-1-i, :] = trayectoria
        
        # Verificación de la coalescencia.
        for l in range(1, len(trayectoria)):
            
            # con la trayectoria inferior.
            if trayectoria[l] < trayectoria_inf[l]:
                trayectoria[l+1:] = trayectoria_inf[l+1:]
                break
            
            # con la trayectoria superior.
            elif trayectoria[l] > trayectoria_sup[l]:
                trayectoria[l+1:] = trayectoria_sup[l+1:]
                break
        
        # Actualización de la matriz registro.
        registro[k-1-i, :] = trayectoria
        
        # Graficación de la trayectoria.
        plt.plot(np.linspace(0, t_max, n), trayectoria)
        
    # Elementos de graficación.
    plt.grid()
    plt.xlabel('Tiempo')
    plt.ylabel('Posición')
    
    # La función únicamente regresa la figura.
    return plt.show()

''' ============================= PARÁMETROS ============================= '''

# Número de trayectorias.
k = 30

# Número de pasos por trayectoria.
n = 1000

# Tiempo máximo de simulación.
t_max = 2

# Máximo del intervalo espacial.
x_max = 5

# Constante del término de deriva.
mu = 1

# Constante del término de difusión.
sigma = 0.5

''' ============================== EJECUCIÓN ============================== '''

print(coalescente_mbg(k, n, t_max, x_max, mu, sigma))