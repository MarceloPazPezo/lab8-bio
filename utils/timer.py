"""
Utilidad para medición de tiempos de ejecución
"""

import time
from functools import wraps
from typing import Callable, Any, Tuple


class Timer:
    """Clase para medir tiempos de ejecución"""
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.elapsed = None
    
    def start(self):
        """Inicia el temporizador"""
        self.start_time = time.time()
        self.end_time = None
        self.elapsed = None
    
    def stop(self):
        """Detiene el temporizador y calcula el tiempo transcurrido"""
        if self.start_time is None:
            raise ValueError("El temporizador no ha sido iniciado")
        
        self.end_time = time.time()
        self.elapsed = self.end_time - self.start_time
        return self.elapsed
    
    def get_elapsed(self) -> float:
        """Obtiene el tiempo transcurrido en segundos"""
        if self.elapsed is None:
            raise ValueError("El temporizador no ha sido detenido")
        return self.elapsed
    
    def get_elapsed_ms(self) -> float:
        """Obtiene el tiempo transcurrido en milisegundos"""
        return self.get_elapsed() * 1000
    
    def __enter__(self):
        """Permite usar con 'with' statement"""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Detiene automáticamente al salir del contexto"""
        self.stop()


def time_function(func: Callable) -> Callable:
    """
    Decorador para medir el tiempo de ejecución de una función.
    
    Args:
        func: Función a decorar
        
    Returns:
        Función decorada que retorna (resultado, tiempo_ejecución)
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Tuple[Any, float]:
        timer = Timer()
        timer.start()
        result = func(*args, **kwargs)
        elapsed = timer.stop()
        return result, elapsed
    
    return wrapper


def format_time(seconds: float) -> str:
    """
    Formatea un tiempo en segundos a una representación legible.
    
    Args:
        seconds: Tiempo en segundos
        
    Returns:
        String formateado (ej: "1.234 seg", "123.4 ms", "12.34 µs")
    """
    if seconds >= 1.0:
        return f"{seconds:.4f} seg"
    elif seconds >= 0.001:
        return f"{seconds * 1000:.4f} ms"
    elif seconds >= 0.000001:
        return f"{seconds * 1000000:.4f} µs"
    else:
        return f"{seconds * 1000000000:.4f} ns"


if __name__ == "__main__":
    # Pruebas del módulo
    print("  TIMER - Pruebas")
    print("=" * 60)
    
    # Prueba 1: Uso básico
    print("\n Prueba 1: Uso básico del Timer")
    timer = Timer()
    timer.start()
    time.sleep(0.1)  # Simular trabajo
    elapsed = timer.stop()
    print(f"Tiempo transcurrido: {format_time(elapsed)}")
    
    # Prueba 2: Context manager
    print("\n Prueba 2: Uso con context manager")
    with Timer() as t:
        time.sleep(0.05)
    print(f"Tiempo transcurrido: {format_time(t.get_elapsed())}")
    
    # Prueba 3: Decorador
    print("\n Prueba 3: Uso con decorador")
    
    @time_function
    def funcion_ejemplo(n):
        total = 0
        for i in range(n):
            total += i
        return total
    
    resultado, tiempo = funcion_ejemplo(1000000)
    print(f"Resultado: {resultado}")
    print(f"Tiempo: {format_time(tiempo)}")
    
    print("\n" + "=" * 60)
