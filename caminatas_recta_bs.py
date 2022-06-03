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
                 MBBS que parten de un segmento de recta
===============================================================================
''' 

''' ============================== ALGORITMO ============================== '''

def coalescente(n, t_max, p1, p2, misma_escala_x = True, 
                misma_escala_y = True):

    # Primer caso: sin banco de semillas (las caminatas no se duermen). 
    # Equivalente al algoritmo del archivo caminatas_recta.py.
    if p1 == 0:
        
        # Si los parámetros misma_escala_x y misma_escala_y son True, la escala
        # de los ejes en el diagrama de coalescencias será idéntica a la del
        # coalescente.
        fig, (ax1, ax2) = plt.subplots(2, 1, sharey = misma_escala_y, 
                                       sharex = misma_escala_x, 
                                       figsize=(6.4, 9.6))
        
        ########## Primera figura: aproximación al flujo de Arratia ##########
        
        # Inicialización.
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
              
            # Se verifica si hay colisión con la última caminata guardada. En 
            # caso de haberla, se aplica la regla de coalescencia.
            for i in range(len(caminata)):
                if caminata[i] == caminatas[-1][i]:
                        caminata[i+1:] = caminatas[-1][i+1:]
                        break
                    
            # Se guarda la caminata.
            caminatas.append(caminata)
            
            # Graficación de la trayectoria.
            ax1.plot(caminata, list(range(t_max+1)))
            
        ########## Segunda figura: diagrama de coalescencias ##########
                
        # En la matriz de caminatas se compara cada columna y se guarda el 
        # número de veces que aparecen los valores repetidos. Estos valores 
        # representan a los puntos de coalescencia.
        df = pd.DataFrame(caminatas)
        df = df.drop([0])
        contador = 0
        
        ax2.scatter(df[0].to_numpy(), [0]*n, color = 'blue', zorder = 3)
        
        puntos = []
            
        for i in range(len(df.columns)):
            
            # Número de iteración en curso (comentar para no imprimir).
            print(str(i))
            
            columna = np.array(df[i])
            repetidos = [item for item, count in 
                         collections.Counter(columna).items() if count > 1]
            df = df.drop_duplicates(subset = i, ignore_index = True)

            # Se cuenta el número de coalescencias en cada columna (en cada 
            # tiempo) y se grafican los puntos de coalescencia.
            if len(repetidos) > 0:
                contador += len(repetidos)
                tiempo = [i]*len(repetidos)    
                ax2.scatter(repetidos, tiempo, color = 'red', zorder = 3)
                
            puntos.extend([j, i] for j in repetidos)
        caminatas.pop(0)
        
        # Tiempo de última coalescencia (punto con el valor de tiempo más 
        # grande dentro del conjunto de puntos).
        tuc = np.max([k[1] for k in puntos])
            
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
    
    # Segundo caso: con banco de semillas (probabilidad de dormir positiva).
    else:
        
        # Si los parámetros misma_escala_x y misma_escala_y son True, la escala
        # de los ejes en el diagrama de coalescencias será idéntica a la del 
        # coalescente.
        fig, (ax1, ax2) = plt.subplots(2, 1, sharey = misma_escala_y, 
                                       sharex = misma_escala_x, 
                                       figsize = (6.4, 9.6))
        
        ########## Primera figura: caminatas con banco de semillas ##########

        # Inicialización.
        registro = [0.5]*(t_max+1)
        caminatas = [registro]
        registro_despiertos = [registro]
        registro_dormidos = [registro]
        
        # Se genera cada una de las caminatas con banco de semillas.
        for j in range(0, 2*n, 2): 
            
            # Inicialización de la caminata.
            caminata = [j]
            valor = j    
            despierto = [j]
            dormido = [j]
            
            # Se genera la caminata con banco de semillas, de acuerdo con el
            # archivo mbbs_esc_alt.py.
            while len(caminata) <= t_max:
                
                aleatorio = np.random.uniform()
                
                # Caminata despierta.
                if aleatorio < 1/2*(1-p1):
                    valor = valor-1
                    caminata.append(valor)
                    despierto.append(valor) 
                    dormido.append(str(j))
                    
                elif aleatorio < 1-p1:
                    valor += 1
                    caminata.append(valor)
                    despierto.append(valor)
                    dormido.append(str(j))
                 
                # Caminata dormida.
                else:
                    valor = valor
                    caminata.append(valor)
                    despierto.append(str(j))
                    dormido.append(valor)
                    continuar = True
                    while continuar and len(caminata) <= t_max:       
                        aleatorio = np.random.uniform()
                        if aleatorio < 1-2*p2:
                            caminata.extend([valor, valor])
                            despierto.extend([str(j), str(j)])
                            dormido.extend([valor, valor])
                        else:
                            caminata.append(valor)
                            despierto.append(valor)
                            dormido.append(str(j))
                            continuar = False  
                            
            # Se trunca la caminata hasta el tiempo máximo de simulación t_max.
            caminata = caminata[0:t_max+1]
            despierto = despierto[0:t_max+1] 
            dormido = dormido[0:t_max+1]
            
            # Verificación de las coalescencias.
            for i in range(len(caminata)):
                for k in range(len(registro_despiertos)):
                    if despierto[i] == registro_despiertos[k][i] or dormido[i] == registro_dormidos[k][i]:
                        caminata[i+1:] = caminatas[k][i+1:]
                        despierto[i+1:] = registro_despiertos[k][i+1:]
                        dormido[i+1:] = registro_dormidos[k][i+1:]
                        break
            
            # Actualización de las listas.
            caminatas.append(caminata)
            registro_despiertos.append(despierto)
            registro_dormidos.append(dormido)
            
            # Graficación.
            ax1.plot(caminata, list(range(t_max+1)))
         
        ########## Segunda figura: diagrama de coalescencias ##########
        
        # En la matriz de caminatas se compara cada columna y se guarda el 
        # número de veces que aparecen los valores repetidos. Estos valores 
        # representan a los puntos de coalescencia.
        df = pd.DataFrame(caminatas)
        df = df.drop([0])
        contador = 0
        ax2.scatter(df[0].to_numpy(), [0]*n, color = 'blue',
                    zorder = 3)
        puntos = []
        for i in range(len(df.columns)):
            
            # Número de iteración en curso (comentar para no imprimir).
            print(i)
            columna = np.array(df[i])
            repetidos = [item for item, count in 
                         collections.Counter(columna).items() if count > 1]
            for k in repetidos:
                indices = [i for i, x in enumerate(columna) if x == k]
                
                # En este caso, una vez que hay intersección de dos
                # trayectorias se comparan las mismas al tiempo siguiente para
                # revisar si coalescieron o no. En caso de no haberlo hecho, se
                # ignora la intersección y no se considera como punto de 
                # coalescencia.
                for r in range(1, len(indices)):
                    if i < len(df.columns)-1 and df[i+1][indices[r]] != df[i+1][indices[r-1]]:
                        repetidos.remove(k)
                        df[i][indices[r-1]] = None
                        break
                    
            df = df.drop_duplicates(subset = i, ignore_index=True)
            
            # Se cuenta el número de coalescencias en cada columna (en cada 
            # tiempo) y se grafican los puntos de coalescencia.
            if len(repetidos) > 0:
                contador += len(repetidos)
                tiempo = [i]*len(repetidos)
                ax2.scatter(repetidos, tiempo, color = 'red',
                            zorder = 3)
                puntos.extend([j, i] for j in repetidos)
        caminatas.pop(0)
        
        # Tiempo de última coalescencia (punto con el valor de tiempo más 
        # grande dentro del conjunto de puntos).
        tuc = np.max([k[1] for k in puntos])
        
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
                           linestyles = 'dashed',
                           color = 'gray')
            else:
                ax2.vlines(punto[0], ultimo_tiempo, tuc, 
                           linestyles = 'dashed',
                           color = 'gray')
        
        # Elementos de graficación.
        ax1.grid()
        ax2.grid()
        ax1.set_ylabel('Tiempo')
        ax1.set_xlabel('Posición')
        ax2.set_ylabel('Tiempo')
        ax2.set_xlabel('Posición')
        plt.show()
        
        # En caso de que no coincidan el número de caminos restantes con el
        # número de trayectorias iniciales menos el número de coalescencias, se
        # arroja un mensaje de alerta. Esto ocurre puesto que es probable que
        # tres trayectorias coincidan al mismo tiempo debido alescalamiento
        # alternativo. Por ejemplo, si dos trayectorias despiertas colisionan y
        # una más se duerme justo en ese punto. En este caso el número de 
        # coalescencias es uno, pero tres trayectorias toman el mismo valor en 
        # el mismo tiempo. En este caso, favor de volver a ejecutar el
        # programa.
        if contador != n-df.shape[0]:
            print("Es posible (pero no seguro) que haya un error en la " +
                  "gráfica del coalescente, pues tres caminos coinciden al " + 
                  "mismo tiempo.")
            
    # La función regresa el número de coalescencias producidas y el tiempo de
    # última coalescencia.
    return contador, tuc

''' ============================= PARÁMETROS ============================= '''

# Número de caminatas.
n = 30

# Tiempo máximo de simulación.
t_max = 1000

# Probabilidad de dormir.
p1 = 0.03

# Probabilidad de despertar.
p2 = 0.03

# Misma escala en el eje x.
misma_escala_x = False

# Misma escala en el eje y.
misma_escala_y = False

''' ============================== EJECUCIÓN ============================== '''

print(coalescente(n, t_max, p1, p2, misma_escala_x, misma_escala_y))