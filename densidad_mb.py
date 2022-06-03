'''
Tesis - Simulación de procesos coalescentes 
Enrique Moctezuma González

'''

# Librerías.
import numpy as np
import matplotlib.pyplot as plt

'''  
===============================================================================
                      Densidad del TUC de las caminatas  
===============================================================================

'''

''' ============================== ALGORITMO ============================== '''

def interseccion_mb(n, t_max, graficacion = True):
         
    # Inicialización.
    tiempo_coalescencia = t_max
    
    # Primera caminata.
    valor = 0    
    caminata1 = [valor]
    while len(caminata1) <= t_max:
        aleatorio = np.random.uniform()
        if aleatorio < 0.5:
            valor = valor-1
            caminata1.append(valor)
        else: 
            valor += 1
            caminata1.append(valor)
      
    # Segunda caminata.
    valor = 2*n-2
    caminata2 = [valor]
    while len(caminata2) <= t_max:
        aleatorio = np.random.uniform()
        if aleatorio < 0.5:
            valor = valor-1
            caminata2.append(valor)
        else: 
            valor += 1
            caminata2.append(valor)
               
    # Se verifica si hay colisión entre las dos trayectorias.
    for i in range(len(caminata1)):
        if caminata1[i] == caminata2[i]:
                tiempo_coalescencia = i
                caminata1[i+1:] = caminata2[i+1:]
                break
        
    # Graficación de las trayectorias.
    if graficacion:
        plt.plot(caminata1, list(range(t_max+1)))
        plt.plot(caminata2, list(range(t_max+1)))
        if tiempo_coalescencia < t_max:
            plt.scatter(caminata1[i], i)
        plt.xlabel('Tiempo')
        plt.ylabel('Posición')
        plt.show()
    
    # Se cuenta el número de caminos restantes al tiempo máximo.
    if tiempo_coalescencia < t_max:
        caminos_restantes = 1
    else:
        caminos_restantes = None
        
    # La función regresa el número de trayectorias restantes al tiempo máximo
    # y el tiempo de coalescencia de las mismas.
    return caminos_restantes, tiempo_coalescencia
    
#################### Histograma y curva ####################

def histograma(no_simulaciones, n, t_max, no_barras = 'auto'):
    
    # Densidad teórica.
    def densidad_teorica(t, x):
        return x/(2*np.sqrt(np.pi*t**3))*np.exp(-x**2/(4*t))
    
    # Densidad empírica.
    muestra = []
    contador = 0
    
    for i in range(no_simulaciones):
        
        # Número de iteración en curso (comentar para no imprimir).
        print(i)
        variable = interseccion_mb(n, t_max, graficacion = False)
        
        # Si el número de caminatas restantes fue 1, se guarda el tiempo de 
        # última coalescencia en el vector muestra.
        if variable[0] == 1:
            muestra.append(variable[1])
            contador += 1
            
    # Histograma.
    counts, bins = np.histogram(muestra, density = True, bins = no_barras)
    counts = len(muestra)/no_simulaciones*counts
    plt.hist(bins[:-1], weights = counts, bins = no_barras, 
              color = 'darkturquoise', label = 'Empírica')  
    
    # Curva.
    plt.plot(range(1, t_max+1), 
             [densidad_teorica(s, 2*n-2) for s in range(1, t_max+1)], 
             label = 'Teórica', color = 'red', linewidth = 2)
        
    # Elementos de graficación.
    plt.xlabel('Tiempo')
    plt.ylabel('Densidad')
    plt.grid()
    plt.legend()
    plt.show()
    
    # La función regresar el número de valores no excedentes.
    return contador

''' ============================= PARÁMETROS ============================= '''

# Número de simulaciones.
no_simulaciones = 1000

# Número de barras.
no_barras = 20

# Número de caminatas.
n = 10

# Tiempo máximo de simulación.
t_max = 1000

''' ============================== EJECUCIÓN ============================== '''

print(histograma(no_simulaciones, n, t_max, no_barras))