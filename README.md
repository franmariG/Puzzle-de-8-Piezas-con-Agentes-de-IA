# Puzzle 8 con Agentes de Búsqueda (IA)

Este proyecto implementa el clásico "Puzzle de 8 Piezas", un rompecabezas deslizante, utilizando la librería Pygame para la interfaz gráfica. Lo más destacado son los dos agentes de inteligencia artificial capaces de resolver el puzzle de forma autónoma, aplicando algoritmos de búsqueda: uno de búsqueda no informada (BFS) y otro de búsqueda informada (A* con heurística de distancia Manhattan).

El proyecto fue desarrollado como parte de un mini-proyecto de Inteligencia Artificial en la Universidad Nacional Experimental de Guayana (UNEG).

https://github.com/user-attachments/assets/6a4ad166-0081-4215-a897-326c6fe7249c
## Características

* **Interfaz Gráfica Interactiva:** Juega el Puzzle 8 de forma manual arrastrando las piezas.
* **Agente de Búsqueda No Informada (BFS):** Encuentra la solución óptima (el camino más corto) para el puzzle.
* **Agente de Búsqueda Informada (A\*):** Utiliza la heurística de distancia Manhattan para encontrar la solución de manera más eficiente.
* **Visualización de la Solución:** Observa a los agentes resolver el puzzle paso a paso.
* **Métricas de Rendimiento:** Compara el rendimiento de ambos agentes en términos de:
    * Nodos expandidos
    * Longitud de la solución
    * Tiempo de cálculo
* **Validación de Solubilidad:** Asegura que los puzzles generados aleatoriamente siempre tengan solución.
* **Pantalla de Inicio:** Una pantalla de bienvenida simple antes de comenzar el juego.
* **Modularización del Código:** El código está organizado en módulos (`main.py`, `config.py`, `game_logic.py`, `agents.py`, `ui.py`) para facilitar su mantenimiento y comprensión.

## Requisitos

Antes de ejecutar el proyecto, asegúrate de tener instalado Python (preferiblemente Python 3.x) y Pygame.

Para instalar Pygame, puedes usar pip:

```bash
pip install pygame
```

## Estructura del Proyecto
El proyecto está organizado en los siguientes archivos:

```bash
├── main.py             # Lógica principal del juego y manejo de estados.
├── config.py           # Definiciones de constantes, inicialización de Pygame y recursos.
├── game_logic.py       # Funciones relacionadas con la lógica del tablero (mezclar, mover, verificar victoria).
├── agents.py           # Implementación de los algoritmos de búsqueda (BFS y A*).
└── ui.py               # Funciones para dibujar la interfaz gráfica (tablero, menú, información).
```

## Uso
Clona el repositorio:

```bash
git clone https://github.com/franmariG/Puzzle-de-8-Piezas-con-Agentes-de-IA.git
```

Navega hasta el directorio del proyecto en tu terminal y ejecuta main.py:
```bash
cd nombre-del-repositorio
python main.py
```

Interfaz del Juego:
* **Pantalla de Inicio**: Al iniciar, verás una pantalla de título con un botón "Iniciar". Haz clic en él para empezar el juego.
* **Modo de Juego Manual**: Puedes mover las baldosas haciendo clic en una baldosa adyacente al espacio vacío.
* **Resolver con Agentes**:
  * Haz clic en "Resolver (A*)" para que el agente A* encuentre y muestre la solución.
  * Haz clic en "Resolver (BFS)" para que el agente BFS encuentre y muestre la solución.
* **Reiniciar Puzzle**: El botón "Reiniciar" generará un nuevo puzzle aleatorio y reseteará los contadores.

## Algoritmos Implementados
* **Búsqueda en Amplitud (BFS - Breadth-First Search)**: Un algoritmo de búsqueda no informada que explora todos los nodos de un nivel antes de pasar al siguiente. Garantiza encontrar la solución más corta si existe.
* **Búsqueda A*** **(A-Star Search)**: Un algoritmo de búsqueda informada que utiliza una función heurística (en este caso, la Distancia Manhattan) para estimar el costo desde el nodo actual hasta el objetivo. Es más eficiente que BFS para encontrar soluciones óptimas en puzzles complejos.

**Heurística de Distancia Manhattan**:
La distancia Manhattan para el Puzzle 8 se calcula como la suma de las distancias horizontales y verticales que cada baldosa (excepto el espacio vacío) necesita moverse desde su posición actual hasta su posición objetivo en el estado resuelto.

## Comparación de Agentes
El panel de información mostrará los "Movimientos", "Nodos Expandidos" y el "Tiempo de Cálculo" para cada agente después de encontrar una solución. Esto permitirá comparar su eficiencia en diferentes escenarios. En general, se espera que A* expanda menos nodos y encuentre la solución más rápido que BFS, especialmente en puzzles con un camino más largo.
