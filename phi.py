'''
Tesis - Simulación de procesos coalescentes 
Enrique Moctezuma González

'''

# Librerías.
import numpy as np
import matplotlib.pyplot as plt

''' 
===============================================================================
                               Función phi
===============================================================================

'''

''' ============================== ALGORITMO ============================== '''

def phi(alpha, beta, renovaciones):
    
    # Inicialización.
    tiempos_alpha = [0]
    tiempos_beta = [0]
    tiempos = [0]
    
    for i in range(renovaciones):
        
        # Tiempos exponenciales T = E+F.
        tiempo_alpha = np.random.exponential(1/alpha)
        tiempos_alpha.append(tiempo_alpha)
        tiempos_alpha.append(0)
        
        tiempo_beta = np.random.exponential(1/beta)
        tiempos_beta.append(0)
        tiempos_beta.append(tiempo_beta)
        
        tiempos.append(tiempo_alpha)
        tiempos.append(tiempo_beta)
    
    # Tiempos acumulados.
    tiempos_acum = np.cumsum(tiempos)
    tiempos_alpha_acum = np.cumsum(tiempos_alpha)
    tiempos_beta_acum = np.cumsum(tiempos_beta)
    
    fig, ax = plt.subplots(constrained_layout = True)
    
    for j in range(1, len(tiempos)):
        
        # Segmentos que crecen como la identidad.
        if j % 2 != 0:
            ax.plot([tiempos_acum[j-1], tiempos_acum[j]], 
                     [tiempos_acum[j-1]-tiempos_beta_acum[j], 
                      tiempos_acum[j]-tiempos_beta_acum[j]],
                     color = 'red')
         
        # Segmentos constantes.
        else:
            ax.plot([tiempos_acum[j-1], tiempos_acum[j]], 
                     [tiempos_alpha_acum[j-1], tiempos_alpha_acum[j-1]], 
                     color = 'blue')
     
    # Elementos de graficación.
    ax.tick_params(bottom = False)
    for k in range(2*renovaciones-1):
        
        # Líneas que denotan los tiempos E.
        if k % 2 == 0:
            ax.axvline(tiempos_acum[k+1], color = 'gray', linestyle = '-.', 
                       zorder = 3)
        
        # Líneas que denotan los tiempos F (coinciden con los tiempos T).
        else:
            ax.axvline(tiempos_acum[k+1], color = 'gray', linestyle = '--', 
                       zorder = 3)
    
    # Colocación de las letras horizontales (tiempos).
    puntos_medios = [(tiempos_acum[j]+tiempos_acum[j-1])/2 for j in range(1, 
                     len(tiempos_acum))]
    ax.set_xticks(puntos_medios)
    etiquetas = []
    for i in range(1, renovaciones+1):
        etiquetas.append(r'$E_'+str(i)+'$')
        etiquetas.append(r'$F_'+str(i)+'$')
    
    # Colocación de las letras verticales (alturas).
    ax.set_xticklabels(etiquetas)
    ax.set_yticks(np.unique(np.delete(tiempos_alpha_acum, 0)))
    ax.set_yticklabels([r'$E_'+str(i)+'$' for i in range(1, renovaciones+1)])
    ax.axvline(0, color = 'black', linewidth = 1)
    ax.axhline(0, color = 'black', linewidth = 1)
    ax.set_xlabel(r'$t$', size = 10)
    ax.set_ylabel(r'$\phi_{t}$', size = 15)
    
    # Tiempos interarribo.
    interarribo = []
    for k in range(len(tiempos_acum)):
        if k % 2 == 0:
            interarribo.append(tiempos_acum[k])
            
    secax = ax.secondary_xaxis('top')
    secax.set_xticks(np.delete(interarribo, -1))
    secax.set_xticklabels(np.append(['0'],[r'$T_'+str(i)+'$' for i in range(1, 
                          len(interarribo)-1)]))
    plt.show()
    
    # La función regresa los tiempos de interarribo.
    return interarribo

''' ============================= PARÁMETROS ============================= '''

# Parámetro alpha.
alpha = 1

# Parámetro beta.
beta = 1

# Número de renovaciones.
renovaciones = 4

''' ============================== EJECUCIÓN ============================== '''

print(phi(alpha, beta, renovaciones))