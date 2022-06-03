'''
Tesis - Simulación de procesos coalescentes 
Enrique Moctezuma González

'''

# Librerías.
import numpy as np
import matplotlib.pyplot as plt

''' 
===============================================================================
             Movimiento browniano con el escalamiento usual
===============================================================================           
           
'''

''' ============================== ALGORITMO ============================== '''

def movimiento_browniano_escalamiento_usual(n):
    
    # Inicialización.
    valores = [0]
    particion = np.linspace(0, 1, n)
    
    # Simulación del movimiento browniano con el escalamiento usual.
    for i in range(len(particion)-1):
        aleatorio = np.random.uniform()
        if aleatorio <= 0.5:
            valores.append(valores[-1]-1/np.sqrt(n))
        else:
            valores.append(valores[-1]+1/np.sqrt(n))
            
    # Graficación.
    plt.plot(particion, valores, color = 'mediumseagreen')
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

print(movimiento_browniano_escalamiento_usual(n))