'''
Tesis - Simulación de procesos coalescentes 
Enrique Moctezuma González

'''

# Librerías.
import numpy as np
import matplotlib.pyplot as plt

''' 
===============================================================================
                MBBS con el escalamiento browniano usual
===============================================================================

'''

''' ============================== ALGORITMO ============================== '''

def mbbs_escalamiento_usual(n, renovaciones, alpha, beta):
    
    # Inicialización.
    tiempos = []
    
    # Generación de los tiempos exponenciales del proceso de renovación.
    for i in range(renovaciones):
        
        tiempo_alpha = np.random.exponential(1/alpha)
        tiempo_beta = np.random.exponential(1/beta)
        
        tiempos.append(tiempo_alpha)
        tiempos.append(tiempo_beta)
    
    # Tiempos acumulados.
    tiempos_acum = np.cumsum(tiempos)
    
    fig, ax = plt.subplots(constrained_layout = True)
    
    # Inicialización.
    
    particion = np.linspace(0, tiempos_acum[-1], n)
    
    # El MBBS comienza en 0.
    valores = [0]
    t = 0
    tiempo = particion[t]
    j = 0
    
    # A esta lista se agregarán los puntos de la partición en los que cambia el
    # comportamiento de la trayectoria.
    cortes = [0]
    
    # Ciclo que se repite el número de renovaciones indicado.
    for i in range(renovaciones):
        j += 1
        
        # Durante el primer tiempo exponencial se simula un movimiento
        # browniano estándar con el escalamiento usual.
        while tiempo < tiempos_acum[j-1]:
            aleatorio = np.random.uniform()
            if aleatorio <= 0.5:
                valores.append(valores[-1]-1/np.sqrt(n))
            else:
                valores.append(valores[-1]+1/np.sqrt(n))
            t += 1
            tiempo = particion[t]
            
        # Graficación (en rojo).
        ax.plot(particion[cortes[-1]:t+1], valores[cortes[-1]:], 
                color = 'red')
        
        cortes.append(t)
        j += 1
        
        # Durante el siguiente tiempo exponencial el proceso es constante.
        while tiempo < tiempos_acum[j-1]:
            valores.append(valores[-1])
            t += 1
            tiempo = particion[t]
            
        # Graficación (en azul).
        ax.plot(particion[cortes[-1]:t+1], valores[cortes[-1]:], 
                color = 'blue')
        
        cortes.append(t)
    
    # Elementos de graficación.
    ax.axvline(0, color = 'black', linewidth = 1)
    ax.axhline(0, color = 'black', linewidth = 1)
    ax.set_xlabel('Tiempo')
    ax.set_ylabel('Posición')
    
    ax.tick_params(bottom = False)
    
    # Líneas verticales en la figura.
    for k in range(2*renovaciones-1):
        if k % 2 == 0:
            ax.axvline(tiempos_acum[k], color = 'gray', linestyle = '-.', 
                       zorder = 3)
        else:
            ax.axvline(tiempos_acum[k], color = 'gray', linestyle = '--', 
                       zorder = 3)
     
    # Etiquetas en el eje horizontal de la figura.
    tiempos_acum = np.append([0], tiempos_acum)
    puntos_medios = [(tiempos_acum[j]+tiempos_acum[j-1])/2 for j in range(1, 
                     len(tiempos_acum))]
    ax.set_xticks(puntos_medios)
    etiquetas = []
    for i in range(1, renovaciones+1):
        etiquetas.append(r'$E_'+str(i)+'$')
        etiquetas.append(r'$F_'+str(i)+'$')
    
    interarribo = []
    for k in range(len(tiempos_acum)):
        if k % 2 == 0:
            interarribo.append(tiempos_acum[k])
        
    secax = ax.secondary_xaxis('top')
    secax.set_xticks(np.delete(interarribo, -1))
    secax.set_xticklabels(np.append(['0'], 
                          [r'$T_'+str(i)+'$' for i in range(1, renovaciones)]))
    
    ax.set_xticklabels(etiquetas)
    plt.show()
    
    # La función regresa los tiempos exponenciales generados y los valores de
    # la trayectorias.
    return tiempos, valores

''' ============================= PARÁMETROS ============================= '''

# Número de pasos.
n = 500

# Número de renovaciones.
renovaciones = 4

# Parámetro alpha.
alpha = 1

# Parámetro beta.
beta = 1

''' ============================== EJECUCIÓN ============================== '''

print(mbbs_escalamiento_usual(n, renovaciones, alpha, beta))