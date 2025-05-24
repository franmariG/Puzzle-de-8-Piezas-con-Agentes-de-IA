import pygame # Importa la biblioteca Pygame para las operaciones gráficas y de interfaz de usuario.
from config import * # Importa todas las constantes de configuración para la interfaz

def dibujar_tablero(tablero, tiempo_transcurrido, movimientos_realizados, resolviendo_agente, nodos_expandidos=0, tiempo_calculo_agente=0.0):
    """
    Dibuja el tablero del puzzle, las piezas numéricas y toda la información relevante del juego en la pantalla.
    """
    PANTALLA.fill(COLOR_FONDO) # Rellena toda la superficie de la pantalla con el color de fondo definido
    
    # ---> Dibujar las piezas del puzzle en su posición actual
    for r in range(FILAS):
        for c in range(COLUMNAS):
            valor = tablero[r][c] # Obtiene el valor (número) de la pieza en la posición (r, c).
            x = c * TAMANO_PIEZA # Calcula la coordenada X de la esquina superior izquierda de la pieza en la pantalla.
            y = r * TAMANO_PIEZA # Calcula la coordenada Y de la esquina superior izquierda de la pieza en la pantalla.
            
            if valor != 0: # Si no es el espacio vacío (pieza 0)
                # Dibujar el rectángulo de la pieza
                pygame.draw.rect(PANTALLA, COLOR_PIEZA, (x, y, TAMANO_PIEZA, TAMANO_PIEZA))
                # Dibujar el número de la pieza
                texto_pieza = FUENTE_NUMERO_PIEZA.render(str(valor), True, COLOR_NUMERO_PIEZA)
                texto_rect = texto_pieza.get_rect(center=(x + TAMANO_PIEZA // 2, y + TAMANO_PIEZA // 2))
                PANTALLA.blit(texto_pieza, texto_rect)
                # Dibujar el borde de la pieza
                pygame.draw.rect(PANTALLA, COLOR_BORDE, (x, y, TAMANO_PIEZA, TAMANO_PIEZA), 2)
            else: # Es el espacio vacío
                pygame.draw.rect(PANTALLA, COLOR_FONDO, (x, y, TAMANO_PIEZA, TAMANO_PIEZA)) # Dibuja un rectángulo del color de fondo
                pygame.draw.rect(PANTALLA, COLOR_BORDE, (x, y, TAMANO_PIEZA, TAMANO_PIEZA), 2) # Dibuja un borde para el espacio vacío
    
    # ---> Dibujar la sección de información del juego
    
    # Título de la sección de referencia
    texto_referencia_titulo = FUENTE_PEQUENA.render("Meta:", True, COLOR_BORDE)
    PANTALLA.blit(texto_referencia_titulo, (ANCHO_JUEGO + 30, 25))

    # Mostrar la meta del puzzle
    for r_obj in range(FILAS):
        for c_obj in range(COLUMNAS):
            valor_obj = ESTADO_OBJETIVO_TUPLA[r_obj][c_obj] # Obtiene el valor del estado objetivo.
            # Ajustar la posición para que esté dentro del panel de información
            x_obj = ANCHO_JUEGO + 45 + c_obj * (TAMANO_PIEZA // 3) # Reducir tamaño para la meta
            y_obj = 60 + r_obj * (TAMANO_PIEZA // 3)

            if valor_obj != 0: # Si no es el espacio vacío 
                # Dibuja el número de la meta.
                texto_meta = FUENTE_PEQUENA.render(str(valor_obj), True, COLOR_NUMERO_PIEZA)
                PANTALLA.blit(texto_meta, (x_obj, y_obj))
            else: # Si es el espacio vacío
                # Muestra un guión para el 0 en la meta
                texto_meta = FUENTE_PEQUENA.render("-", True, COLOR_NUMERO_PIEZA)
                PANTALLA.blit(texto_meta, (x_obj, y_obj))

    # Tiempo transcurrido en el juego
    minutos = int(tiempo_transcurrido // 60) # Calcula los minutos.
    segundos = int(tiempo_transcurrido % 60) # Calcula los segundos restantes
    texto_tiempo = FUENTE_PEQUENA.render(f"Tiempo de Juego: {minutos:02}:{segundos:02}", True, COLOR_TEXTO) # Formatea el tiempo a "MM:SS"
    PANTALLA.blit(texto_tiempo, (ANCHO_JUEGO + 30, 240))  # Posición del texto del tiempo.

    # Número de movimientos realizados por el jugador o el agente
    texto_movimientos = FUENTE_PEQUENA.render(f"Movimientos: {movimientos_realizados}", True, COLOR_TEXTO)
    PANTALLA.blit(texto_movimientos, (ANCHO_JUEGO + 30, 270)) # Posición del texto de movimientos.
    
    # Mostrar información adicional de los agentes solo si se ha ejecutado una solución
    if nodos_expandidos > 0 or tiempo_calculo_agente > 0.0:
        texto_nodos_expandidos = FUENTE_PEQUENA.render(f"Nodos Exp.: {nodos_expandidos}", True, COLOR_TEXTO)
        PANTALLA.blit(texto_nodos_expandidos, (ANCHO_JUEGO + 30, 300)) # Posición del texto de nodos expandidos.
        
        texto_tiempo_calculo = FUENTE_PEQUENA.render(f"Tiempo de Cálculo: {tiempo_calculo_agente:.4f}s", True, COLOR_TEXTO)
        PANTALLA.blit(texto_tiempo_calculo, (ANCHO_JUEGO + 30, 330)) # Posición del texto de tiempo de cálculo.

    # ---> Dibujar los botones de control
    # Botón para resolver con el agente A*
    pygame.draw.rect(PANTALLA, COLOR_BOTON_A, BOTON_RESOLVER_A_RECT)
    texto_boton_a = FUENTE_PEQUENA.render("Resolver (A*)", True, COLOR_BOTON_TEXTO)
    PANTALLA.blit(texto_boton_a, texto_boton_a.get_rect(center=BOTON_RESOLVER_A_RECT.center))

    # Botón para resolver con el agente BFS
    pygame.draw.rect(PANTALLA, COLOR_BOTON_BFS, BOTON_RESOLVER_BFS_RECT)
    texto_boton_bfs = FUENTE_PEQUENA.render("Resolver (BFS)", True, COLOR_BOTON_TEXTO)
    PANTALLA.blit(texto_boton_bfs, texto_boton_bfs.get_rect(center=BOTON_RESOLVER_BFS_RECT.center))

    # Botón para reiniciar el juego
    pygame.draw.rect(PANTALLA, COLOR_BOTON_REINICIAR, BOTON_REINICIAR_RECT)
    texto_boton_reiniciar = FUENTE_PEQUENA.render("Reiniciar", True, COLOR_BOTON_TEXTO)
    PANTALLA.blit(texto_boton_reiniciar, texto_boton_reiniciar.get_rect(center=BOTON_REINICIAR_RECT.center))
    
    # Mensaje de estado cuando un agente está mostrando la solución
    if resolviendo_agente:
        texto_calculando = FUENTE_PEQUENA.render(f"Mostrando solución...", True, COLOR_TEXTO)
        PANTALLA.blit(texto_calculando, (ANCHO_JUEGO + 30, BOTON_REINICIAR_RECT.bottom + 20)) # Posición debajo del botón Reiniciar.


def dibujar_menu():
    """Dibuja la pantalla del menú principal del juego."""
    PANTALLA.fill(COLOR_FONDO) # Rellena toda la pantalla con el color de fondo para el menú.
    
    # Título del juego
    titulo_juego = FUENTE_GRANDE.render("PUZZLE 8", True, COLOR_TEXTO)
    titulo_rect = titulo_juego.get_rect(center=(ANCHO_TOTAL // 2, ALTO // 2 - 50))
    PANTALLA.blit(titulo_juego, titulo_rect)
    
    # Botón "Iniciar" para comenzar la partida
    pygame.draw.rect(PANTALLA, COLOR_BOTON_MENU, BOTON_INICIAR_RECT)
    texto_iniciar = FUENTE_MEDIA.render("Iniciar", True, COLOR_BOTON_TEXTO)
    texto_iniciar_rect = texto_iniciar.get_rect(center=BOTON_INICIAR_RECT.center)
    PANTALLA.blit(texto_iniciar, texto_iniciar_rect)

def dibujar_victoria(ancho_juego, alto):
    """
    Dibuja una pantalla de victoria superpuesta al juego cuando el puzzle es resuelto.
    """
    # Crea una superficie semitransparente para el efecto de oscurecimiento
    s = pygame.Surface((ancho_juego, alto), pygame.SRCALPHA) 
    s.fill((0,0,0,128)) # Rellena con negro y una transparencia de 128 (de 255)
    PANTALLA.blit(s, (0,0)) # Dibuja la superposición en la pantalla
    
    # Texto de victoria
    texto_victoria = FUENTE_GRANDE.render("¡Puzzle resuelto!", True, COLOR_GANADO)
    texto_rect_victoria = texto_victoria.get_rect(center=(ancho_juego // 2, alto // 2))
    PANTALLA.blit(texto_victoria, texto_rect_victoria)