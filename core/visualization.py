"""
Módulo de visualización para reversal con signo
Crea diagramas gráficos de secuencias expandidas con L/R y conexiones
"""

from typing import List, Tuple, Dict
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


def create_expanded_sequence_diagram(sequence: List[str], ax=None, title: str = "Secuencia Expandida", step: int = 0, reversal_range: Tuple[int, int] = None):
    """
    Crea un diagrama visual de una secuencia expandida con L/R.
    
    Muestra los elementos en una línea horizontal y dibuja aristas
    conectando las tuplas relacionadas según el algoritmo de breakpoints.
    
    Args:
        sequence: Secuencia expandida (ej: ['L', '-1', '+1', '+3', '-3', '-2', '+2', 'R'])
        ax: Eje de matplotlib (si None, se crea uno nuevo)
        title: Título del diagrama
        step: Paso de visualización (0 = solo nodos, 1 = nodos + arcos rectos)
        reversal_range: Tupla (i, j) indicando el rango de reversión en la secuencia original (None si no hay reversión)
        
    Returns:
        Figura y eje de matplotlib
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(14, 6))
    else:
        fig = ax.figure
    
    n = len(sequence)
    
    # Posiciones horizontales para cada elemento (espaciadas uniformemente)
    x_positions = np.linspace(1, 9, n)
    y_base = 0.5
    
    # Todos los nodos con el mismo color (gris claro)
    node_color = '#E0E0E0'  # Gris claro
    edge_color = 'black'    # Borde negro
    
    # Dibujar puntos/nodos
    for i, (elem, x) in enumerate(zip(sequence, x_positions)):
        # Dibujar círculo más grande
        circle = plt.Circle((x, y_base), 0.2, facecolor=node_color, 
                           edgecolor=edge_color, linewidth=2, zorder=3)
        ax.add_patch(circle)
        
        # Etiqueta del elemento (texto negro)
        ax.text(x, y_base, elem, ha='center', va='center', 
                fontsize=11, fontweight='bold', color='black',
                zorder=4)
    
    # Paso 0: Solo nodos, sin arcos
    # Paso 1: Nodos + arcos rectos (líneas negras) entre pares de nodos
    # Paso 2: Nodos + arcos con flechas formando ciclos
    
    if step >= 1:
        # Dibujar arcos rectos (líneas negras) entre pares de nodos
        # Conectar nodos en pares: 0-1, 2-3, 4-5, etc.
        for i in range(0, n - 1, 2):  # Avanzar de 2 en 2
            x1, x2 = x_positions[i], x_positions[i + 1]
            # Línea recta negra entre el par de nodos
            ax.plot([x1, x2], [y_base, y_base], 'k-', linewidth=2.5, 
                   zorder=2)
    
    if step >= 2:
        # Paso 2: Dibujar ciclos con arcos y flechas
        _draw_cycle_arcs(ax, sequence, x_positions, y_base)
    
    # Dibujar líneas verticales para mostrar el rango de reversión solo en paso 2 o superior
    if reversal_range is not None and step >= 2:
        i, j = reversal_range
        # Mapear el rango de la secuencia original a la secuencia expandida
        # La secuencia expandida tiene: L (0), (-n, +n) (1,2), (-m, +m) (3,4), ..., R
        # La primera línea vertical debe estar ANTES del primer nodo del rango (elemento i)
        # La segunda línea vertical debe estar DESPUÉS del último nodo del rango (elemento j)
        if i is not None and j is not None:
            # Calcular número de elementos originales (sin contar L y R)
            num_original_elements = (n - 2) // 2  # (n - 2) porque L y R, luego dividir por 2
            
            # Línea vertical izquierda: unión ANTES del elemento i
            if i > 0:
                # Unión del elemento anterior (i-1)
                # El elemento i-1 está en las posiciones 1+(i-1)*2 y 2+(i-1)*2
                expanded_start_left = 2 + (i - 1) * 2
                expanded_start_right = 3 + (i - 1) * 2
                x_start = (x_positions[expanded_start_left] + x_positions[expanded_start_right]) / 2
            else:
                # Si i == 0, la unión anterior está entre L (0) y el primer nodo (1)
                x_start = (x_positions[0] + x_positions[1]) / 2
            
            # Línea vertical derecha: unión DESPUÉS del elemento j
            if j < num_original_elements - 1:
                # Unión del elemento siguiente (j+1)
                # El elemento j+1 está en las posiciones 1+(j+1)*2 y 2+(j+1)*2
                expanded_end_left = 0 + (j + 1) * 2
                expanded_end_right = 1 + (j + 1) * 2
                x_end = (x_positions[expanded_end_left] + x_positions[expanded_end_right]) / 2
            else:
                # Si j es el último elemento, la unión siguiente está entre el último nodo del último par y R
                # El último par está en las posiciones n-3 y n-2, R está en n-1
                # La unión después está en el centro entre n-2 y n-1
                if n >= 3:
                    x_end = (x_positions[n - 2] + x_positions[n - 1]) / 2
                else:
                    x_end = x_positions[n - 1]  # Si solo hay L y R
            
            # Dibujar líneas verticales en los extremos del rango
            # Línea vertical izquierda (antes del primer nodo del rango)
            ax.plot([x_start, x_start], [y_base - 0.35, y_base + 0.35], 
                   'r-', linewidth=3, zorder=5, alpha=0.7)
            # Línea vertical derecha (después del último nodo del rango)
            ax.plot([x_end, x_end], [y_base - 0.35, y_base + 0.35], 
                   'r-', linewidth=3, zorder=5, alpha=0.7)
            
            # Opcional: dibujar una línea horizontal conectando las dos verticales
            ax.plot([x_start, x_end], [y_base - 0.35, y_base - 0.35], 
                   'r--', linewidth=2, zorder=5, alpha=0.5)
            ax.plot([x_start, x_end], [y_base + 0.35, y_base + 0.35], 
                   'r--', linewidth=2, zorder=5, alpha=0.5)
    
    # Configurar el eje
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Solo mostrar título si no está vacío
    if title:
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    
    return fig, ax


def _draw_cycle_arcs(ax, sequence: List[str], x_positions: np.ndarray, y_base: float):
    """
    Dibuja los arcos de ciclos siguiendo las uniones del paso 1.
    
    Reglas:
    - Si el número es positivo (+n): busca el nodo con número incrementado en negativo (-(n+1))
      Si no existe, se conecta con R
    - Si el número es negativo (-n): busca el nodo con número decrementado en positivo (+(n-1))
      Si no existe, se conecta con L
    
    IMPORTANTE: Después de aplicar la regla, si el nodo destino está en una unión (par del paso 1),
    se sigue por la unión al otro nodo del par antes de continuar.
    
    Args:
        ax: Eje de matplotlib
        sequence: Secuencia expandida
        x_positions: Posiciones x de los nodos
        y_base: Posición y base
    """
    n = len(sequence)
    l_idx = sequence.index('L')
    r_idx = sequence.index('R')
    
    # Crear diccionario para encontrar índices rápidamente
    elem_to_idx = {}
    for i, elem in enumerate(sequence):
        if elem not in elem_to_idx:
            elem_to_idx[elem] = i
    
    # Identificar las uniones del paso 1 (pares de nodos: 0-1, 2-3, 4-5, etc.)
    unions = {}  # {node_idx: paired_node_idx}
    for i in range(0, n - 1, 2):
        unions[i] = i + 1
        unions[i + 1] = i
    
    # Función para obtener el nodo objetivo según las reglas
    def get_target_node(node_idx):
        elem = sequence[node_idx]
        
        # REGLA ESPECIAL PARA R: Se conecta al negativo del mayor valor absoluto
        if elem == 'R':
            # Encontrar el mayor valor absoluto en la secuencia
            max_value = 0
            max_negative_idx = None
            for i, e in enumerate(sequence):
                if e.startswith('-'):
                    value = int(e[1:])
                    if value > max_value:
                        max_value = value
                        max_negative_idx = i
            # Si encontramos un negativo, retornar su índice
            # Luego seguiremos por la unión al positivo correspondiente
            return max_negative_idx if max_negative_idx is not None else None
        
        # REGLA ESPECIAL PARA L: Se conecta al primer elemento negativo (ya implementado al final)
        # Pero también puede conectarse al negativo del menor valor si es necesario
        if elem == 'L':
            # L siempre se conecta al primer elemento negativo (l_idx + 1)
            if l_idx + 1 < n:
                first_negative_elem = sequence[l_idx + 1]
                if first_negative_elem.startswith('-'):
                    return l_idx + 1
            return None
        
        if elem.startswith('+'):
            value = int(elem[1:])
            target_value = value + 1
            target_elem = f'-{target_value}'
            if target_elem in elem_to_idx:
                return elem_to_idx[target_elem]
            else:
                return r_idx
        elif elem.startswith('-'):
            value = int(elem[1:])
            target_value = value - 1
            if target_value > 0:
                target_elem = f'+{target_value}'
                if target_elem in elem_to_idx:
                    return elem_to_idx[target_elem]
            return l_idx
        return None
    
    # Construir ciclos siguiendo las uniones
    nodes_in_cycles = set()  # Nodos que ya están en un ciclo (GLOBAL para toda la renderización)
    drawn_arcs = set()  # Para evitar dibujar el mismo arco dos veces
    
    for start_idx in range(n):
        # Saltar L y R como puntos de inicio
        if start_idx == l_idx or start_idx == r_idx:
            continue
        
        # Si este nodo ya está en un ciclo (verificación GLOBAL), saltarlo
        if start_idx in nodes_in_cycles:
            continue
        
        # Construir el ciclo desde este nodo
        current_idx = start_idx
        cycle_nodes = set()  # Nodos en este ciclo específico
        cycle_nodes.add(start_idx)  # Agregar el nodo inicial
        
        while True:
            # Aplicar la regla para obtener el nodo objetivo desde current_idx
            target_idx = get_target_node(current_idx)
            
            if target_idx is None:
                # No hay objetivo válido, terminar el ciclo
                nodes_in_cycles.update(cycle_nodes)
                break
            
            # Verificar si target_idx ya está en este ciclo (ciclo cerrado)
            # Si está, dibujar el arco que cierra el ciclo y terminar
            if target_idx in cycle_nodes:
                # Dibujar el arco que cierra el ciclo (si no se ha dibujado)
                arc_key = (current_idx, target_idx)
                if arc_key not in drawn_arcs:
                    drawn_arcs.add(arc_key)
                    x1, x2 = x_positions[current_idx], x_positions[target_idx]
                    distance = abs(x2 - x1)
                    height = 0.4 if distance > 2 else 0.3
                    # Todos los arcos van hacia arriba para consistencia visual
                    _draw_arrow_arc(ax, x1, x2, y_base, height, color='blue', linewidth=2)
                # El ciclo está cerrado, terminar
                nodes_in_cycles.update(cycle_nodes)
                break
            
            # Dibujar arco de current_idx a target_idx (si no se ha dibujado)
            arc_key = (current_idx, target_idx)
            if arc_key not in drawn_arcs:
                drawn_arcs.add(arc_key)
                x1, x2 = x_positions[current_idx], x_positions[target_idx]
                distance = abs(x2 - x1)
                height = 0.4 if distance > 2 else 0.3
                # Todos los arcos van hacia arriba para consistencia visual
                _draw_arrow_arc(ax, x1, x2, y_base, height, color='blue', linewidth=2)
            
            # Agregar target_idx al ciclo
            cycle_nodes.add(target_idx)
            
            # Determinar el siguiente nodo a procesar
            # Si target_idx está en una unión, seguimos por la unión al otro nodo del par
            next_idx = target_idx
            cycle_should_close = False
            
            if target_idx in unions:
                paired_idx = unions[target_idx]
                
                # Verificar si el nodo del par ya está en este ciclo (ciclo cerrado)
                if paired_idx in cycle_nodes:
                    # El ciclo se cierra aquí, ya dibujamos el arco, terminar
                    cycle_should_close = True
                # Verificar si el nodo del par es el inicio del ciclo (ciclo cerrado)
                elif paired_idx == start_idx:
                    # El ciclo se cierra volviendo al inicio, ya dibujamos el arco, terminar
                    cycle_should_close = True
                # Verificar si el nodo del par ya está en OTRO ciclo (verificación GLOBAL)
                # Si está en otro ciclo, no seguimos desde ahí, pero el arco ya se dibujó
                elif paired_idx in nodes_in_cycles:
                    # El nodo del par está en otro ciclo, terminar este ciclo
                    # Pero el arco ya se dibujó, así que está bien
                    cycle_should_close = True
                else:
                    # Agregar el nodo del par al ciclo y continuar desde ahí
                    cycle_nodes.add(paired_idx)
                    next_idx = paired_idx
                
                if cycle_should_close:
                    nodes_in_cycles.update(cycle_nodes)
                    break
            elif target_idx == l_idx or target_idx == r_idx:
                # Si target_idx es L o R, verificar si tienen un target según las reglas especiales
                # R se conecta al mayor valor negativo, L se conecta al primer elemento negativo
                special_target = get_target_node(target_idx)
                if special_target is not None:
                    # L o R tienen un target especial, dibujar el arco y continuar el ciclo
                    # Dibujar arco de L/R hacia el target especial
                    arc_key = (target_idx, special_target)
                    if arc_key not in drawn_arcs:
                        drawn_arcs.add(arc_key)
                        x1, x2 = x_positions[target_idx], x_positions[special_target]
                        distance = abs(x2 - x1)
                        height = 0.4 if distance > 2 else 0.3
                        _draw_arrow_arc(ax, x1, x2, y_base, height, color='blue', linewidth=2)
                    
                    # Agregar L o R y el target especial al ciclo
                    cycle_nodes.add(target_idx)
                    cycle_nodes.add(special_target)
                    
                    # Verificar si el target especial ya está en el ciclo (ciclo cerrado)
                    if special_target in cycle_nodes and special_target != target_idx:
                        # El ciclo se cierra aquí
                        nodes_in_cycles.update(cycle_nodes)
                        break
                    
                    # Si el target especial está en una unión, seguir por la unión
                    if special_target in unions:
                        paired_idx = unions[special_target]
                        if paired_idx in cycle_nodes:
                            nodes_in_cycles.update(cycle_nodes)
                            break
                        cycle_nodes.add(paired_idx)
                        current_idx = paired_idx
                    else:
                        current_idx = special_target
                    continue
                else:
                    # L o R no tienen target, el ciclo termina aquí
                    nodes_in_cycles.update(cycle_nodes)
                    break
            
            # Verificar si el siguiente nodo ya está en este ciclo (ciclo cerrado)
            # IMPORTANTE: Verificar después de agregar paired_idx al ciclo
            if next_idx in cycle_nodes and next_idx != target_idx:
                # El ciclo se cierra aquí, ya dibujamos el arco, terminar
                nodes_in_cycles.update(cycle_nodes)
                break
            
            # Verificar si podemos continuar desde next_idx
            # Si next_idx es L o R, verificar si tienen target especial
            if next_idx == l_idx or next_idx == r_idx:
                special_target = get_target_node(next_idx)
                if special_target is None:
                    # L o R no tienen target, el ciclo termina aquí
                    nodes_in_cycles.update(cycle_nodes)
                    break
                # Si tienen target, dibujar el arco y continuar
                arc_key = (next_idx, special_target)
                if arc_key not in drawn_arcs:
                    drawn_arcs.add(arc_key)
                    x1, x2 = x_positions[next_idx], x_positions[special_target]
                    distance = abs(x2 - x1)
                    height = 0.4 if distance > 2 else 0.3
                    _draw_arrow_arc(ax, x1, x2, y_base, height, color='blue', linewidth=2)
                
                # Agregar L/R y el target especial al ciclo
                cycle_nodes.add(next_idx)
                cycle_nodes.add(special_target)
                
                # Verificar si el target especial ya está en el ciclo
                if special_target in cycle_nodes and special_target != next_idx:
                    nodes_in_cycles.update(cycle_nodes)
                    break
                
                # Si el target especial está en una unión, seguir por la unión
                if special_target in unions:
                    paired_idx = unions[special_target]
                    if paired_idx in cycle_nodes:
                        nodes_in_cycles.update(cycle_nodes)
                        break
                    cycle_nodes.add(paired_idx)
                    current_idx = paired_idx
                else:
                    current_idx = special_target
                continue
            
            # Continuar desde el siguiente nodo
            current_idx = next_idx
    
    # PASADA FINAL: Asegurar que todos los nodos tengan sus arcos dibujados
    # Esto es necesario porque algunos arcos pueden no haberse dibujado si los nodos
    # estaban en diferentes ciclos que se cerraron prematuramente
    for node_idx in range(n):
        # Saltar L y R
        if node_idx == l_idx or node_idx == r_idx:
            continue
        
        # Obtener el target para este nodo
        target_idx = get_target_node(node_idx)
        if target_idx is None:
            continue
        
        # Verificar si el arco ya está dibujado
        arc_key = (node_idx, target_idx)
        if arc_key not in drawn_arcs:
            # Dibujar el arco faltante
            drawn_arcs.add(arc_key)
            x1, x2 = x_positions[node_idx], x_positions[target_idx]
            distance = abs(x2 - x1)
            height = 0.4 if distance > 2 else 0.3
            _draw_arrow_arc(ax, x1, x2, y_base, height, color='blue', linewidth=2)
            
            # Si el target está en una unión, también dibujar el arco desde el nodo pareado si es necesario
            if target_idx in unions:
                paired_idx = unions[target_idx]
                # El arco desde el nodo pareado se dibujará cuando procesemos ese nodo
                # o ya debería estar dibujado si ese nodo ya fue procesado


def _draw_arrow_arc(ax, x1, x2, y_base, height=0.3, color='blue', linewidth=2):
    """
    Dibuja un arco (sin flecha) entre dos puntos usando una curva cuadrática.
    
    Args:
        ax: Eje de matplotlib
        x1, x2: Posiciones x de inicio y fin
        y_base: Posición y base
        height: Altura del arco (positivo hacia arriba, negativo hacia abajo)
        color: Color del arco
        linewidth: Grosor de la línea
    """
    # Crear puntos para la curva cuadrática
    t = np.linspace(0, 1, 100)
    x_curve = x1 + (x2 - x1) * t
    y_curve = y_base + 4 * height * t * (1 - t)
    
    # Dibujar solo la curva, sin flecha
    ax.plot(x_curve, y_curve, color=color, linewidth=linewidth, zorder=2)


def _draw_arc(ax, x1, x2, y_base, height=0.3, color='blue', linewidth=2):
    """
    Dibuja un arco entre dos puntos.
    
    Args:
        ax: Eje de matplotlib
        x1, x2: Posiciones x de inicio y fin
        y_base: Posición y base
        height: Altura del arco (positivo hacia arriba, negativo hacia abajo)
        color: Color del arco
        linewidth: Grosor de la línea
    """
    # Crear puntos para el arco (curva cuadrática)
    x_mid = (x1 + x2) / 2
    y_arc = y_base + height
    
    # Crear puntos para la curva
    t = np.linspace(0, 1, 100)
    x_curve = x1 + (x2 - x1) * t
    y_curve = y_base + 4 * height * t * (1 - t)
    
    ax.plot(x_curve, y_curve, color=color, linewidth=linewidth, zorder=2)


def visualize_sequence_expansion(sequence: List[str]) -> Tuple:
    """
    Función principal para visualizar una secuencia expandida.
    
    Args:
        sequence: Secuencia original con signos (ej: ['+1', '-3', '+2'])
        
    Returns:
        Tupla (fig, ax) de matplotlib
    """
    from .reversal_directed import expand_sequence_with_lr
    
    expanded = expand_sequence_with_lr(sequence)
    return create_expanded_sequence_diagram(expanded)


if __name__ == "__main__":
    # Prueba del módulo
    test_sequence = ['+1', '-3', '+2']
    fig, ax = visualize_sequence_expansion(test_sequence)
    plt.tight_layout()
    plt.show()

