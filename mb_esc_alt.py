'''
Tesis - Simulación de procesos coalescentes 
Enrique Moctezuma González

'''

# Librerías.
import numpy as np
import matplotlib.pyplot as plt

''' 
===============================================================================
            Movimiento browniano con el escalamiento alternativo
===============================================================================           
           
'''

''' ============================== ALGORITMO ============================== '''

def movimiento_browniano_escalamiento_alternativo(n):
    
    # Inicialización.
    valores = [0]
    tiempos = list(range(n+1))
    
    # Simulación del movimiento browniano con el escalamiento alternativo.
    for i in range(n):
        aleatorio = np.random.uniform()
        if aleatorio <= 0.5:
            valores.append(valores[-1]-1)
        else:
            valores.append(valores[-1]+1)
            
    # Graficación.
    plt.plot(tiempos, valores, color = 'cadetblue')
    plt.grid()
    plt.xlabel('Tiempo')
    plt.ylabel('Posición')
    plt.show()
    
    # La función regresa los valores de la caminata.
    return valores

''' ============================= PARÁMETROS ============================= '''

# Número de pasos.
n = 1000

''' ============================== EJECUCIÓN ============================== '''

print(movimiento_browniano_escalamiento_alternativo(n))