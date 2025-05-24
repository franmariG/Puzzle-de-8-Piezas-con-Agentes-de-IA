import time # Importa el módulo time para funciones relacionadas con el tiempo (temporizadores)
import heapq # Módulo para colas de prioridad (utilizado en A* para recuperar el nodo de menor costo f)
from collections import deque # Módulo para colas de doble extremo (utilizado en BFS)
from game_logic import obtener_posicion_vacia, FILAS, COLUMNAS # Importa lógica del juego necesaria
from config import ESTADO_OBJETIVO_TUPLA # Importa el estado objetivo para A* y BFS

def reconstruir_camino(nodo_final):
    """
    Reconstruye el camino desde el nodo final de la búsqueda hasta el nodo inicial,
    siguiendo los padres de cada nodo.
    """
    camino = [] # Inicializa una lista vacía para almacenar el camino invertido (donde parent es None).
    actual = nodo_final # Comienza desde el nodo final.
    while actual is not None: # Itera hacia atrás desde el nodo final hasta que se alcanza el nodo inicial
        camino.append(actual.tablero) # Añade el estado del tablero del nodo actual al camino
        actual = actual.parent # Sube al nodo padre para continuar reconstruyendo hacia atrás.
    
    # Invertir el camino para que vaya del inicio al final
    camino_invertido = []
    for i in range(len(camino) - 1, -1, -1): # Recorre la lista 'camino' desde el último elemento hasta el primero.
        camino_invertido.append(camino[i]) # Añade cada elemento a la nueva lista.
    return camino_invertido # Retorna el camino en el orden correcto.

def obtener_sucesores(nodo_actual, es_astar=False):
    """
    Genera todos los posibles estados del tablero (sucesores) a partir de un nodo dado,
    realizando un movimiento válido de la pieza vacía.
    """
    sucesores = [] # Lista para almacenar los nodos sucesores generados.
    
    # Convertir la tupla de tuplas del tablero actual a una lista de listas para poder modificarla
    tablero_list = [list(fila_tupla) for fila_tupla in nodo_actual.tablero]
        
    vacia_fila, vacia_columna = obtener_posicion_vacia(tablero_list) # Encuentra la posición del espacio vacío

    # Definir los posibles movimientos en el tablero 
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)] # (-1, 0): Arriba; (1, 0): Abajo; (0, -1): Izquierda; (0, 1): Derecha.

    # Itera sobre cada posible cambio de fila (dr) y columna (dc).
    for dr, dc in movimientos:
        # Calcula la nueva posición potencial para el espacio vacío después de un movimiento.
        nueva_vacia_fila = vacia_fila + dr
        nueva_vacia_columna = vacia_columna + dc

        # Verificar si el nuevo movimiento está dentro de los límites del tablero 
        if 0 <= nueva_vacia_fila < FILAS and 0 <= nueva_vacia_columna < COLUMNAS: # Las filas deben estar entre 0 y FILAS-1, y las columnas entre 0 y COLUMNAS-1.
            # Crear una copia profunda del tablero actual para no modificar el original del nodo_actual
            nuevo_tablero_list = [list(fila_original) for fila_original in tablero_list]
            
            # Realizar el intercambio de la pieza vacía con la pieza adyacente
            temp_val = nuevo_tablero_list[nueva_vacia_fila][nueva_vacia_columna]  # Guarda temporalmente el valor de la pieza que se va a mover a la posición del espacio vacío.
            nuevo_tablero_list[nueva_vacia_fila][nueva_vacia_columna] = nuevo_tablero_list[vacia_fila][vacia_columna] # Mueve el valor del espacio vacío (que es 0) a la nueva posición calculada.
            nuevo_tablero_list[vacia_fila][vacia_columna] = temp_val # Coloca el valor de la pieza temporal (la que se movió) en la posición original del espacio vacío.
            
            # Convertir el nuevo tablero (lista de listas) a tupla de tuplas.
            # Esto asegura que el estado del tablero sea inmutable,
            # para su uso en conjuntos (sets) o como claves de diccionario en los algoritmos de búsqueda.
            nuevo_tablero_tupla = tuple(tuple(fila_list) for fila_list in nuevo_tablero_list)
            
            # Crear el nodo sucesor correspondiente, dependiendo si es para A* o BFS
            # El costo 'g_cost' del sucesor es el costo del nodo actual más 1 (por un movimiento).
            # El 'parent' del sucesor es el nodo actual, para la reconstrucción del camino.
            if es_astar:
                sucesor_nodo = NodoAStar(nuevo_tablero_tupla, nodo_actual.g_cost + 1, nodo_actual)
            else: # Es BFS
                sucesor_nodo = NodoBFS(nuevo_tablero_tupla, nodo_actual)
            sucesores.append(sucesor_nodo) # Añade el nodo sucesor a la lista de sucesores
            
    return sucesores

# ---> Agente A* (Búsqueda Informada)
class NodoAStar:
    """
    Representa un nodo en el árbol de búsqueda A* para el puzzle de 8.
    Contiene el estado del tablero, el costo del camino (g_cost),
    el costo heurístico (h_cost) y el costo total (f_cost = g_cost + h_cost).
    """
    def __init__(self, tablero, g_cost, parent=None):
        self.tablero = tablero # Estado actual del tablero (tupla de tuplas)
        self.g_cost = g_cost # Costo del camino desde el inicio hasta este nodo
        self.h_cost = self.calcular_manhattan_distancia() # Costo heurístico estimado desde este nodo hasta la meta. Se calcula usando la distancia de Manhattan.
        self.f_cost = self.g_cost + self.h_cost # Costo total estimado (f = g + h), usado para la prioridad en A*.
        self.parent = parent # Nodo padre para reconstruir el camino

    def calcular_manhattan_distancia(self):
        """
        Calcula la distancia de Manhattan para este estado del tablero.
        La distancia de Manhattan es la suma de las distancias horizontales y verticales
        que cada pieza está de su posición objetivo.
        """
        distancia = 0
        # Mapa de posiciones objetivo para una búsqueda rápida de la ubicación final de cada pieza
        posiciones_objetivo = {}
        # Recorre el ESTADO_OBJETIVO_TUPLA para construir el mapa de posiciones objetivo
        for r_obj in range(FILAS):
            for c_obj in range(COLUMNAS):
                valor_obj = ESTADO_OBJETIVO_TUPLA[r_obj][c_obj]
                posiciones_objetivo[valor_obj] = (r_obj, c_obj)

        # Itera sobre cada celda del tablero actual del nodo.
        for r in range(FILAS):
            for c in range(COLUMNAS):
                valor = self.tablero[r][c] # Obtiene el valor de la pieza en la celda actual.
                if valor != 0: # Ignora el espacio vacío en el cálculo de la heurística
                    objetivo_r, objetivo_c = posiciones_objetivo[valor] # Obtener la posición objetivo de la pieza
                    distancia += abs(r - objetivo_r) + abs(c - objetivo_c) # Sumar la distancia de Manhattan |fila_actual - fila_objetivo| + |columna_actual - columna_objetivo|.
        return distancia # Retorna la distancia total de Manhattan.

    def __lt__(self, other):
        """
        Define el comportamiento de comparación "menor que" (<) para los nodos A*.
        Esto es crucial para que heapq (la cola de prioridad) pueda ordenar los nodos
        correctamente basándose en su 'f_cost'.
        """
        return self.f_cost < other.f_cost

def resolver_puzzle_a_estrella(tablero_inicial_list):
    """
    Resuelve el puzzle de 8 utilizando el algoritmo de búsqueda A*.
    Retorna el camino de la solución, el número de nodos expandidos y el tiempo de cálculo.
    """
    tiempo_inicio = time.perf_counter() # Inicia el contador de tiempo de cálculo

    # Convertir el tablero inicial (lista de listas) a una tupla de tuplas para inmutabilidad.
    tablero_inicial_tupla = tuple(tuple(fila_list) for fila_list in tablero_inicial_list)
    
    nodo_inicial = NodoAStar(tablero_inicial_tupla, 0) # Crear el nodo inicial con costo g=0
    
    cola = [] # Cola de prioridad (min-heap) para nodos por explorar. Los nodos se ordenan automáticamente por su 'f_cost' (costo total estimado).
    heapq.heappush(cola, nodo_inicial) # Añade el nodo inicial a cola_abierta
    
    # visitados almacena los tableros visitados y el costo g más bajo para llegar a ellos.  Esto evita ciclos y permite encontrar caminos más cortos a estados ya visitados.
    visitados = {nodo_inicial.tablero: nodo_inicial.g_cost} 
    
    nodos_expandidos_cont = 0 # Contador de nodos expandidos para métricas
    
    # El bucle principal del algoritmo A*. Continúa mientras haya nodos en cola_abierta para explorar.
    while cola:
        nodo_actual = heapq.heappop(cola) # Sacar el nodo con el f_cost (costo total estimado) más bajo
        nodos_expandidos_cont += 1 # Incrementa el contador de nodos expandidos
        
        # Si el tablero actual es el estado objetivo, se ha encontrado la solución
        if nodo_actual.tablero == ESTADO_OBJETIVO_TUPLA:
            tiempo_fin = time.perf_counter() # Finaliza el contador de tiempo
            tiempo_calculo = tiempo_fin - tiempo_inicio # Calcula el tiempo transcurrido.
            # Reconstruye y retorna el camino, el conteo de nodos y el tiempo
            return reconstruir_camino(nodo_actual), nodos_expandidos_cont, tiempo_calculo
            
        # Genera todos los posibles estados sucesores (vecinos) del nodo actual.'es_astar=True' indica que los sucesores deben ser de tipo NodoAStar.
        for sucesor in obtener_sucesores(nodo_actual, es_astar=True):
            # Si el sucesor no ha sido visitado o si se encontró un camino más corto para llegar a él
            if sucesor.tablero not in visitados or sucesor.g_cost < visitados[sucesor.tablero]:
                visitados[sucesor.tablero] = sucesor.g_cost # Actualiza o añade el costo g más bajo para este estado en visitados.
                heapq.heappush(cola, sucesor) # Añade el nodo sucesor a cola_abierta para su futura exploración
                
    # Si la cola se vacía y no se encuentra el objetivo, significa que no hay solución
    tiempo_fin = time.perf_counter()
    tiempo_calculo = tiempo_fin - tiempo_inicio
    return None, nodos_expandidos_cont, tiempo_calculo # Retorna None para el camino si no se encontró solución. No debería pasar porque la función mezclar_tablero() garantiza tableros resolubles

# ---> Agente BFS (Búsqueda Primero en Anchura - No Informada)
class NodoBFS:
    """
    Representa un nodo en el árbol de búsqueda BFS para el puzzle de 8.
    Contiene el estado del tablero y una referencia a su nodo padre para reconstruir el camino.
    """
    def __init__(self, tablero, parent=None):
        self.tablero = tablero # Estado actual del tablero (tupla de tuplas)
        self.parent = parent # Nodo padre para reconstruir el camino

def resolver_puzzle_bfs(tablero_inicial_list):
    """
    Resuelve el puzzle de 8 utilizando el algoritmo de búsqueda BFS.
    Retorna el camino de la solución, el número de nodos expandidos y el tiempo de cálculo.
    """
    tiempo_inicio = time.perf_counter() # Inicia el contador de tiempo de cálculo

    # Convierte el tablero inicial (lista de listas) a una tupla de tuplas para inmutabilidad.
    tablero_inicial_tupla = tuple(tuple(fila_list) for fila_list in tablero_inicial_list)
    
    nodo_inicial = NodoBFS(tablero_inicial_tupla) # Crear el nodo inicial
    
    cola = deque() # Cola de doble extremo (deque) para BFS (FIFO) que almacena los nodos pendientes de explorar.
    cola.append(nodo_inicial) # Añade el nodo inicial a la cola
    
    visitados = {nodo_inicial.tablero} # Conjunto de tableros visitados para evitar ciclos y repeticiones
    
    nodos_expandidos_cont = 0 # Contador de nodos expandidos para métricas
    
    # El bucle principal del algoritmo BFS. Continúa mientras haya nodos en la cola para explorar.
    while cola:
        nodo_actual = cola.popleft() # Sacar el nodo más antiguo de la cola (FIFO)
        nodos_expandidos_cont += 1 # Incrementa el contador de nodos expandidos
        
        # Si el tablero actual es el estado objetivo, se ha encontrado la solución
        if nodo_actual.tablero == ESTADO_OBJETIVO_TUPLA:
            tiempo_fin = time.perf_counter() # Finaliza el contador de tiempo
            tiempo_calculo = tiempo_fin - tiempo_inicio
            # Reconstruye y retorna el camino, el conteo de nodos y el tiempo
            return reconstruir_camino(nodo_actual), nodos_expandidos_cont, tiempo_calculo
            
        # Genera todos los posibles estados sucesores (vecinos) del nodo actual. 'es_astar=False' indica que los sucesores deben ser de tipo NodoBFS.
        for sucesor in obtener_sucesores(nodo_actual, es_astar=False):
            if sucesor.tablero not in visitados: # Si el sucesor no ha sido visitado aún
                visitados.add(sucesor.tablero) # Añade el tablero del sucesor al conjunto de estados visitados
                cola.append(sucesor) # Añade el nodo sucesor a la cola para su futura exploración
                
    # Si la cola se vacía y no se encuentra el objetivo, significa que no hay solución
    tiempo_fin = time.perf_counter()
    tiempo_calculo = tiempo_fin - tiempo_inicio
    return None, nodos_expandidos_cont, tiempo_calculo # Retorna None si no se encontró solución. No debería pasar porque la función mezclar_tablero() garantiza tableros resolubles