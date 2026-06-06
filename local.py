# local.py
import random
import math

def calcular_ataques(estado):
    """
    Función base que cuenta cuántas parejas de reinas se están atacando mutuamente.
    El 'estado' es una lista de 8 números (columnas), el valor es la fila.
    """
    ataques = 0
    n = len(estado)
    for i in range(n):
        for j in range(i + 1, n):
            # 1. Conflicto en la misma fila
            if estado[i] == estado[j]:
                ataques += 1
            # 2. Conflicto en la misma diagonal
            elif abs(estado[i] - estado[j]) == abs(i - j):
                ataques += 1
    return ataques

def obtener_vecinos_locales(estado):
    """
    Genera el vecindario N(s) moviendo una sola reina a la vez 
    a cualquier otra fila de su misma columna.
    """
    vecinos = []
    n = len(estado)
    for col in range(n):
        for fila in range(n):
            if fila != estado[col]:
                nuevo_estado = list(estado)
                nuevo_estado[col] = fila
                vecinos.append(nuevo_estado)
    return vecinos

def buscar_hill_climbing(inicio):
    """
    Algoritmo Hill Climbing (Escalada Simple).
    Busca MAXIMIZAR F(s) = -Ataques. 
    Se mueve al PRIMER vecino que encuentra que sea mejor.
    """
    estado_actual = list(inicio)
    # Convención F(s) = -Ataques
    f_actual = -calcular_ataques(estado_actual)
    historial_pasos = []
    
    # Registramos el paso inicial en el historial (se guarda el número positivo para la interfaz)
    historial_pasos.append((estado_actual, abs(f_actual)))
    
    while True:
        vecinos = obtener_vecinos_locales(estado_actual)
        un_vecino_mejoro = False
        
        # PROCEDIMIENTO DE ESCALADA SIMPLE:
        # Recorremos los vecinos y nos movemos en el PRIMERO que aumente el valor de F(s)
        for v in vecinos:
            f_v = -calcular_ataques(v)
            if f_v > f_actual:  # Criterio de mejora: F(v) > F(actual)
                estado_actual = v
                f_actual = f_v
                historial_pasos.append((estado_actual, abs(f_actual)))
                un_vecino_mejoro = True
                break  # ¡Lógica de Escalada Simple! Dejamos de revisar los demás vecinos
                
        # Criterio de paro: Si ningún vecino de todo el vecindario mejoró, se detiene
        if not un_vecino_mejoro:
            break
            
    return estado_actual, historial_pasos

def buscar_recocido_simulado(inicio):
    """
    Algoritmo de Recocido Simulado.
    Busca MINIMIZAR Energía E(s) = Ataques.
    Acepta algunos movimientos peores bajo un criterio probabilístico exponencial.
    """
    estado_actual = list(inicio)
    # E(s) = Ataques
    e_actual = calcular_ataques(estado_actual)
    historial_pasos = []
    
    # Parámetros iniciales del cronograma de enfriamiento
    T = 10.0
    T_min = 0.01
    alfa = 0.95  # Enfriamiento exponencial estándar
    
    historial_pasos.append((estado_actual, e_actual))
    
    while T > T_min and e_actual > 0:
        vecinos = obtener_vecinos_locales(estado_actual)
        # Seleccionamos un vecino al azar del vecindario
        vecino_aleatorio = random.choice(vecinos)
        e_v = calcular_ataques(vecino_aleatorio)
        
        # Cálculo del cambio de energía deltaE = E(s') - E(s)
        delta_e = e_v - e_actual
        
        # Criterio de Aceptación:
        if delta_e <= 0:
            # Si reduce energía (o empata), se acepta automáticamente sin sorteo
            estado_actual = vecino_aleatorio
            e_actual = e_v
            historial_pasos.append((estado_actual, e_actual))
        else:
            # Si el vecino empeora (deltaE > 0), sorteamos con la probabilidad de Boltzmann
            probabilidad = math.exp(-delta_e / T)
            if random.random() < probabilidad:
                estado_actual = vecino_aleatorio
                e_actual = e_v
                historial_pasos.append((estado_actual, e_actual))
                
        # Decremento de la Temperatura según el Schedule exponencial
        T *= alfa
        
    return estado_actual, historial_pasos