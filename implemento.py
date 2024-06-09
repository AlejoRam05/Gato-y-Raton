"""Agregare una funcion RECURSIVA, la cual tendra que realizar una optimizacion de mi codigo.
El objetivo del mismo seria poder calcular la ruta más rapida/obtimizada para el minijuego"""

import random

Fila = 6
Column = 6
movimientos_previos = set()
def generar_posiciones():
    """Genera posiciones aleatorias únicas para el gato, el ratón y la salida"""
    while True:
        Cat_pos = (random.randint(0, Fila - 1), random.randint(0, Column - 1))
        Mouse_pos = (random.randint(0, Fila - 1), random.randint(0, Column - 1))
        Exit_pos = (random.randint(0, Fila - 1), random.randint(0, Column - 1))
        if Cat_pos != Mouse_pos and Mouse_pos != Exit_pos and Cat_pos != Exit_pos:
            break
    return Cat_pos, Mouse_pos, Exit_pos

Cat_pos, Mouse_pos, Exit_pos = generar_posiciones()

def ilustrar():
    """Muestra a los personajes dentro de la terminal"""
    for i in range(Fila):
        for j in range(Column):
            if (i, j) == Cat_pos:
                print('🐱', end=' ')
            elif (i, j) == Mouse_pos:
                print('🐭', end=' ')
            elif (i, j) == Exit_pos:
                print('E', end=' ')
            else:
                print('.', end=' ')
        print()
    print()

def mov_validos(pos, movimientos_previos):
    """Retorna los movimientos válidos para una posición dada"""
    movimientos = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    posibles_movimientos = []
    for movimiento in movimientos:
        nueva_pos = (pos[0] + movimiento[0], pos[1] + movimiento[1])
        if 0 <= nueva_pos[0] < Fila and 0 <= nueva_pos[1] < Column:
            posibles_movimientos.append(nueva_pos)
    return posibles_movimientos

def check_win(Mouse_pos, Cat_pos, Exit_pos):
    """Comprueba el estado del juego"""
    if Mouse_pos == Exit_pos:
        return 1  # El ratón gana
    elif Cat_pos == Mouse_pos:
        return -1  # El gato gana
    else:
        return 0  # El juego continúa

def minimax(profundidad, esMax, Mouse_pos, Cat_pos, movimientos_previos):
    resultado = check_win(Mouse_pos, Cat_pos, Exit_pos)
    if resultado != 0 or profundidad == 0:
        return resultado
    
    if esMax:  # Turno del ratón (Max)
        mejor_valor = -float('inf')
        for nueva_pos in mov_validos(Mouse_pos, movimientos_previos):
            valor = minimax(profundidad - 1, False, nueva_pos, Cat_pos, movimientos_previos)
            mejor_valor = max(mejor_valor, valor)
        return mejor_valor
    else:  # Turno del gato (Min)
        mejor_valor = float('inf')
        for nueva_pos in mov_validos(Cat_pos, movimientos_previos):
            valor = minimax(profundidad - 1, True, Mouse_pos, nueva_pos, movimientos_previos)
            mejor_valor = min(mejor_valor, valor)
        return mejor_valor

def mover_ratón_con_minimax(Mouse_pos, Cat_pos, profundidad=3):
    """Usa Minimax para mover al ratón"""
    mejor_valor = -float('inf')
    mejor_movimiento = Mouse_pos
    for nueva_pos in mov_validos(Mouse_pos, movimientos_previos):
        valor = minimax(profundidad - 1, False, nueva_pos, Cat_pos, movimientos_previos)
        if valor > mejor_valor:
            mejor_valor = valor
            mejor_movimiento = nueva_pos
    return mejor_movimiento

def mover_gato_con_minimax(Mouse_pos, Cat_pos, profundidad=5):
    """Usa Minimax para mover al gato"""
    mejor_valor = float('inf')
    mejor_movimiento = Cat_pos
    for nueva_pos in mov_validos(Cat_pos, movimientos_previos):
        valor = minimax(profundidad - 1, True, Mouse_pos, nueva_pos, movimientos_previos)
        if valor < mejor_valor:
            mejor_valor = valor
            mejor_movimiento = nueva_pos
    return mejor_movimiento








# Estado inicial
print("Posiciones iniciales")
ilustrar()

# Simulación del juego
for _ in range(100):
    if Mouse_pos != Exit_pos:
        Mouse_pos = mover_ratón_con_minimax(Mouse_pos, Cat_pos)
    if Mouse_pos != Cat_pos:
        Cat_pos = mover_gato_con_minimax(Mouse_pos, Cat_pos)
        
    ilustrar()
    
    if Mouse_pos == Exit_pos:
        print('El ratón gana')
        break
    if Mouse_pos == Cat_pos:
        print('El gato gana')
        break

            
    
    
    
        