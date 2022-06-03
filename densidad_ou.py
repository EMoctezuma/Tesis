'''
Tesis - Simulación de procesos coalescentes 
Enrique Moctezuma González

'''

# Librerías.
import numpy as np
import matplotlib.pyplot as plt
import sympy as sy

''' 
===============================================================================
                     Intersecciones de procesos de OU 
===============================================================================

'''

''' ============================== ALGORITMO ============================== '''

# Método de Euler-Maruyama.
def euler_maruyama(n, t_max, x0, f, g, graficacion = True):
    
    # Inicialización
    
    # Variables introducidas como elementos de Sympy.
    x = sy.Symbol('x')
    t = sy.Symbol('t')
    
    # Funciones introducidas como elementos de Sympy.
    
    # Coeficiente de deriva.
    f = sy.sympify(f)
    f_dt = lambda posicion, tiempo: f.evalf(subs = {x: posicion, t: tiempo})
    
    # Coeficiente de difusión.
    g = sy.sympify(g)
    g_Bt = lambda posicion, tiempo: g.evalf(subs = {x: posicion, t: tiempo})
    
    # Condición inicial.
    X = [x0]
    
    # Intervalo temporal de simulación.
    tiempos = np.linspace(0, t_max, n)
    
    # Esquema iterativo de Euler-Maruyama.
    for i in range(1, len(tiempos)):
        Y = np.random.normal(0, 1)
        X.append(X[-1]+f_dt(X[-1], tiempos[-1])*t_max/n+
                 g_Bt(X[-1], tiempos[-1])*np.sqrt(t_max/n)*Y)

    # Elementos de graficación.
    if graficacion:
        plt.plot(np.linspace(0, t_max, n), X, 
                 label='Trayectoria del proceso')
        plt.xlabel('Tiempo')
        plt.ylabel('Valor')
        plt.grid()
        plt.legend()
        plt.show()
    
    # La función regresa la lista con los valores del proceso.
    return X

# Intersección de dos procesos de OU.
def punto_de_interseccion(n, t_max, x0, x1, f, g, graficacion = True):
    
    # Tomar x0 < x1.
    
    # Inicialización.
    tiempos = np.linspace(0, t_max, n)
    tuc = 0
    altura = 0
    
    # Simulación de las trayectorias.
    trayectoria1 = euler_maruyama(n, t_max, x0, f, g, False)
    trayectoria2 = euler_maruyama(n, t_max, x1, f, g, False)
    
    # Verificación de la condición de paro (con la corrección realizada para
    # aproximar el punto de intersección).
    for i in range(len(trayectoria1)):
        if trayectoria1[i] >= trayectoria2[i]:
            
            tuc = (tiempos[i]+tiempos[i-1])/2
            altura = (trayectoria1[i]+trayectoria1[i-1])/2
            
            # Graficación del punto de intersección.
            if graficacion:
                plt.scatter(tuc, altura, color = 'red', 
                            label = 'Intersección (aprox.): ('+
                            str(np.round(tuc, 4))+', '+
                            str(np.round(float(altura), 4))+')',
                            zorder = 3)
            break
     
    if graficacion:
        
        # Graficación de las trayectorias.
        plt.plot(tiempos, trayectoria1, color = 'turquoise', 
                  label = 'c.i.: '+str(x1))
        plt.plot(tiempos, trayectoria2, color = 'yellowgreen', 
                  label = 'c.i.: '+str(x0))
        
        # Elementos de graficación.
        plt.grid()
        plt.legend()
        plt.xlabel('Tiempo')
        plt.ylabel('Posición')
        plt.show()
    
    # La función regresa las coordenadas del punto de intersección.
    return tuc, altura
 
# Función de densidad de la intersección de dos procesos de OU.
def curva(t, x, y, sigma, alpha):
    t1 = (np.sqrt(2)*(x-y)*np.exp(2*alpha*t)*alpha**(3/2))/(sigma*np.sqrt(np.pi)*(np.exp(2*alpha*t)-1)**(3/2))
    t2 = np.exp(-(alpha*(x-y)**2)/(2*sigma**2*(np.exp(2*alpha*t)-1)))
    return t1*t2

# Histograma de intersecciones.
def histograma(no_simulaciones, no_barras, n, t_max, x0, x1, f, g, sigma):    

    # Inicialización.    
    muestra = []
    tiempos = np.linspace(0, t_max, n)[1:]

    contador = 0
    
    # Generación de la muestra.
    for j in range(no_simulaciones):
        
        # Número de iteración en curso (comentar para no imprimir).
        print(j)
        
        punto = punto_de_interseccion(n, t_max, x0, x1, f, g, 
                                      graficacion = False)
        if punto[0] != 0:
            muestra.append(punto[0])
            contador += 1
      
    # Histograma.
    counts, bins = np.histogram(muestra, density = True, bins = no_barras)
    counts = len(muestra)/no_simulaciones*counts
    plt.hist(bins[:-1], weights = counts, bins = no_barras, 
             color = 'darkturquoise', label = 'Empírica')  
      
    # Graficación.
    
    # Curva de la densidad teórica.
    plt.plot(tiempos, [curva(i, x1, x0, sigma, 1) for i in tiempos], 
             color = 'red', label = 'Teórica')
    
    # Elementos de graficación.
    plt.legend()
    plt.xlabel('Tiempo')
    plt.ylabel('Densidad')
    plt.grid()
    plt.show()
    
    # La función regresa el número de valores no excedentes.
    return contador

''' ============================= PARÁMETROS ============================= '''

# Para ambas funciones:

# Número de pasos.
n = 1000

# Tiempo máximo de simulación.
t_max = 10

# Primera condición inicial (recordar que x0 < x1).
x1 = 3

# Segunda condición inicial (recordar que x0 < x1).
x0 = 0

# Coeficiente de deriva.
f = '-x'

# Coeficiente de difusión.
g = '0.25'

# Varianza (únicamente se utiliza para la graficación de la curva de la
# curva de la densidad teórica). Debe coincidir con la constante que se 
# encuentra en el coeficiente de difusión.
sigma = 0.25

# Para la función 'histograma':

# Número de simulaciones.
no_simulaciones = 100

# Número de barras.
no_barras = 10

''' ============================== EJECUCIÓN ============================== '''

print(punto_de_interseccion(n, t_max, x0, x1, f, g, graficacion = True))
print(histograma(no_simulaciones, no_barras, n, t_max, x0, x1, f, g, sigma))