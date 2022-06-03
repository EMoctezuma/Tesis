'''
Tesis - Simulación de procesos coalescentes 
Enrique Moctezuma González

'''

# Librerías.
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import collections

''' 
===============================================================================
             Movimientos brownianos coalescentes en la recta
===============================================================================           
           
'''

''' ============================== ALGORITMO ============================== '''

def caminatas_en_la_recta(n, t_max, graficacion = True, misma_escala_x = True, 
                          misma_escala_y = True):
    
    # Si los parámetros misma_escala_x y misma_escala_y son True, la escala
    # de los ejes en el diagrama de coalescencias será idéntica a la del
    # coalescente.
    if graficacion:
        fig, (ax1, ax2) = plt.subplots(2, 1, sharey = misma_escala_y, 
                                       sharex = misma_escala_x, 
                                       figsize = (6.4, 9.6))
    
    ########## Primera figura: aproximación al flujo de Arratia ##########
    
    # Inicialización
    caminatas = [[0.5]*(t_max+1)]

    # Se genera cada una de las caminatas en los números pares de la recta
    # t = 0.
    for j in range(0, 2*n, 2):    
        caminata = [j]
        valor = j    
        while len(caminata) <= t_max:
            aleatorio = np.random.uniform()
            if aleatorio < 0.5:
                valor = valor-1
                caminata.append(valor)
            else: 
                valor += 1
                caminata.append(valor)
          
        # Se verifica si hay colisión con la última caminata guardada. En caso
        # de haberla, se aplica la regla de coalescencia.
        for i in range(len(caminata)):
            if caminata[i] == caminatas[-1][i]:
                    caminata[i+1:] = caminatas[-1][i+1:]
                    break
                
        # Se guarda la caminata.
        caminatas.append(caminata)
        
        # Graficación de la trayectoria.
        if graficacion:
            ax1.plot(caminata, list(range(t_max+1)))
        
    ########## Segunda figura: diagrama de coalescencias ##########
            
    # En la matriz de caminatas se compara cada columna y se guarda el 
    # número de veces que aparecen los valores repetidos. Estos valores 
    # representan a los puntos de coalescencia.
    df = pd.DataFrame(caminatas)
    df = df.drop([0])
    contador = 0
    
    if graficacion:
        ax2.scatter(df[0].to_numpy(), [0]*n, color = 'blue', zorder = 3)
    
    puntos = []
        
    for i in range(len(df.columns)):
        
        # Número de iteración en curso (comentar para no imprimir).
        print(str(i))
        
        columna = np.array(df[i])
        repetidos = [item for item, count in 
                     collections.Counter(columna).items() if count > 1]
        df = df.drop_duplicates(subset = i, ignore_index = True)

        # Se cuenta el número de coalescencias en cada columna (es decir, en  
        # cada tiempo) y se grafican los puntos de coalescencia.
        if len(repetidos) > 0:
            contador += len(repetidos)
            tiempo = [i]*len(repetidos)
            
            if graficacion:
                ax2.scatter(repetidos, tiempo, color = 'red', zorder = 3)
            
        puntos.extend([j, i] for j in repetidos)
    caminatas.pop(0)
    
    # Tiempo de última coalescencia (punto con el valor de tiempo más 
    # grande dentro del conjunto de puntos).
    tuc = np.max([k[1] for k in puntos])
        
    if graficacion:
        
        # Se unen los puntos de coalescencia mediante segmentos de recta de 
        # acuerdo con las trayectorias que chocaron.
        for i in caminatas:
            punto = [i[0], 0]
            ultimo_tiempo = 0
            for j in range(t_max+1):
                for k in puntos:
                    if [i[j], j] == k:
                        ax2.plot([punto[0], i[j]], [punto[1], j], 
                                 color = 'gray')
                        punto = k
                        ultimo_tiempo = j
                        break
                    
            # Líneas punteadas en el diagrama de coalescencias.
            if misma_escala_y:
                ax2.vlines(punto[0], ultimo_tiempo, t_max+1, 
                           linestyles = 'dashed', color = 'gray')
            else:
                ax2.vlines(punto[0], ultimo_tiempo, tuc, linestyles = 'dashed',
                           color = 'gray')
                
        # Elementos de graficación.
        ax1.grid()
        ax2.grid()
        ax1.set_ylabel('Tiempo')
        ax1.set_xlabel('Posición')
        ax2.set_ylabel('Tiempo')
        ax2.set_xlabel('Posición')
        plt.show()
    
    # La función regresa el número de coalescencias producidas y el tiempo de
    # última coalescencia.
    return contador, tuc

''' ============================= PARÁMETROS ============================= '''

# Número de caminatas.
n = 30

# Tiempo máximo de simulación.
t_max = 1000

# Graficación.
graficacion = True

# Misma escala en el eje x.
misma_escala_x = False

# Misma escala en el eje y.
misma_escala_y = False

''' ============================== EJECUCIÓN ============================== '''

print(caminatas_en_la_recta(n, t_max, graficacion, misma_escala_x, 
                            misma_escala_y))