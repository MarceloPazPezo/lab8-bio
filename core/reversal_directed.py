"""
Función 3: Reversal Con Dirección
Implementa el algoritmo de sorting por reversiones considerando dirección (+/-).
"""

from typing import List, Tuple, Dict
from collections import deque
import time


class SignedElement:
    """Representa un elemento con dirección (+/-)"""
    
    def __init__(self, value, sign=1):
        """
        Args:
            value: Valor del elemento
            sign: +1 para positivo, -1 para negativo
        """
        if isinstance(value, str):
            if value.startswith('+'):
                self.value = int(value[1:]) if value[1:].lstrip('-').isdigit() else value[1:]
                self.sign = 1
            elif value.startswith('-'):
                self.value = int(value[1:]) if value[1:].isdigit() else value[1:]
                self.sign = -1
            else:
                self.value = int(value) if value.lstrip('-').isdigit() else value
                self.sign = 1
        else:
            self.value = value
            self.sign = sign
    
    def flip(self):
        """Invierte la dirección del elemento"""
        return SignedElement(self.value, -self.sign)
    
    def __eq__(self, other):
        if isinstance(other, SignedElement):
            return self.value == other.value and self.sign == other.sign
        return False
    
    def __hash__(self):
        return hash((self.value, self.sign))
    
    def __repr__(self):
        sign_str = '+' if self.sign > 0 else '-'
        return f"{sign_str}{self.value}"
    
    def __str__(self):
        return self.__repr__()


def parse_signed_sequence(sequence: List) -> List[SignedElement]:
    """
    Convierte una lista de strings o enteros en elementos con signo.
    
    Args:
        sequence: Lista de elementos (puede ser '+1', '-2', etc.)
        
    Returns:
        Lista de SignedElement
    """
    return [SignedElement(elem) for elem in sequence]


def expand_sequence_with_lr(sequence: List) -> List[str]:
    """
    Expande una secuencia con signos agregando L al inicio, R al final,
    y expandiendo cada elemento en su tupla de signos.
    
    Regla: Si el elemento es positivo (+n), se expande a (-n, +n)
           Si el elemento es negativo (-n), se expande a (+n, -n)
    
    Ejemplo:
        Entrada: ['+1', '-3', '+2']
        Salida: ['L', '-1', '+1', '+3', '-3', '-2', '+2', 'R']
    
    Args:
        sequence: Lista de elementos con signos (ej: ['+1', '-2', '+3'])
        
    Returns:
        Lista expandida con L, tuplas de signos, y R
    """
    expanded = ['L']
    
    for elem in sequence:
        # Parsear el elemento
        signed_elem = SignedElement(elem)
        value = signed_elem.value
        sign = signed_elem.sign
        
        # Si es positivo (+n), expandir a (-n, +n)
        # Si es negativo (-n), expandir a (+n, -n)
        if sign > 0:
            expanded.append(f'-{value}')
            expanded.append(f'+{value}')
        else:
            expanded.append(f'+{value}')
            expanded.append(f'-{value}')
    
    expanded.append('R')
    return expanded


def apply_reversal_directed(sequence: List[SignedElement], i: int, j: int) -> List[SignedElement]:
    """
    Aplica una reversión con cambio de dirección en el rango [i, j].
    
    Args:
        sequence: Secuencia de elementos con signo
        i: Índice inicial del rango
        j: Índice final del rango
        
    Returns:
        Nueva secuencia con la reversión aplicada y direcciones invertidas
    """
    result = sequence[:]
    # Revertir y cambiar signo de los elementos en el rango
    reversed_segment = [elem.flip() for elem in reversed(result[i:j+1])]
    result[i:j+1] = reversed_segment
    return result


def sequence_to_tuple(sequence: List[SignedElement]) -> Tuple:
    """Convierte una secuencia a tupla para usar como clave en set"""
    return tuple((elem.value, elem.sign) for elem in sequence)


def reversal_distance_directed_bfs(initial_seq: List[SignedElement], 
                                   target_seq: List[SignedElement]) -> Tuple[List[List[SignedElement]], int]:
    """
    Calcula la distancia de reversión con dirección usando BFS.
    
    Args:
        initial_seq: Secuencia inicial con signos
        target_seq: Secuencia objetivo con signos
        
    Returns:
        Tupla con (lista de pasos intermedios, número de pasos)
    """
    if len(initial_seq) > 10:
        raise ValueError("La secuencia no debe tener más de 10 elementos")
    
    if len(initial_seq) != len(target_seq):
        raise ValueError("Las secuencias deben tener el mismo tamaño")
    
    # Si ya son iguales
    if initial_seq == target_seq:
        return [initial_seq], 0
    
    # BFS
    queue = deque([(initial_seq, [initial_seq])])
    visited = {sequence_to_tuple(initial_seq)}
    
    while queue:
        current_seq, path = queue.popleft()
        
        # Probar todas las reversiones posibles
        n = len(current_seq)
        for i in range(n):
            for j in range(i, n):
                new_seq = apply_reversal_directed(current_seq, i, j)
                
                # Si encontramos la secuencia objetivo
                if new_seq == target_seq:
                    final_path = path + [new_seq]
                    return final_path, len(final_path) - 1
                
                # Si no hemos visitado este estado
                new_seq_tuple = sequence_to_tuple(new_seq)
                if new_seq_tuple not in visited:
                    visited.add(new_seq_tuple)
                    queue.append((new_seq, path + [new_seq]))
    
    # No se encontró solución
    return [initial_seq], -1


def calculate_steps_directed(initial_seq: List, target_seq: List) -> Dict:
    """
    Calcula todos los pasos necesarios para transformar la secuencia inicial en la objetivo.
    
    Args:
        initial_seq: Secuencia inicial (con signos como '+1', '-2', etc.)
        target_seq: Secuencia objetivo (con signos)
        
    Returns:
        Diccionario con información completa de los pasos
    """
    start_time = time.time()
    
    # Parsear secuencias
    initial_parsed = parse_signed_sequence(initial_seq)
    target_parsed = parse_signed_sequence(target_seq)
    
    steps, num_steps = reversal_distance_directed_bfs(initial_parsed, target_parsed)
    
    end_time = time.time()
    
    # Identificar las reversiones aplicadas
    reversions = []
    for i in range(len(steps) - 1):
        current = steps[i]
        next_seq = steps[i + 1]
        
        # Encontrar dónde ocurrió la reversión
        for start in range(len(current)):
            for end in range(start, len(current)):
                if apply_reversal_directed(current, start, end) == next_seq:
                    reversions.append((start, end))
                    break
            else:
                continue
            break
    
    return {
        'initial': initial_seq,
        'target': target_seq,
        'steps': [[str(elem) for elem in step] for step in steps],
        'num_steps': num_steps,
        'reversions': reversions,
        'time': end_time - start_time
    }


def reversal_sort_directed(initial_seq: List, target_seq: List) -> Dict:
    """
    Función principal para sorting por reversiones con dirección.
    
    Args:
        initial_seq: Secuencia inicial (máximo 10 elementos, con signos)
        target_seq: Secuencia objetivo (máximo 10 elementos, con signos)
        
    Returns:
        Diccionario con toda la información del proceso
    """
    return calculate_steps_directed(initial_seq, target_seq)


if __name__ == "__main__":
    # Pruebas del módulo
    print("  REVERSAL CON DIRECCIÓN - Pruebas")
    print("=" * 60)
    
    # Prueba 1: Caso simple con negativas
    print("\n Prueba 1: Invertir direcciones")
    initial = ['+1', '-2', '+3', '-4']
    target = ['+1', '+2', '+3', '+4']
    
    result = reversal_sort_directed(initial, target)
    
    print(f"\nSecuencia inicial: {result['initial']}")
    print(f"Secuencia objetivo: {result['target']}")
    print(f"\nPasos de transformación:")
    for i, step in enumerate(result['steps']):
        if i < len(result['reversions']):
            rev = result['reversions'][i]
            # Mostrar la secuencia con formato
            step_str = "  ".join([f"[{x}]" for x in step])
            print(f"  Paso {i}: {step_str}")
            
            # Crear el subrayado para la reversión
            if i < len(result['steps']) - 1:
                underline_parts = []
                for idx, elem in enumerate(step):
                    elem_str = f"[{elem}]"
                    if rev[0] <= idx <= rev[1]:
                        # Subrayar los elementos en el rango de reversión
                        underline_parts.append("─" * len(elem_str))
                    else:
                        underline_parts.append(" " * len(elem_str))
                
                underline = "  ".join(underline_parts)
                print(f"          {underline}")
        else:
            step_str = "  ".join([f"[{x}]" for x in step])
            print(f"  Paso {i}: {step_str} - Objetivo")
    
    print(f"\n Total de pasos: {result['num_steps']}")
    print(f"  Tiempo de ejecución: {result['time']:.6f} segundos")
    
    # Prueba 2: Caso más complejo
    print("\n" + "=" * 60)
    print("\n Prueba 2: Reordenar y cambiar direcciones")
    initial2 = ['-3', '+1', '-2']
    target2 = ['+1', '+2', '+3']
    
    result2 = reversal_sort_directed(initial2, target2)
    
    print(f"\nSecuencia inicial: {result2['initial']}")
    print(f"Secuencia objetivo: {result2['target']}")
    print(f"\n Total de pasos: {result2['num_steps']}")
    print(f"  Tiempo de ejecución: {result2['time']:.6f} segundos")
    
    print("\n" + "=" * 60)
