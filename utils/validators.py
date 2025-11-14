"""
Utilidad para validación de entradas
"""

from typing import List, Any


class ValidationError(Exception):
    """Excepción personalizada para errores de validación"""
    pass


def validate_sequence_length(sequence: List, min_length: int = None, 
                            max_length: int = None, exact_length: int = None) -> bool:
    """
    Valida la longitud de una secuencia.
    
    Args:
        sequence: Secuencia a validar
        min_length: Longitud mínima permitida
        max_length: Longitud máxima permitida
        exact_length: Longitud exacta requerida
        
    Returns:
        True si la validación es exitosa
        
    Raises:
        ValidationError: Si la validación falla
    """
    if not isinstance(sequence, (list, tuple)):
        raise ValidationError("La entrada debe ser una lista o tupla")
    
    length = len(sequence)
    
    if exact_length is not None and length != exact_length:
        raise ValidationError(
            f"La secuencia debe tener exactamente {exact_length} elementos, "
            f"pero tiene {length}"
        )
    
    if min_length is not None and length < min_length:
        raise ValidationError(
            f"La secuencia debe tener al menos {min_length} elementos, "
            f"pero tiene {length}"
        )
    
    if max_length is not None and length > max_length:
        raise ValidationError(
            f"La secuencia debe tener como máximo {max_length} elementos, "
            f"pero tiene {length}"
        )
    
    return True


def validate_same_length(seq1: List, seq2: List) -> bool:
    """
    Valida que dos secuencias tengan la misma longitud.
    
    Args:
        seq1: Primera secuencia
        seq2: Segunda secuencia
        
    Returns:
        True si tienen la misma longitud
        
    Raises:
        ValidationError: Si las longitudes son diferentes
    """
    if len(seq1) != len(seq2):
        raise ValidationError(
            f"Las secuencias deben tener la misma longitud. "
            f"Secuencia 1: {len(seq1)}, Secuencia 2: {len(seq2)}"
        )
    return True


def validate_not_empty(sequence: List) -> bool:
    """
    Valida que una secuencia no esté vacía.
    
    Args:
        sequence: Secuencia a validar
        
    Returns:
        True si no está vacía
        
    Raises:
        ValidationError: Si está vacía
    """
    if not sequence:
        raise ValidationError("La secuencia no puede estar vacía")
    return True


def validate_signed_elements(sequence: List) -> bool:
    """
    Valida que los elementos de una secuencia tengan formato con signo (+/-).
    
    Args:
        sequence: Secuencia a validar
        
    Returns:
        True si todos los elementos tienen signo válido
        
    Raises:
        ValidationError: Si algún elemento no tiene formato válido
    """
    for i, elem in enumerate(sequence):
        elem_str = str(elem)
        if not (elem_str.startswith('+') or elem_str.startswith('-')):
            raise ValidationError(
                f"El elemento en la posición {i} ('{elem}') debe empezar con + o -"
            )
        
        # Validar que después del signo hay un valor válido
        if len(elem_str) < 2:
            raise ValidationError(
                f"El elemento en la posición {i} ('{elem}') no tiene valor después del signo"
            )
    
    return True


def validate_numeric_sequence(sequence: List) -> bool:
    """
    Valida que todos los elementos de una secuencia sean numéricos o convertibles a número.
    
    Args:
        sequence: Secuencia a validar
        
    Returns:
        True si todos los elementos son numéricos
        
    Raises:
        ValidationError: Si algún elemento no es numérico
    """
    for i, elem in enumerate(sequence):
        elem_str = str(elem)
        # Remover signo si existe
        if elem_str.startswith('+') or elem_str.startswith('-'):
            elem_str = elem_str[1:]
        
        if not elem_str.isdigit():
            raise ValidationError(
                f"El elemento en la posición {i} ('{elem}') no es numérico"
            )
    
    return True


def validate_unique_elements(sequence: List, allow_duplicates: bool = True) -> bool:
    """
    Valida que los elementos de una secuencia sean únicos.
    
    Args:
        sequence: Secuencia a validar
        allow_duplicates: Si False, lanza error si hay duplicados
        
    Returns:
        True si pasa la validación
        
    Raises:
        ValidationError: Si hay duplicados y allow_duplicates es False
    """
    if not allow_duplicates:
        if len(sequence) != len(set(map(str, sequence))):
            raise ValidationError("La secuencia contiene elementos duplicados")
    
    return True


def parse_input_sequence(input_str: str, separator: str = ',') -> List[str]:
    """
    Parsea una cadena de entrada en una lista de elementos.
    
    Args:
        input_str: Cadena de entrada (ej: "1,2,3,4" o "+1,-2,+3")
        separator: Separador entre elementos
        
    Returns:
        Lista de elementos parseados
        
    Raises:
        ValidationError: Si el formato es inválido
    """
    if not input_str or not input_str.strip():
        raise ValidationError("La entrada no puede estar vacía")
    
    # Dividir por el separador y limpiar espacios
    elements = [elem.strip() for elem in input_str.split(separator)]
    
    # Filtrar elementos vacíos
    elements = [elem for elem in elements if elem]
    
    if not elements:
        raise ValidationError("No se encontraron elementos válidos en la entrada")
    
    return elements


if __name__ == "__main__":
    # Pruebas del módulo
    print("VALIDATORS - Pruebas")
    print("=" * 60)
    
    # Prueba 1: Validación de longitud
    print("\n Prueba 1: Validación de longitud")
    try:
        validate_sequence_length([1, 2, 3, 4], exact_length=4)
        print("Secuencia de 4 elementos: VÁLIDA")
    except ValidationError as e:
        print(f" Error: {e}")
    
    try:
        validate_sequence_length([1, 2, 3], exact_length=4)
        print("Secuencia de 3 elementos con requerimiento de 4: VÁLIDA")
    except ValidationError as e:
        print(f" Error esperado: {e}")
    
    # Prueba 2: Validación de elementos con signo
    print("\n Prueba 2: Validación de signos")
    try:
        validate_signed_elements(['+1', '-2', '+3', '-4'])
        print("Elementos con signo: VÁLIDOS")
    except ValidationError as e:
        print(f" Error: {e}")
    
    try:
        validate_signed_elements(['1', '2', '3'])
        print("Elementos sin signo: VÁLIDOS")
    except ValidationError as e:
        print(f" Error esperado: {e}")
    
    # Prueba 3: Parseo de entrada
    print("\n Prueba 3: Parseo de entrada")
    try:
        result = parse_input_sequence("+1, -2, +3, -4")
        print(f"Parseado: {result}")
    except ValidationError as e:
        print(f" Error: {e}")
    
    print("\n" + "=" * 60)
