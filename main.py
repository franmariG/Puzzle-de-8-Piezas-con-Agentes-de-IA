import pygame # Importa la biblioteca Pygame para el desarrollo de juegos y gráficos
import time # Importa el módulo time para funciones relacionadas con el tiempo (temporizadores)

from config import * # Importa todas las constantes de configuración para el juego
from game_logic import mezclar_tablero, mover_pieza_en_tablero, verificar_victoria # Importa funciones de la lógica del juego
from agents import resolver_puzzle_a_estrella, resolver_puzzle_bfs # Importa las funciones de resolución de los agentes
from ui import dibujar_tablero, dibujar_menu, dibujar_victoria # Importa las funciones de dibujo de la interfaz

# ---> Constantes de estado del juego
STATE_MENU = 0 # Estado cuando se muestra el menú principal
STATE_GAME = 1 # Estado cuando se está jugando el puzzle

# ---> Variables de estado del juego (Globales para gestionar el estado de la aplicación) 
tablero_actual = [] # El estado actual del puzzle en la pantalla
juego_terminado = False # Bandera para indicar si el puzzle ha sido resuelto
ganador = False # Bandera para indicar si el jugador o agente ha ganado
inicio_tiempo = 0.0 # Marca de tiempo cuando el juego comienza o se reinicia
tiempo_final_juego = 0.0 # Almacena el tiempo exacto en que el juego termina (manual o por agente)

movimientos_jugador = 0 # Contador de movimientos realizados por el jugador o el agente

camino_solucion = [] # Lista de estados del tablero que forman la solución del agente para animación
indice_paso_actual = 0 # Índice del paso actual en la animación de la solución del agente
resolviendo_agente = False # Bandera para indicar si un agente está calculando o mostrando una solución
agente_actual_tipo = "" # Almacena el tipo de agente ('A*' o 'BFS')
tiempo_entre_pasos = 0.4 # Retraso en segundos entre cada paso de la animación del agente
ultimo_tiempo_paso = 0.0 # Marca de tiempo del último paso de la animación para controlar el retraso

nodos_expandidos_mostrar = 0 # Muestra el número de nodos expandidos por el agente
tiempo_calculo_mostrar = 0.0 # Muestra el tiempo que tardó el agente en calcular la solución

current_game_state = STATE_MENU # El estado inicial del juego es el menú

# ---> Funciones de control de estado del juego

def inicializar_variables_juego():
    """
    Reinicia todas las variables de estado del juego para comenzar una nueva partida.
    Genera un nuevo tablero mezclado y asegura que el temporizador y contadores se restablezcan.
    """
    # Variables globales a modificar.
    global tablero_actual, juego_terminado, ganador, inicio_tiempo, movimientos_jugador, \
           camino_solucion, indice_paso_actual, resolviendo_agente, agente_actual_tipo, \
           ultimo_tiempo_paso, nodos_expandidos_mostrar, tiempo_calculo_mostrar, tiempo_final_juego

    tablero_actual = mezclar_tablero() # Mezcla el tablero para una nueva partida

    juego_terminado = False # El juego no ha terminado
    ganador = False # No hay ganador aún
    inicio_tiempo = time.time() # Establece el tiempo de inicio de la partida
    tiempo_final_juego = 0.0 # Reinicia el tiempo final del juego

    movimientos_jugador = 0 # Reinicia el contador de movimientos
    camino_solucion = [] # Vacía el camino de solución del agente
    indice_paso_actual = 0 # Reinicia el índice de animación del agente
    resolviendo_agente = False # El agente no está activo
    agente_actual_tipo = "" # Sin agente seleccionado
    ultimo_tiempo_paso = 0.0 # Reinicia el control de tiempo de animación

    nodos_expandidos_mostrar = 0 # Reinicia el contador de nodos expandidos
    tiempo_calculo_mostrar = 0.0 # Reinicia el tiempo de cálculo del agente
    print("Juego inicializado. Nuevo puzzle generado.") # Mensaje de consola para depuración.

def manejar_eventos_menu(evento):
    """
    Maneja los eventos de usuario cuando el juego está en el estado de menú.
    Actualmente, solo detecta clics en el botón "Iniciar".
    """
    # Variable global a modificar.
    global current_game_state
    # Si el evento es un click del ratón.
    if evento.type == pygame.MOUSEBUTTONDOWN:
        # Si se hizo click en el botón "Iniciar"
        if BOTON_INICIAR_RECT.collidepoint(evento.pos):
            inicializar_variables_juego() # Prepara una nueva partida
            current_game_state = STATE_GAME # Cambia el estado a juego
            print("Iniciando juego desde el menú.") # Mensaje de consola para depuración.

def manejar_eventos_juego(evento):
    """
    Maneja los eventos de usuario cuando el juego está en el estado de juego.
    Incluye movimientos manuales, activación de agentes y reinicio del juego.
    """
    # Variables globales a modificar.
    global tablero_actual, juego_terminado, movimientos_jugador, ganador, \
           resolviendo_agente, agente_actual_tipo, camino_solucion, \
           indice_paso_actual, ultimo_tiempo_paso, nodos_expandidos_mostrar, \
           tiempo_calculo_mostrar, inicio_tiempo, tiempo_final_juego
    # Si el evento es un click del ratón.
    if evento.type == pygame.MOUSEBUTTONDOWN:
        mouse_x, mouse_y = evento.pos # Obtiene las coordenadas del click del ratón

        # ---> Lógica para el movimiento manual del jugador
        # Solo si el juego no ha terminado y ningún agente está resolviendo
        if not juego_terminado and not resolviendo_agente:
            if mouse_x < ANCHO_JUEGO and mouse_y < ALTO: # Si el click fue dentro del área del puzzle
                # Calcula la fila y columna de la pieza clickeada según el tamaño de las piezas.
                clic_columna = mouse_x // TAMANO_PIEZA
                clic_fila = mouse_y // TAMANO_PIEZA

                # Intenta mover la pieza, si el movimiento es válido
                if mover_pieza_en_tablero(tablero_actual, clic_fila, clic_columna):
                    movimientos_jugador += 1 # Incrementa el contador de movimientos
                    # Verifica si el puzzle ha sido resuelto después del movimiento
                    if verificar_victoria(tablero_actual):
                        juego_terminado = True # Marca el juego como terminado
                        ganador = True # Marca al jugador como ganador
                        resolviendo_agente = False # Asegura que el agente no esté activo
                        tiempo_final_juego = time.time() - inicio_tiempo # Guarda el tiempo final de la partida manual
                        print(f"¡Felicidades! Puzzle resuelto manualmente en {movimientos_jugador} movimientos y {tiempo_final_juego:.2f} segundos.")  # Mensaje de victoria para depuración

        # ---> Lógica para el botón "Resolver (A*)"
        # Verifica si el click colisionó con el botón A*.
        if BOTON_RESOLVER_A_RECT.collidepoint(evento.pos):
            # Solo si el juego no ha terminado y ningún agente está activo
            if not juego_terminado and not resolviendo_agente:
                resolviendo_agente = True # Activa el estado de resolución por agente
                agente_actual_tipo = "A*" # Establece el tipo de agente
                print("\nIniciando cálculo de la solución A*...") # Mensaje de inicio de cálculo para depuración
                
                # Reiniciar métricas para la nueva búsqueda del agente
                nodos_expandidos_mostrar = 0
                tiempo_calculo_mostrar = 0.0
                movimientos_jugador = 0 # Los movimientos del jugador se reinician al activar el agente
                inicio_tiempo = time.time() # Reinicia el tiempo para medir la duración de la solución del agente
                tiempo_final_juego = 0.0 # Asegura que el tiempo final se reinicie

                # Ejecuta el algoritmo A*
                camino_solucion_temp, nodos_expandidos_calculados, tiempo_calculado_agente = resolver_puzzle_a_estrella(tablero_actual)
                
                # Actualiza las métricas para la UI
                nodos_expandidos_mostrar = nodos_expandidos_calculados 
                tiempo_calculo_mostrar = tiempo_calculado_agente

                if camino_solucion_temp: # Si se encontró una solución
                    camino_solucion = camino_solucion_temp # Almacena el camino para la animación
                    indice_paso_actual = 0 # Reinicia el índice de la animación
                    ultimo_tiempo_paso = time.time() # Prepara el temporizador para la animación
                    # Imprime los resultados del cálculo del agente en consola
                    print(f"Solución A* encontrada en {tiempo_calculado_agente:.4f} segundos, expandiendo {nodos_expandidos_calculados} nodos. Longitud del camino: {len(camino_solucion) - 1} movimientos.")
                else: # Si no se encontró solución (camino_solucion_temp es None).
                    # Mensaje de depuración
                    print(f"No se encontró solución con A* después de expandir {nodos_expandidos_calculados} nodos. El puzzle podría ser irresoluble o la búsqueda fue incompleta.")
                    resolviendo_agente = False # Desactiva el estado de resolución si no hay solución

        # ---> Lógica para el botón "Resolver (BFS)"
        # Verifica si el click colisionó con el botón BFS.
        elif BOTON_RESOLVER_BFS_RECT.collidepoint(evento.pos):
            # Solo si el juego no ha terminado y ningún agente está activo
            if not juego_terminado and not resolviendo_agente:
                resolviendo_agente = True # Activa el estado de resolución por agente
                agente_actual_tipo = "BFS" # Establece el tipo de agente
                print("\nIniciando cálculo de la solución BFS...") # Mensaje de inicio de cálculo para depuración

                # Reiniciar métricas para la nueva búsqueda del agente
                nodos_expandidos_mostrar = 0
                tiempo_calculo_mostrar = 0.0
                movimientos_jugador = 0 # Los movimientos del jugador se reinician al activar el agente
                inicio_tiempo = time.time() # Reinicia el tiempo para medir la duración de la solución del agente
                tiempo_final_juego = 0.0 # Asegura que el tiempo final se reinicie
                
                # Ejecuta el algoritmo BFS
                camino_solucion_temp, nodos_expandidos_calculados, tiempo_calculado_agente = resolver_puzzle_bfs(tablero_actual)

                # Actualiza las métricas para la UI
                nodos_expandidos_mostrar = nodos_expandidos_calculados 
                tiempo_calculo_mostrar = tiempo_calculado_agente

                if camino_solucion_temp: # Si se encontró una solución
                    camino_solucion = camino_solucion_temp # Almacena el camino para la animación
                    indice_paso_actual = 0 # Reinicia el índice de la animación
                    ultimo_tiempo_paso = time.time() # Prepara el temporizador para la animación
                    # Imprime los resultados del cálculo del agente en consola
                    print(f"Solución BFS encontrada en {tiempo_calculado_agente:.4f} segundos, expandiendo {nodos_expandidos_calculados} nodos. Longitud del camino: {len(camino_solucion) - 1} movimientos.")
                else: # Si no se encontró solución
                    # Mensaje de depuración
                    print(f"No se encontró solución con BFS después de expandir {nodos_expandidos_calculados} nodos. El puzzle podría ser irresoluble o la búsqueda fue incompleta.")
                    resolviendo_agente = False # Desactiva el estado de resolución si no hay solución
        
        # ---> Lógica para el botón "Reiniciar"
        # Verifica si el click colisionó con el botón Reiniciar.
        elif BOTON_REINICIAR_RECT.collidepoint(evento.pos):
            inicializar_variables_juego() # Reinicia todas las variables y el tablero
            print("Juego reiniciado.") # Mensaje de consola para depuración
                
# ---> Bucle principal del juego
ejecutando = True # Bandera para mantener el bucle del juego en ejecución
while ejecutando:
    # Manejo de eventos: procesa todas las acciones del usuario (clicks, cierre de ventana, etc.)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT: # Si el usuario cierra la ventana
            ejecutando = False # Termina el bucle principal
            print("Saliendo del juego.") # Mensaje de salida para depuración
        
        # Dirige los eventos al manejador correspondiente según el estado actual del juego
        if current_game_state == STATE_MENU:
            manejar_eventos_menu(evento) # Si está en el menú, solo maneja eventos del menú.
        elif current_game_state == STATE_GAME:
            manejar_eventos_juego(evento) # Si está en el juego, maneja eventos de juego.

    # Lógica de actualización del juego (solo en el estado de juego)
    if current_game_state == STATE_GAME:
        # Actualización del temporizador del juego
        if not juego_terminado:  # Si el puzzle no ha sido resuelto aún.
            tiempo_transcurrido = time.time() - inicio_tiempo # El tiempo sigue corriendo si el juego no ha terminado
        else:
            tiempo_transcurrido = tiempo_final_juego # Si el juego terminó, el tiempo se "congela" en el valor final
            
        # Lógica de animación del agente (si un agente está resolviendo, no se ha terminado el juego y hay un camino de solución)
        if resolviendo_agente and not juego_terminado and camino_solucion:
            tiempo_actual_animacion = time.time() # Obtiene el tiempo actual para el control del ritmo de animación.
            
            # Controla el ritmo de la animación según 'tiempo_entre_pasos'
            if tiempo_actual_animacion - ultimo_tiempo_paso >= tiempo_entre_pasos:
                ultimo_tiempo_paso = tiempo_actual_animacion # Actualiza el tiempo del último paso
                indice_paso_actual += 1 # Avanza al siguiente paso de la solución

                # Si aún hay pasos en el camino de la solución
                if indice_paso_actual < len(camino_solucion):
                    # Actualiza el tablero a la siguiente configuración del camino de solución
                    # Se convierte a lista de listas para que sea modificable, aunque en este punto de la animación no se modifica el tablero directamente por un click.
                    tablero_actual = [list(fila) for fila in camino_solucion[indice_paso_actual]]
                    movimientos_jugador = indice_paso_actual # El contador de movimientos refleja el paso de la animación
                    
                else:
                    # La animación ha terminado, lo que significa que el puzzle ha sido resuelto por el agente.
                    if not juego_terminado: # Evita recalcular si ya se marcó como terminado por alguna razón
                        juego_terminado = True # Marca el juego como terminado
                        ganador = True # El agente ha ganado
                        resolviendo_agente = False # El agente ya no está activo
                        tiempo_final_juego = time.time() - inicio_tiempo # Guarda el tiempo total de la animación
                         # Imprime un mensaje final sobre la solución del agente en consola
                        print(f"Animación de solución de agente '{agente_actual_tipo}' completada. Puzzle resuelto en {len(camino_solucion) - 1} movimientos y {tiempo_final_juego:.2f} segundos de animación.")

    # Lógica de dibujo: renderiza la pantalla según el estado actual del juego
    if current_game_state == STATE_MENU:
        dibujar_menu() # Dibuja la pantalla del menú
    elif current_game_state == STATE_GAME:
        # Dibuja el tablero del puzzle y la información del juego
        dibujar_tablero(tablero_actual, tiempo_transcurrido, movimientos_jugador, resolviendo_agente, nodos_expandidos_mostrar, tiempo_calculo_mostrar)
        
        # Si el juego ha terminado y se ha ganado, dibuja la pantalla de victoria
        if juego_terminado and ganador:
            dibujar_victoria(ANCHO_JUEGO, ALTO)

    pygame.display.flip() # Actualiza toda la pantalla para mostrar los cambios

pygame.quit() # Cierra Pygame cuando el bucle principal termina