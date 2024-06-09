import pygame
import random

# Configuración del tablero
Fila = 5
Column = 5
CELL_SIZE = 50
WIDTH = Column * CELL_SIZE
HEIGHT = Fila * CELL_SIZE

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Inicialización de Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ratón y Gato")

# Generar posiciones iniciales
def generar_posiciones():
    while True:
        Cat_pos = (random.randint(0, Fila - 1), random.randint(0, Column - 1))
        Mouse_pos = (random.randint(0, Fila - 1), random.randint(0, Column - 1))
        Exit_pos = (random.randint(0, Fila - 1), random.randint(0, Column - 1))
        if Cat_pos != Mouse_pos and Mouse_pos != Exit_pos and Cat_pos != Exit_pos:
            break
    return Cat_pos, Mouse_pos, Exit_pos

Cat_pos, Mouse_pos, Exit_pos = generar_posiciones()

# Función para dibujar el tablero
def ilustrar():
    screen.fill(WHITE)
    for i in range(Fila):
        for j in range(Column):
            rect = pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BLACK, rect, 1)
            if (i, j) == Cat_pos:
                pygame.draw.circle(screen, RED, rect.center, CELL_SIZE // 2 - 5)
            elif (i, j) == Mouse_pos:
                pygame.draw.circle(screen, GREEN, rect.center, CELL_SIZE // 2 - 5)
            elif (i, j) == Exit_pos:
                pygame.draw.circle(screen, BLACK, rect.center, CELL_SIZE // 2 - 5)
    pygame.display.flip()

# Función para obtener movimientos válidos
def mov_validos(pos):
    movimientos = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    posibles_movimientos = []
    for movimiento in movimientos:
        nueva_pos = (pos[0] + movimiento[0], pos[1] + movimiento[1])
        if 0 <= nueva_pos[0] < Fila and 0 <= nueva_pos[1] < Column:
            posibles_movimientos.append(nueva_pos)
    return posibles_movimientos

# Función para verificar el estado del juego
def check_win(Mouse_pos, Cat_pos, Exit_pos):
    if Mouse_pos == Exit_pos:
        return 1  # El ratón gana
    elif Cat_pos == Mouse_pos:
        return -1  # El gato gana
    else:
        return 0  # El juego continúa

# Algoritmo Minimax
def minimax(profundidad, esMax, Mouse_pos, Cat_pos):
    resultado = check_win(Mouse_pos, Cat_pos, Exit_pos)
    if resultado != 0 or profundidad == 0:
        return resultado
    
    if esMax:  # Turno del ratón (Max)
        mejor_valor = -float('inf')
        for nueva_pos in mov_validos(Mouse_pos):
            valor = minimax(profundidad - 1, False, nueva_pos, Cat_pos)
            mejor_valor = max(mejor_valor, valor)
        return mejor_valor
    else:  # Turno del gato (Min)
        mejor_valor = float('inf')
        for nueva_pos in mov_validos(Cat_pos):
            valor = minimax(profundidad - 1, True, Mouse_pos, nueva_pos)
            mejor_valor = min(mejor_valor, valor)
        return mejor_valor

# Función para mover al ratón usando Minimax
def mover_ratón_con_minimax(Mouse_pos, Cat_pos, profundidad=5):
    mejor_valor = -float('inf')
    mejor_movimiento = Mouse_pos
    for nueva_pos in mov_validos(Mouse_pos):
        valor = minimax(profundidad - 1, False, nueva_pos, Cat_pos)
        if valor > mejor_valor:
            mejor_valor = valor
            mejor_movimiento = nueva_pos
    return mejor_movimiento

# Función para mover al gato usando Minimax
def mover_gato_con_minimax(Mouse_pos, Cat_pos, profundidad=5):
    mejor_valor = float('inf')
    mejor_movimiento = Cat_pos
    for nueva_pos in mov_validos(Cat_pos):
        valor = minimax(profundidad - 1, True, Mouse_pos, nueva_pos)
        if valor < mejor_valor:
            mejor_valor = valor
            mejor_movimiento = nueva_pos
    return mejor_movimiento

# Bucle principal del juego
running = True
clock = pygame.time.Clock()

# Estado inicial
print("Posiciones iniciales")
ilustrar()

# Simulación del juego
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movimiento del ratón
    if Mouse_pos != Exit_pos:
        Mouse_pos = mover_ratón_con_minimax(Mouse_pos, Cat_pos)
    if Mouse_pos != Cat_pos:
        Cat_pos = mover_gato_con_minimax(Mouse_pos, Cat_pos)
        
    ilustrar()
    
    if Mouse_pos == Exit_pos:
        print('El ratón gana')
        running = False
    if Mouse_pos == Cat_pos:
        print('El gato gana')
        running = False

    clock.tick(1)  # Ajusta la velocidad del juego a 1 FPS

pygame.quit()
