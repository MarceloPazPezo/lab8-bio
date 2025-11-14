"""
Ventana Principal de la Aplicación
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

# Añadir el directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.function3_tab import Function3Tab


ABOUT_TAB_LABEL = "Acerca de"


class AboutTab(ttk.Frame):
    """Tab con información general de la aplicación"""

    def __init__(self, parent):
        super().__init__(parent)
        self.build_content()

    def build_content(self):
        container = ttk.Frame(self, padding="20")
        container.pack(fill=tk.BOTH, expand=True)

        title = ttk.Label(
            container,
            text="Reversal con Signo - Bioinformática",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=(0, 20))

        sections = [
            ("Autores", "Victor López & Marcelo Paz"),
            ("Fecha", "14 de noviembre de 2025"),
            (
                "Descripción",
                "Aplicación para calcular la secuencia de reversiones con dirección (+/-) "
                "necesarias para transformar una secuencia inicial en una objetivo. "
                "Implementa el algoritmo de sorting por reversiones considerando signos."
            ),
        ]

        for header, body in sections:
            frame = ttk.LabelFrame(container, text=header, padding="15")
            frame.pack(fill=tk.X, pady=5)
            label = ttk.Label(frame, text=body, justify=tk.LEFT, wraplength=700)
            label.pack(anchor=tk.W)


class MainWindow(tk.Tk):
    """Ventana principal de la aplicación"""
    
    def __init__(self):
        super().__init__()
        
        self.title("Reversal con Signo - Bioinformática")
        
        # Configurar para pantalla completa (maximizada)
        self.state('zoomed')  # En Windows maximiza la ventana
        # Alternativa para Linux: self.attributes('-zoomed', True)
        # Para pantalla completa real: self.attributes('-fullscreen', True)

        # Configurar estilo
        self.configure_styles()
        
        # Crear widgets
        self.create_widgets()

        # Crear menú superior
        self.create_menu()
        
        # Configurar cierre
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def configure_styles(self):
        """Configura los estilos de la aplicación"""
        style = ttk.Style()
        
        # Tema
        try:
            style.theme_use('clam')
        except tk.TclError:
            pass
        
        # Colores personalizados
        style.configure('TNotebook', background='#ECF0F1')
        style.configure('TNotebook.Tab', padding=[20, 10])
        style.configure('TFrame', background='#ECF0F1')
        style.configure('TLabelframe', background='#ECF0F1')
        style.configure('TLabel', background='#ECF0F1')

        # Estilo para ocultar pestañas del notebook
        style.layout('Hidden.TNotebook.Tab', [])
        style.configure('Hidden.TNotebook', background='#ECF0F1')
    
    def create_widgets(self):
        """Crea los widgets de la ventana principal"""
        # Frame principal
        main_frame = ttk.Frame(self, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Notebook (Tabs)
        self.notebook = ttk.Notebook(main_frame, style='Hidden.TNotebook')
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Crear tabs
        self.tab3 = Function3Tab(self.notebook)
        self.tab_about = AboutTab(self.notebook)
        
        # Añadir tabs al notebook
        self.notebook.add(self.tab3, text="Reversal con Signo")
        self.notebook.add(self.tab_about, text=ABOUT_TAB_LABEL)

        # Sin pestañas visibles, necesitamos manejar selección manualmente
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
        
        # Configurar weights para redimensionamiento
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)
    
    def create_menu(self):
        """Crea la barra de menú para navegación"""
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        self.selected_tab = tk.IntVar(value=0)

        tabs = [
            ("Reversal con Signo", 0),
            (ABOUT_TAB_LABEL, 1),
        ]

        self.menu_tab_items = []
        for label, index in tabs:
            self.menu_bar.add_command(
                label=label,
                command=lambda idx=index: self.select_tab(idx)
            )
            position = self.menu_bar.index('end')
            self.menu_tab_items.append({'position': position, 'label': label, 'index': index})

        # Seleccionar pestaña inicial a través del menú
        self.select_tab(self.selected_tab.get())

    def select_tab(self, index: int):
        """Selecciona una pestaña en el notebook"""
        self.notebook.select(index)
        self.selected_tab.set(index)
        self.update_menu_tab_labels(index)

    def on_tab_changed(self, event):
        """Actualiza el menú cuando cambia la pestaña."""
        current = self.notebook.index(self.notebook.select())
        self.selected_tab.set(current)
        self.update_menu_tab_labels(current)

    def update_menu_tab_labels(self, active_index: int):
        """Actualiza las etiquetas del menú para reflejar la pestaña seleccionada."""
        if not hasattr(self, 'menu_tab_items'):
            return
        for item in self.menu_tab_items:
            label = f"[{item['label']}]" if item['index'] == active_index else item['label']
            self.menu_bar.entryconfig(item['position'], label=label)

    def on_closing(self):
        """Maneja el cierre de la ventana"""
        # Limpiar visualizaciones de matplotlib antes de cerrar
        try:
            # Limpiar visualización del tab3 si existe
            if hasattr(self, 'tab3') and hasattr(self.tab3, 'clear_visualization'):
                self.tab3.clear_visualization()
            
            # Cerrar todas las figuras de matplotlib
            import matplotlib.pyplot as plt
            plt.close('all')
        except Exception as e:
            print(f"Error al limpiar visualizaciones: {e}")
        
        # Destruir la ventana
        self.destroy()
        
        # Forzar salida del programa
        import sys
        sys.exit(0)

def main():
    """Función principal"""
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
