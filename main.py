"""
Reversal con Signo - Bioinformática
Autores: Victor López / Marcelo Paz
Fecha: 28-10-2025
Curso: Bioinformática
"""

import sys
import os

# Añadir el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.main_window import main


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nAplicación cerrada por el usuario")
        import sys
        sys.exit(0)
    except SystemExit:
        # Salida normal del programa
        pass
    except Exception as e:
        print(f"\nError al ejecutar la aplicación: {e}")
        import traceback
        traceback.print_exc()
        import sys
        sys.exit(1)
