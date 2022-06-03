'''
Tesis - Simulación de procesos coalescentes 
Enrique Moctezuma González

'''

# Librerías.
import numpy as np
import matplotlib.pyplot as plt

''' 
===============================================================================
                  Caminatas coalescentes en el plano
===============================================================================           
           
'''

''' ============================== ALGORITMO ============================== '''

def caminatas_en_el_plano(n, x_max, t_max):
    
    # Inicialización.
    registro = [[0.5]*(t_max+1)]
    tiempo = list(range(t_max+1))
    caminata = [0]
    valor = 0
    
    # Primera caminata (siempre comienza en (0,0)).
    while len(caminata) <= t_max:    
        aleatorio = np.random.uniform()     
        if aleatorio < 0.5:
            valor = valor-1
            caminata.append(valor)
        else:
            valor += 1
            caminata.append(valor)
    
    # Se agrega la caminata al vector registro.
    registro.append(caminata)
    plt.plot(caminata, tiempo)
    
    # Resto de caminatas (comienzan en puntos en [0, x_max] X [0, t_max]).
    for k in range(n-1):
        m = 1
        j = 0
        
        # Se selecciona el punto en la retícula Z^2_{par}.
        while (m+j)%2 != 0:
            j = np.random.randint(x_max)
            m = np.random.randint(t_max)
        
        # Se genera la caminata correspondiente al punto de inicio. Nótese que
        # las primeras m+1 entradas no tienen formato numérico.
        caminata = [str(j)+','+str(m)]*(m+1)
        valor = j
        while len(caminata) <= t_max:    
            aleatorio = np.random.uniform()     
            if aleatorio < 0.5:
                valor = valor-1
                caminata.append(valor)
            else:
                valor += 1
                caminata.append(valor)
                 
        # Se compara la caminata generada con las anteriores para que, en caso
        # de intersección, se aplique la regla de coalescencia y sigan la misma
        # trayectoria.
        caminata = caminata[0:t_max+1]
        for i in range(len(caminata)):
            for k in range(len(registro)):
                if caminata[i] == registro[k][i]:
                    caminata[i+1:] = registro[k][i+1:]
                    break
                
        # Se agrega la caminata generada al registro.
        registro.append(caminata)
        
        # Graficación.
        plt.plot(caminata[m+1:i+1], tiempo[m+1:i+1])
     
    # Elementos de graficación.
    plt.xlabel('Posición')
    plt.ylabel('Tiempo')
    
    # Descomentar las siguientes dos líneas para fijar los límites del 
    # rectángulo [0, x_max] X [0, t_max] en la visualización de la figura.
    #plt.xlim(0, x_max)
    #plt.ylim(0, t_max)
    
    plt.show()
    
    # La función solo regresa la figura.
    
''' ============================= PARÁMETROS ============================= '''

# Número de caminatas.
n = 100

# Máximo del intervalo espacial.
x_max = 10

# Máximo del intervalo temporal.
t_max = 10

''' ============================== EJECUCIÓN ============================== '''

print(caminatas_en_el_plano(n, x_max, t_max))