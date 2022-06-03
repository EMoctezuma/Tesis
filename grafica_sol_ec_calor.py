'''
Tesis - Simulación de procesos coalescentes 
Enrique Moctezuma González

'''

# Librerías.
import numpy as np
import matplotlib.pyplot as plt

''' 
===============================================================================
                   Curvas solución del problema del calor
===============================================================================

'''

''' ============================= PARÁMETROS ============================= '''

# Cantidad de números aleatorios uniformes por generar para cada integral.
n = 10000

# Mínimo del intervalo espacial.
a = -10

# Máximo del intervalo espacial.
b = 10

# Número de elementos en la partición del intervalo.
particion = 1000

''' ============================== ALGORITMO ============================== '''

# Función solución de la ecuación del calor (función de distribución del 
# tiempo de intersección de dos movimientos brownianos).
def u(t, x, n):
    return 1-2/(np.sqrt(2*np.pi))*metodo_monte_carlo(0, x/np.sqrt(2*t), n)

# Método Monte Carlo.
def metodo_monte_carlo(a, b, n):
    areas = (b-a)*exp(np.random.uniform(a, b, n))
    
    # La función regresa una aproximación a la integral.
    return np.mean(areas)

# Integrando.
def exp(y):
    return np.exp(-y**2/2)

# Partición del espacio.
dominio = np.linspace(a, b, particion)

# Tiempos de graficación: [0, 1, 10, 20, ..., 200].
tiempos = np.append([0, 1], np.arange(10, 210, 10))

# Colores de las curvas.
colores = ['black', 'black', 'red', 'darkorange', 'purple', 'green', 'blue', 
           'brown', 'deeppink', 'olive', 'cadetblue', 'red', 'darkorange', 
           'purple', 'green', 'blue', 'brown', 'deeppink', 'olive', 
           'cadetblue', 'red', 'darkorange', 'purple', 'green']

# Elementos de graficación.
ax = plt.axes(projection ='3d')
ax.set_xlabel(r'$x$', size = 12)
ax.set_ylabel(r'$t$', size = 12)
ax.set_zlabel(r'$u~\left(t,x\right)$', size = 12)

# Graficación.
j = 0
for i in tiempos:
    j += 1
    
    # Condición inicial.
    if i == 0:
        
        x = [a, 0]
        y = [i]*2
        z = [2, 2]
        ax.plot3D(x, y, z, color = 'black', zorder = len(tiempos)+1, 
                  linewidth = 0.8)
        x = [0, b]
        y = [i]*2
        z = [0, 0]
        ax.plot3D(x, y, z, color = 'black', zorder = len(tiempos)+1, 
                  linewidth = 0.8)
        x = [i]*2
        y = [i]*2
        z = [0, 2]
        ax.plot3D(x, y, z, linestyle = '--', color = 'black', 
                  zorder = len(tiempos)+1, linewidth = 0.8)
        
        # Graficación.
        ax.scatter3D(0, 0, 2, color = 'black', zorder = len(tiempos)+1, 
                     linewidth = 0.8)
        ax.scatter3D(0, 0, 0, color = 'black', zorder = len(tiempos)+1, 
                     facecolor = 'none', linewidth = 0.8)
        
        # Número de iteración en curso (comentar para no imprimir).
        print(i)
        
    # Curva solución.
    else:
        
        # Número de iteración en curso (comentar para no imprimir).
        print(i)
        x = np.linspace(a, b, particion)
        y = [i]*particion
        z = [u(i, s, n) for s in x] 
        
        # Graficación.
        ax.plot3D(x, y, z, zorder = len(tiempos)-i, color = colores[j])

plt.show()