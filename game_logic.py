import random #Para mezclar aleatoriamente el tablero
from config import FILAS, COLUMNAS, ESTADO_OBJETIVO_TUPLA, ESTADO_INICIAL_BASICO_LISTA # Importa las dimensiones y el estado objetivo e inicial básico del tablero

def obtener_posicion_vacia(tablero_list):
    """
    Encuentra la posición (fila, columna) del espacio vacío (pieza con valor 0).
    """
    for r in range(FILAS):
        for c in range(COLUMNAS):
            if tablero_list[r][c] == 0: # Comprueba si el valor de la celda actual es 0 (el espacio vacío).
                return r, c # Si encuentra el 0, retorna su posición (fila, columna).
    return -1, -1  # Si el bucle termina y no se encontró el 0, retorna (-1, -1). Esto no debería ocurrir en un tablero bien formado

def contar_inversiones(tablero_plano):
    """
    Cuenta el número de inversiones en una representación plana del tablero (excluyendo el 0).
    """
    inversiones = 0
    for i in range(len(tablero_plano)):
        for j in range(i + 1, len(tablero_plano)):
            # Comprueba si ambos números no son el espacio vacío (0) y si el número en la posición 'i' es mayor que el número en la posición 'j'.
            # Si ambas condiciones son verdaderas, se ha encontrado una inversión.
            if tablero_plano[i] != 0 and tablero_plano[j] != 0 and tablero_plano[i] > tablero_plano[j]:
                inversiones += 1
    return inversiones # Devuelve el numero de inversiones del tablero

def mezclar_tablero():
    """
    Mezcla un tablero hasta que se obtiene una configuración que sea resoluble
    respecto a la paridad de la meta deseada (ESTADO_OBJETIVO_TUPLA) y que no sea igual al estado objetivo.
    """
    # Convierte el estado inicial básico (lista de listas) a una lista plana (1D) para facilitar la mezcla.
    # Esta lista 'plano' contendrá todos los números del 0 al 8.
    plano = []
    for fila in ESTADO_INICIAL_BASICO_LISTA:
        for num in fila:
            plano.append(num)
            
    # Se crea una versión plana del estado objetivo para calcular la paridad de inversiones del estado objetivo
    meta_plana = []
    for fila_meta in ESTADO_OBJETIVO_TUPLA:
        for num_meta in fila_meta:
            if num_meta != 0: # Excluir el 0 para el cálculo de inversiones
                meta_plana.append(num_meta)
    
    paridad_meta = contar_inversiones(meta_plana) % 2 # 0 si es par, 1 si es impar

    nuevo_tablero = [] # Variable para almacenar el tablero 2D final y válido.

    while True:
        random.shuffle(plano) # Mezcla aleatoriamente la lista 1D
        
        # Verificar la paridad de inversiones del tablero mezclado actual
        paridad_mezclado = contar_inversiones(plano) % 2
        
        # Si la paridad del tablero mezclado coincide con la paridad de la meta, es resoluble.
        if paridad_mezclado == paridad_meta:
            # Reconstruir el tablero 2D a partir del plano para retornarlo
            temp_2d_tablero = []
            for i in range(FILAS):
                fila_temp = []
                for j in range(COLUMNAS):
                    fila_temp.append(plano[i * COLUMNAS + j]) 
                temp_2d_tablero.append(fila_temp)
            # Si el tablero mezclado es resoluble Y no es idéntico al estado objetivo:
            if temp_2d_tablero != list(list(fila) for fila in ESTADO_OBJETIVO_TUPLA):
                nuevo_tablero = temp_2d_tablero # Asigna el tablero 2D válido a la variable de retorno.
                break # Sale del bucle al encontrar un tablero adecuado
            
    return nuevo_tablero # Retorna el tablero 2D válido.

def es_movimiento_valido(vacia_fila, vacia_columna, nueva_fila, nueva_columna):
    """
    Verifica si un movimiento de una pieza a la posición del espacio vacío es válido.
    Un movimiento es válido si la pieza a mover es adyacente (arriba, abajo, izquierda, derecha)
    al espacio vacío, no en diagonal.
    """
    # Comprueba si la pieza está en la misma columna y una fila adyacente (arriba/abajo)
    # O si está en la misma fila y una columna adyacente (izquierda/derecha)
    if (abs(nueva_fila - vacia_fila) == 1 and nueva_columna == vacia_columna) or \
       (abs(nueva_columna - vacia_columna) == 1 and nueva_fila == vacia_fila):
        return True
    return False

def mover_pieza_en_tablero(tablero_list, clic_fila, clic_columna):
    """
    Mueve una pieza si el movimiento es válido. Esta función es utilizada
    cuando el jugador interactúa manualmente con el tablero.
    Retorna True si el movimiento fue exitoso, False en caso contrario.
    """
    vacia_fila, vacia_columna = obtener_posicion_vacia(tablero_list) # Obtiene la posición del espacio vacío
    
    # Verifica si la pieza clickeada se puede mover al espacio vacío
    if es_movimiento_valido(vacia_fila, vacia_columna, clic_fila, clic_columna):
        # Realiza el intercambio de los valores de las piezas en el tablero
        temp = tablero_list[clic_fila][clic_columna] # Guarda temporalmente el valor de la pieza que fue clickeada
        tablero_list[vacia_fila][vacia_columna] = temp # Mueve el valor de la pieza clicada a la posición del espacio vacío
        tablero_list[clic_fila][clic_columna] = 0 # Coloca el 0 (espacio vacío) en la posición original de la pieza que se movió
        return True # El movimiento fue válido y se realizó
    return False # El movimiento no fue válido

def verificar_victoria(tablero_list):
    """
    Comprueba si el estado actual del tablero (lista de listas) es idéntico
    al estado objetivo (tupla de tuplas).
    Retorna True si el puzzle está resuelto, False en caso contrario.
    """
    # Convierte la lista de listas del tablero actual a una tupla de tuplas.
    tablero_como_tupla = tuple(tuple(fila) for fila in tablero_list)
    return tablero_como_tupla == ESTADO_OBJETIVO_TUPLA # Compara el tablero actual con el objetivo.