'''
Tesis - Simulación de procesos coalescentes 
Enrique Moctezuma González

'''

# Librerías.
import numpy as np
import matplotlib.pyplot as plt

'''
===============================================================================
               MBBS con el escalamiento browniano alternativo
===============================================================================
''' 

''' ============================== ALGORITMO ============================== '''

def mbbs_escalamiento_alternativo(n, p1, p2):
    
    # Inicialización.
    valores = [0]  
    valor = 0
    
    while len(valores) <= n:
        
        # Mientras la trayectoria se encuentre despierta, se simula un 
        # movimiento browniano con el escalamiento alternativo. Los pasos son
        # dados con equiprobabilidad, pero el número p1 influye.
        aleatorio = np.random.uniform()
        
        if aleatorio < 1/2*(1-p1):
            valor = valor-1
            valores.append(valor)
            
        elif aleatorio < 1-p1:
            valor += 1
            valores.append(valor)
            
        # Si la trayectoria se duerme, entonces entra al espacio Z^2_{impar} y
        # su comportamiento es constante (se agrega el mismo valor a la lista).
        # Se encontrará aquí mientras continuar = True. Se realizan las 
        # correcciones indicadas en la parte escrita (pasos dobles y 
        # probabilidad de despertar duplicada).
        else:
            valor = valor
            valores.append(valor)
            continuar = True
            
            while continuar and len(valores) <= n:
                aleatorio = np.random.uniform()
        
                if aleatorio < 1-2*p2:
                    valores.extend([valor, valor])
                    
                else:
                    valores.append(valor)
                    continuar = False
    
    # Se trunca la lista a la longitud deseada.
    valores = valores[0:n+1]
    
    # Graficación.
    plt.plot(list(range(1001)), valores, color = 'red', zorder = 2)
     
    # Elementos de graficación.     
    plt.ylabel('Posición')
    plt.xlabel('Tiempo')
    plt.axhline(0, color = 'black', zorder = 1)
    plt.axvline(0, color = 'black', zorder = 1)
    plt.grid()
    plt.show()
    
    # La función regresa los valores tomados por la trayectoria.
    return valores

''' ============================= PARÁMETROS ============================= '''

# Número de pasos.
n = 1000

# Probabilidad de dormir.
p1 = 0.01

# Probabilidad de despertar.
p2 = 0.01

''' ============================== EJECUCIÓN ============================== '''

print(mbbs_escalamiento_alternativo(n, p1, p2))