'''
Tesis - Simulación de procesos coalescentes 
Enrique Moctezuma González

'''

# Librerías.
import numpy as np
from math import comb
import matplotlib.pyplot as plt

''' 
===============================================================================
                          Coalescente de Kingman
===============================================================================           
           
'''

''' ============================== ALGORITMO ============================== '''

def coalescente_de_kingman(n):
    
    # Inicialización.
    tiempos = []
    alturas = [0]*n
    pi = [i for i in range(n)]
    
    # Simulación del coalescente de Kingman.
    
    # Individuos iniciales
    fig, ax = plt.subplots(constrained_layout = True)
    ax.tick_params(bottom = False)
    plt.scatter(np.linspace(0, n-1, n), alturas, zorder = 2)
    
    # Proceso de reducción de la lista y graficación simultánea.
    while len(pi) > 1:
        
        # Simulación del tiempo exponencial.
        tiempo = np.random.exponential(1/comb(len(pi), 2))
        
        # Elección de individuos y creación del ancestro.
        eleccion = np.random.choice(list(range(len(pi))), 2, replace = False)  
        pto_medio = np.sum([pi[k] for k in eleccion])/2 
        
        tiempos.append(tiempo)
        altura = np.sum(tiempos)
        
        # ACMR (para la última iteración).
        if len(pi) == 2: 
            plt.scatter(pto_medio, altura, color = 'red', zorder = 2,
                        label = r'$\tau_{ACMR}\approx$'+
                        str(np.round(np.sum(tiempos), 4)))
        else:
            plt.scatter(pto_medio, altura, color = 'limegreen', zorder = 2)
        
        # Conexión de los individuos.
        for j in eleccion:
             plt.plot([pi[j], pto_medio], [alturas[j], altura], color = 'gray',
                      zorder = 0)
             
        # Actualización de las listas.
        alturas = np.delete(alturas, eleccion)
        alturas = np.append(alturas, altura)
        pi = np.delete(pi, eleccion)
        pi = np.append(pi, pto_medio)
        
    # Elementos de graficación.
    ax.axhline(0, color = 'black', zorder = 0)
    
    for i in np.cumsum(tiempos):
        ax.axhline(i, color = 'gray', linestyle = '--', linewidth = 1, 
                   zorder = 0)
    ax.set_xticks([])
    ax.set_yticks(np.append([0], np.cumsum(tiempos)))
    etiquetas = [r'$T_'+str(n)+'=0$']
    
    for i in range(1, n):
        etiquetas.append(r'$T_'+str(n-i)+
                         r'\approx$'+str(np.round(np.cumsum(tiempos)[i-1], 4)))
    ax.set_yticklabels(etiquetas)
    ax.legend()
    
    # La función regresa los tiempos exponenciales generados.
    return tiempos

''' ============================= PARÁMETROS ============================= '''

# Número de generaciones.
n = 7

''' ============================== EJECUCIÓN ============================== '''

print(coalescente_de_kingman(7))