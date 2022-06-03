'''
Tesis - Simulación de procesos coalescentes 
Enrique Moctezuma González

'''

# Librerías.
import numpy as np
import matplotlib.pyplot as plt

'''
===============================================================================
                 MBBS que parten de puntos en el plano
===============================================================================
''' 

''' ============================== ALGORITMO ============================== '''

def caminatas_bs_en_el_plano(x_max, t_max, n, p1, p2):
    
    # Primera caminata (siempre comienza en (0,0)).
    
    # Inicialización.
    caminatas = [[0.5]*(t_max+1)]
    registro_despiertos = [[0.5]*(t_max+1)]
    registro_dormidos = [[0.5]*(t_max+1)]
    
    # Esta lista guardará la información de la caminata a partir del punto en
    # el que ésta comienza. Las primeras entradas serán datos de tipo
    # caracter.
    tiempo = list(range(t_max+1))
    caminata = [0]
    valor = 0
    despierto = [0]
    dormido = [0]
    
    # Simulación de la trayectoria.
    while len(caminata) <= t_max: 
        
        aleatorio = np.random.uniform()  
        
        # Despierta.
        if aleatorio < 1/2*(1-p1):
            valor = valor-1
            caminata.append(valor)
            despierto.append(valor)  
            dormido.append(str(0))
        elif aleatorio < 1-p1:
            valor += 1
            caminata.append(valor)
            despierto.append(valor)  
            dormido.append(str(0))
            
        # Dormida.
        else:
            valor = valor         
            caminata.append(valor)         
            despierto.append(str(0))    
            dormido.append(valor)        
            continuar = True 
            
            while continuar and len(caminata) <= t_max: 
                
                aleatorio = np.random.uniform()
                
                if aleatorio < 1-p2:
                    caminata.extend([valor, valor])
                    despierto.extend([str(0), str(0)])  
                    dormido.extend([valor, valor])   
                    
                else:
                    caminata.append(valor)
                    despierto.append(valor)
                    dormido.append(str(0))
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
    plt.plot(caminata, tiempo)
    
    # Resto de caminatas (comienzan en puntos en [0, x_max] X [0, t_max]).
    
    # Selección aleatoria del punto de inicio en Z^2_{par}.
    for k in range(n-1):
        m = 1
        j = 0
        while (m+j)%2 != 0:
            j = np.random.randint(x_max)
            m = np.random.randint(t_max)
                    
        # Inicializaión.
        caminata = [str(j)]*(m+1)
        valor = j
        despierto = [str(j)+','+str(m)]*(m+1)
        dormido = [str(j)+','+str(m)]*(m+1)
        
        # Simulación de la caminata.
        while len(caminata) <= t_max: 
            
            aleatorio = np.random.uniform()  
            
            # Despierta.
            if aleatorio < 1/2*(1-p1):
                valor = valor-1
                caminata.append(valor)
                despierto.append(valor) 
                dormido.append(str(j)+','+str(m))
                
            elif aleatorio < 1-p1:
                valor += 1
                caminata.append(valor)
                despierto.append(valor)  
                dormido.append(str(j)+','+str(m))
            
            # Dormida.
            else:
                valor = valor         
                caminata.append(valor) 
                despierto.append(str(j)+','+str(m))  
                dormido.append(valor)
                continuar = True            
                while continuar and len(caminata) <= t_max:                
                    aleatorio = np.random.uniform()
                    if aleatorio < 1-p2:
                        caminata.extend([valor, valor])
                        despierto.extend([str(j)+','+str(m), 
                                          str(j)+','+str(m)])
                        dormido.extend([valor, valor])
                    else:
                        caminata.append(valor)
                        despierto.append(valor)
                        dormido.append(str(j)+','+str(m))
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
n = 200

# Máximo del intervalo espacial.
x_max = 120

# Máximo del intervalo temporal.
t_max = 1000

# Probabilidad de dormir.
p1 = 0.01

# Probabilidad de despertar.
p2 = 0.01

''' ============================== EJECUCIÓN ============================== '''

print(caminatas_bs_en_el_plano(x_max, t_max, n, p1, p2))