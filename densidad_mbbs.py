'''
Tesis - Simulación de procesos coalescentes 
Enrique Moctezuma González

'''

# Librerías.
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

''' ============================== ALGORITMO ============================== '''

def mbbs_segmento_de_recta(n, t_max, p1, p2, graficacion = True):
    
    # Primer caso: sin banco de semillas (las caminatas no se duermen).
    if p1 == 0:
        
        # Inicialización.
        tuc = t_max
        caminatas = [[0.5]*(t_max+1)]
        
        # Se simula cada una de las trayectorias.
        for j in [0, 2*n-2]:
            caminata = [j]
            valor = j   
            
            while len(caminata) <= t_max:
                aleatorio = np.random.uniform()
                if aleatorio < 1/2:
                    valor = valor-1
                    caminata.append(valor)
                elif aleatorio < 1:
                    valor += 1
                    caminata.append(valor)
            
            # Verificación de la coalescencia.
            for i in range(len(caminata)):
                if caminata[i] == caminatas[-1][i]:
                    tuc = i
                    caminata[i+1:] = caminatas[-1][i+1:]
                    break
                
            # Se agrega la caminata generada a la lista.
            caminatas.append(caminata)
            
            # Graficación de la trayectoria.
            if graficacion:
                plt.plot(caminata, list(range(t_max+1)))
            
        caminatas.pop(0)
        
        # Si se alcanzó la última coalescencia, caminos_restantes = 1. Si no,
        # restan al menos dos trayectorias.
        if tuc < t_max:
            caminos_restantes = 1
        else:
            caminos_restantes = 2
            
        # Elementos de graficación.
        if graficacion:
            plt.grid()
            plt.xlabel('Tiempo')
            plt.ylabel('Posición')
            plt.show()
            
        # En este caso, la función regresa el número de caminos restantes y el
        # tiempo de última coalescencia.
        return caminos_restantes, tuc
    
    # Segundo caso: con banco de semillas (probabilidad de dormir positiva).
    else:
        
        # Inicialización.
        caminatas = [[0.5]*(t_max+1)]
        registro_despiertos = [[0.5]*(t_max+1)]
        registro_dormidos = [[0.5]*(t_max+1)]
        
        # Se simula cada una de las trayectorias.
        for j in range(0, 2*n, 2):    
            caminata = [j]
            valor = j    
            despierto = [j]
            dormido = [j]
            
            while len(caminata) <= t_max:
                aleatorio = np.random.uniform()
                
                # Despierta.
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
                    
                # Dormida.
                else:
                    valor = valor
                    caminata.append(valor)
                    despierto.append(str(j))
                    dormido.append(valor)
                    continuar = True
                    
                    while continuar and len(caminata) <= t_max:       
                        aleatorio = np.random.uniform()
                        
                        if aleatorio < 1-p2:
                            caminata.extend([valor, valor])
                            despierto.extend([str(j), str(j)])
                            dormido.extend([valor, valor])
                        
                        else:
                            caminata.append(valor)
                            despierto.append(valor)
                            dormido.append(str(j))
                            continuar = False  
                            
            # Se truncan las listas al tamaño indicado.
            caminata = caminata[0:t_max+1]
            despierto = despierto[0:t_max+1] 
            dormido = dormido[0:t_max+1]
            
            # Verificación de la coalescencia.
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
            
            # Graficación de la trayectoria.
            if graficacion:
                plt.plot(caminata, list(range(t_max+1)))
                
        # Elementos de graficación.
        if graficacion:
            plt.xlabel('Tiempo')
            plt.ylabel('Posición')
            plt.grid()
            plt.show()
            
        # Se convierte a la matriz de caminatas en un data frame.
        df = pd.DataFrame(caminatas)
        df = df.drop([0])
        
        # Se toma a cada una de las columnas del data frame y se observa el 
        # número de elementos únicos. Si solo hay un elemento único en la 
        # columna i, significa que todas las caminatas valen lo mismo en este 
        # tiempo. Se toma entonces la siguiente columna y se repite el 
        # procedimiento. Si también hay un solo elemento único, significa que 
        # en la columna anterior (es decir, el tiempo i) se produjo la última 
        # coalescencia. Si no, al menos dos caminatas se cruzaron sin 
        # coalescer al tiempo i. Al terminar el procedimiento, se verifica si  
        # se produjo o no la última coalescencia antes del tiempo máximo 
        # establecido.
        for i in range(len(df.columns)-1):
            columna = np.array(df[i])
            if len(np.unique(columna)) == 1 and len(np.unique(np.array(df[i+1]))) == 1:
                plt.show()
                return 1, i
        
        # El mismo procedimiento se realiza para las últimas dos columnas.
        if len(np.unique(df[t_max-1])) == 1 and len(np.unique(df[t_max])) == 1:
            return 1, t_max-1
        
    # La función regresa el número de caminos restantes (si la coalescencia no 
    # se produjo antes del tiempo t_max) y t_max.
    return len(np.unique(np.array(df[t_max]))), t_max

########## Histograma ##########

def histograma(no_simulaciones, n, t_max, p1, p2, no_barras = 'auto'):
     
    # Densidad empírica.
    muestra = []
    contador = 0
    
    for i in range(no_simulaciones):
        
        # Número de iteración en curso (comentar para no imprimir).
        print(i)
        variable = mbbs_segmento_de_recta(n, t_max, p1, p2, False)
        
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
no_barras = 25

# Número de caminatas.
n = 10

# Tiempo máximo de simulación.
t_max = 3000

# Probabilidad de dormir.
p1 = 0.3

# Probabilidad de despertar.
p2 = 0.3

''' ============================== EJECUCIÓN ============================== '''

print(histograma(no_simulaciones, n, t_max, 0.3, 0.3, no_barras))