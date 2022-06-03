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
                      Coalescente de difusiones de WF
===============================================================================

'''

''' ============================== ALGORITMO ============================== '''

# Método de Euler-Maruyama modificado para la difusión de WF.
def euler_maruyama_wf(n, t_max, x0, graficacion=True):
    
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
    intervalo = np.linspace(0, t_max, n)
    
    # Simulación de la trayectoria con el método de Euler-Maruyama.
    for i in range(1, len(intervalo)):
        Y = np.random.normal(0, 1)
        iteracion = X[-1]+f_dt(X[-1], intervalo[i-1])*t_max/n+g_Bt(X[-1], 
                    intervalo[i-1])*np.sqrt(t_max/n)*Y
        
        # Modificación del algoritmo.
       
        # Frontera 1.
        if iteracion > 1:
            X.extend([1]*(n-i))
            break

        # Frontera 0.
        elif iteracion < 0:
            X.extend([0]*(n-i))
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

# Simulación del coalescente.
def coalescente_wf(k, n, t_max):
     
    # Inicialización.
    registro = np.reshape([None]*(k*n), (k, n))
    particion = np.linspace(0, 1, k+2)
    particion = np.delete(particion, [0, -1])
    indices = np.arange(k)
    
    # Permutación aleatoria.
    np.random.shuffle(indices)
    
    for i in indices:
        
        # Simulación de la i-ésima trayectoria.
        trayectoria = euler_maruyama_wf(n, t_max, particion[i], False)
        
        # Inicialización de las trayectorias superior e inferior.
        trayectoria_sup = [1]*n
        trayectoria_inf = [0]*n
        
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
            
            # Con la trayectoria inferior.
            if trayectoria[l] < trayectoria_inf[l]:
                trayectoria[l+1:] = trayectoria_inf[l+1:]
                break
            
            # Con la trayectoria superior.
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
t_max = 1

''' ============================== EJECUCIÓN ============================== '''

print(coalescente_wf(k, n, t_max))