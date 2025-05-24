import pygame

# ---> Configuración de las dimensiones de la ventana y el juego
ANCHO_JUEGO = 600 # Ancho del área donde se dibuja el puzzle
ANCHO_INFO = 200 # Ancho del panel lateral para información y botones
ANCHO_TOTAL = ANCHO_JUEGO + ANCHO_INFO + 60 # Ancho total de la ventana (juego + info + márgenes)
ALTO = 600 # Alto de la ventana

FILAS, COLUMNAS = 3, 3 # Dimensiones del puzzle (3x3 para el Puzzle de 8)
TAMANO_PIEZA = ANCHO_JUEGO // COLUMNAS # Tamaño en píxeles de cada pieza del puzzle

# ---> Definición de colores en formato RGB
COLOR_FONDO = (25, 25, 25) # Fondo general
COLOR_BORDE = (255, 255, 255) # Bordes y líneas (blanco)
COLOR_TEXTO = (255, 255, 255) # Color del texto (blanco)
COLOR_NUMERO_PIEZA = (255, 255, 255) # Color del número en la pieza (blanco)
COLOR_GANADO = (0, 255, 0) # Verde para el mensaje de victoria

# Colores para los botones
COLOR_BOTON_MENU = (65, 105, 225) # Azul para el botón de inicio del menú
COLOR_BOTON_A = (0, 0, 250) # Azul para el botón A*
COLOR_BOTON_BFS = (255, 0, 0) # Rojo para el botón BFS
COLOR_BOTON_REINICIAR = (50, 150, 50) # Verde para el botón Reiniciar
COLOR_BOTON_TEXTO = (255, 255, 255) # Texto de los botones (blanco)
COLOR_PIEZA = (50, 50, 50) # Color de fondo de las piezas con números

# ---> Inicialización de Pygame
pygame.init() # Inicializa todos los módulos de Pygame
PANTALLA = pygame.display.set_mode((ANCHO_TOTAL, ALTO)) # Configura la ventana principal
pygame.display.set_caption("Puzzle de 8 Piezas con Agentes") # Establece el título de la ventana

# ---> Definición de Fuentes
FUENTE_GRANDE = pygame.font.Font(None, 80) # Fuente para títulos grandes ("PUZZLE 8")
FUENTE_MEDIA = pygame.font.Font(None, 36) # Fuente para texto de tamaño medio ("Iniciar")
FUENTE_PEQUENA = pygame.font.Font(None, 24) # Fuente para texto pequeño (información del juego, botones)
FUENTE_NUMERO_PIEZA = pygame.font.Font(None, int(TAMANO_PIEZA * 0.7)) # Fuente para los números de las piezas

# ---> ESTADO OBJETIVO DEL PUZZLE
# Define la disposición de las piezas que se considera el estado "resuelto" o "meta" del puzzle.
# El '0' representa el espacio vacío. Este es el 'Goal State' al que los agentes de IA deben llegar.
# Se define como una tupla de tuplas para asegurar que es inmutable, para su uso como claves en diccionarios o elementos en conjuntos en los algoritmos de búsqueda.
ESTADO_OBJETIVO_TUPLA = (
    (1, 2, 3),
    (8, 0, 4),
    (7, 6, 5)
)

# ---> ESTADO INICIAL BÁSICO PARA LA MEZCLA
# Este es el tablero en un estado "resuelto" y secuencial desde el cual se inicia la mezcla.
# Es una lista de listas porque la función 'mezclar_tablero' necesita modificarla temporalmente.
ESTADO_INICIAL_BASICO_LISTA = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

# ---> Definición de las áreas de los botones (Rectángulos de Pygame)
BOTON_RESOLVER_A_RECT = pygame.Rect(ANCHO_JUEGO + 30, 370, ANCHO_INFO - 60, 40) # Botón para activar el agente A*.
BOTON_RESOLVER_BFS_RECT = pygame.Rect(ANCHO_JUEGO + 30, 430, ANCHO_INFO - 60, 40) # Botón para activar el agente BFS.
BOTON_REINICIAR_RECT = pygame.Rect(ANCHO_JUEGO + 30, 490, ANCHO_INFO - 60, 40) # Botón para reiniciar el juego.
BOTON_INICIAR_RECT = pygame.Rect(ANCHO_TOTAL // 2 - 75, ALTO // 2 + 50, 150, 60) # Botón del menú, centrado