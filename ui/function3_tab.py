"""
Tab para Función 3: Reversal Con Dirección
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.reversal_directed import reversal_sort_directed, expand_sequence_with_lr
from core.visualization import create_expanded_sequence_diagram
from utils.validators import ValidationError, parse_input_sequence, validate_sequence_length
from utils.timer import format_time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


TARGET_SORTED_THREE = "+1, +2, +3"
TARGET_SORTED_FOUR = "+1, +2, +3, +4"
TARGET_SORTED_FIVE = "+1, +2, +3, +4, +5"
TARGET_SORTED_SIX = "+1, +2, +3, +4, +5, +6"
DEFAULT_SIGNED_INITIAL = "+1, -2, +3, -4"

EXAMPLE_PAIRS = [
    (DEFAULT_SIGNED_INITIAL, TARGET_SORTED_FOUR),
    ("-3, +1, -2", TARGET_SORTED_THREE),
    ("+2, -1, +4, -3", TARGET_SORTED_FOUR),
    ("-1, -2, +3, +4", TARGET_SORTED_FOUR),
    ("+4, -1, -3, +2", TARGET_SORTED_FOUR),
    ("-5, +3, -1, +2, -4", TARGET_SORTED_FIVE),
    ("+3, -4, +1, -2", TARGET_SORTED_FOUR),
    ("-2, +4, -1, +3", TARGET_SORTED_FOUR),
    ("+1, -3, +2, -4", TARGET_SORTED_FOUR),
    ("-6, +5, -4, +3, -2, +1", TARGET_SORTED_SIX),
]


class Function3Tab(ttk.Frame):
    """Tab para la Función 3: Reversal Con Dirección"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()
    
    def create_widgets(self):
        """Crea los widgets del tab"""
        # Marco principal
        main_frame = ttk.Frame(self, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # ===== LAYOUT: 
        # [1] [3] [3]
        # [2] [3] [3]
        # Donde: 1=Input, 2=Pasos, 3=Visualización (2/3 ancho, todo el alto)
        
        # Frame de entrada (posición 1 - arriba izquierda, 1/3 ancho)
        input_frame = ttk.LabelFrame(main_frame, text="Secuencias de Entrada", padding="10")
        input_frame.grid(row=0, column=0, pady=10, padx=(0, 5), sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Nota informativa
        info_text = "Use + o - antes de cada elemento (ej: +1, -2, +3)"
        ttk.Label(input_frame, text=info_text, foreground="blue", 
                 font=('Arial', 9, 'italic')).grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        # Secuencia inicial
        ttk.Label(input_frame, text="Secuencia Inicial:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Label(
            input_frame,
            text="(con signos: +1, -2, +3)",
            font=('Arial', 8, 'italic')
        ).grid(row=2, column=0, sticky=tk.W, pady=2)
        self.initial_entry = ttk.Entry(input_frame, width=35)
        self.initial_entry.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=5)
        self.initial_entry.insert(0, EXAMPLE_PAIRS[0][0])
        
        # Secuencia objetivo
        ttk.Label(input_frame, text="Secuencia Objetivo:").grid(row=4, column=0, sticky=tk.W, pady=(10, 5))
        ttk.Label(
            input_frame,
            text="(con signos: +1, -2, +3)",
            font=('Arial', 8, 'italic')
        ).grid(row=5, column=0, sticky=tk.W, pady=2)
        self.target_entry = ttk.Entry(input_frame, width=35)
        self.target_entry.grid(row=6, column=0, sticky=(tk.W, tk.E), pady=5)
        self.target_entry.insert(0, EXAMPLE_PAIRS[0][1])
        
        # Botones
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=7, column=0, pady=(15, 5))
        
        ttk.Button(button_frame, text="Calcular Pasos", 
                  command=self.calculate_steps).pack(pady=3, fill=tk.X)
        ttk.Button(button_frame, text="Limpiar", 
                  command=self.clear_results).pack(pady=3, fill=tk.X)
        ttk.Button(button_frame, text="Ejemplo", 
                  command=self.load_example).pack(pady=3, fill=tk.X)
        
        # Frame de resultados (posición 2 - abajo izquierda, 1/3 ancho)
        results_frame = ttk.LabelFrame(main_frame, text="Pasos de Transformación", padding="10")
        results_frame.grid(row=1, column=0, pady=(0, 10), padx=(0, 5), sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Text widget con scroll
        text_frame = ttk.Frame(results_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.results_text = tk.Text(text_frame, height=15, width=60, wrap=tk.WORD, font=('Courier', 10))
        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.results_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_text['yscrollcommand'] = scrollbar.set
        
        # Frame de estadísticas (dentro de results_frame)
        stats_frame = ttk.Frame(results_frame)
        stats_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.stats_label = ttk.Label(stats_frame, text="", justify=tk.LEFT, font=('Arial', 10))
        self.stats_label.pack(anchor=tk.W)
        
        # Frame de visualización (posición 3 - lado derecho, 2/3 ancho, 2 filas de alto)
        self.viz_frame = ttk.LabelFrame(main_frame, text="Visualización Gráfica", padding="10")
        self.viz_frame.grid(row=0, column=1, rowspan=2, pady=10, padx=(5, 0), sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Controles de paso para la visualización
        self.step_control_frame = ttk.Frame(self.viz_frame)
        self.step_control_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(self.step_control_frame, text="Paso de visualización:").pack(side=tk.LEFT, padx=5)
        
        self.viz_step_var = tk.IntVar(value=0)
        self.viz_step_label = ttk.Label(self.step_control_frame, text="0", font=('Arial', 10, 'bold'))
        self.viz_step_label.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(self.step_control_frame, text="◀ Anterior", 
                  command=self.prev_viz_step, width=12).pack(side=tk.LEFT, padx=2)
        ttk.Button(self.step_control_frame, text="Siguiente ▶", 
                  command=self.next_viz_step, width=12).pack(side=tk.LEFT, padx=2)
        
        # Canvas para matplotlib
        self.viz_canvas = None
        self.viz_fig = None
        self.current_result = None  # Guardar el resultado completo del cálculo
        self.max_viz_step = 0  # Máximo paso de visualización disponible
        self.viz_steps_per_algorithm_step = 3  # Pasos de visualización por cada paso del algoritmo
        
        # Configurar weights para redimensionamiento
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        # Configurar columnas: 1/3 para izquierda, 2/3 para derecha
        main_frame.columnconfigure(0, weight=1)  # Columna izquierda (1/3)
        main_frame.columnconfigure(1, weight=2)  # Columna derecha (2/3)
        main_frame.rowconfigure(0, weight=1)      # Fila superior
        main_frame.rowconfigure(1, weight=1)      # Fila inferior
        
        input_frame.columnconfigure(0, weight=1)
        results_frame.columnconfigure(0, weight=1)
    
    def calculate_steps(self):
        """Calcula y muestra los pasos de transformación"""
        try:
            # Obtener secuencias
            initial_str = self.initial_entry.get()
            target_str = self.target_entry.get()
            
            initial_seq = parse_input_sequence(initial_str)
            target_seq = parse_input_sequence(target_str)
            
            # Validar longitud
            validate_sequence_length(initial_seq, max_length=10)
            validate_sequence_length(target_seq, max_length=10)
            
            if len(initial_seq) != len(target_seq):
                raise ValidationError("Las secuencias deben tener la misma longitud")
            
            # Calcular
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, " Calculando pasos...\n\n")
            self.update()
            
            result = reversal_sort_directed(initial_seq, target_seq)
            
            # Limpiar y mostrar resultados
            self.results_text.delete(1.0, tk.END)
            
            output = []
            output.append("=" * 70)
            output.append("  REVERSAL CON DIRECCIÓN")
            output.append("=" * 70)
            output.append("")
            
            # Mostrar pasos
            for i, step in enumerate(result['steps']):
                # Formatear la secuencia con espacios entre elementos
                step_str = "  ".join([f"[{elem}]" for elem in step])
                
                if i == 0:
                    output.append(f"Paso {i}: {step_str} - Inicial")
                elif i == len(result['steps']) - 1:
                    output.append(f"Paso {i}: {step_str} - Objetivo")
                else:
                    output.append(f"Paso {i}: {step_str}")
                
                # Mostrar reversión con subrayado si existe
                if i < len(result['reversions']):
                    rev = result['reversions'][i]
                    
                    # Crear el subrayado para la reversión
                    underline_parts = []
                    for idx, elem in enumerate(step):
                        elem_str = f"[{elem}]"
                        if rev[0] <= idx <= rev[1]:
                            # Subrayar los elementos en el rango de reversión
                            underline_parts.append("─" * len(elem_str))
                        else:
                            underline_parts.append(" " * len(elem_str))
                    
                    underline = "  ".join(underline_parts)
                    output.append(f"        {underline}")
                    output.append("")
            
            output.append("")
            output.append("=" * 70)
            
            self.results_text.insert(tk.END, "\n".join(output))
            
            # Actualizar estadísticas
            stats = []
            stats.append(f"Total de pasos: {result['num_steps']}")
            stats.append(f"Tiempo de ejecución: {format_time(result['time'])}")
            # stats.append(f"Elementos en secuencia: {len(initial_seq)}")
            
            self.stats_label.config(text="\n".join(stats))
            
            # Guardar el resultado completo para la visualización
            self.current_result = result
            # Paso 0 del algoritmo tiene 3 sub-pasos (nodos, uniones, ciclos)
            # Pasos siguientes tienen 2 sub-pasos (uniones, ciclos) - sin "solo nodos"
            num_algorithm_steps = len(result['steps'])
            # Total: 3 para el paso 0 + 2 para cada paso siguiente
            self.max_viz_step = 3 + (num_algorithm_steps - 1) * 2 - 1
            
            # Crear visualización del paso 0 (secuencia inicial, solo nodos)
            self.viz_step_var.set(0)
            # Verificar que el widget existe antes de configurarlo
            if hasattr(self, 'viz_step_label') and self.viz_step_label.winfo_exists():
                self.viz_step_label.config(text=f"0 / {self.max_viz_step}")
            self.update_visualization(step=0)
            
        except ValidationError as e:
            messagebox.showerror("Error de Validación", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular pasos: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def clear_results(self):
        """Limpia los resultados"""
        self.results_text.delete(1.0, tk.END)
        self.stats_label.config(text="")
        self.current_result = None
        self.max_viz_step = 0
        self.viz_step_var.set(0)
        # Verificar que el widget existe antes de configurarlo
        if hasattr(self, 'viz_step_label') and self.viz_step_label.winfo_exists():
            self.viz_step_label.config(text="0")
        self.clear_visualization()
    
    def update_visualization(self, step: int = None):
        """Actualiza la visualización con el paso específico de visualización"""
        try:
            if self.current_result is None:
                return
            
            # Usar el paso actual si no se especifica
            if step is None:
                step = self.viz_step_var.get()
            
            # Validar que el paso esté en el rango válido
            if step < 0 or step > self.max_viz_step:
                return
            
            # Calcular qué paso del algoritmo y qué sub-paso de visualización corresponde
            # Paso 0 del algoritmo: visualización 0, 1, 2 (nodos, uniones, ciclos)
            # Pasos siguientes: visualización 3, 4, 5, 6, 7, 8... (uniones, ciclos, uniones, ciclos...)
            if step < 3:
                # Paso 0 del algoritmo
                algorithm_step = 0
                viz_substep = step  # 0, 1, o 2
            else:
                # Pasos siguientes del algoritmo
                # step 3, 4 → algoritmo paso 1 (uniones, ciclos)
                # step 5, 6 → algoritmo paso 2 (uniones, ciclos)
                algorithm_step = ((step - 3) // 2) + 1
                viz_substep = ((step - 3) % 2) + 1  # 1 o 2 (uniones o ciclos)
            
            # Validar que el paso del algoritmo sea válido
            if algorithm_step >= len(self.current_result['steps']):
                return
            
            # Obtener la secuencia del paso del algoritmo correspondiente
            current_sequence = self.current_result['steps'][algorithm_step]
            
            # Limpiar visualización anterior (solo el canvas, no los controles)
            if self.viz_canvas is not None:
                self.viz_canvas.get_tk_widget().destroy()
                self.viz_canvas = None
            if self.viz_fig is not None:
                import matplotlib.pyplot as plt
                plt.close(self.viz_fig)
                self.viz_fig = None
            
            # Expandir la secuencia del paso actual
            expanded = expand_sequence_with_lr(current_sequence)
            
            # Determinar qué mostrar según el sub-paso de visualización:
            # Para paso 0 del algoritmo: viz_substep 0=solo nodos, 1=uniones, 2=ciclos
            # Para pasos siguientes: viz_substep 1=uniones, 2=ciclos
            viz_step = viz_substep if viz_substep <= 2 else 2
            
            # Crear el diagrama sin título
            fig, ax = create_expanded_sequence_diagram(
                expanded, 
                title="",  # Sin título
                step=viz_step
            )
            
            # Integrar en tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.viz_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            self.viz_canvas = canvas
            self.viz_fig = fig
            
        except Exception as e:
            print(f"Error al crear visualización: {e}")
            import traceback
            traceback.print_exc()
    
    def prev_viz_step(self):
        """Retrocede un paso en la visualización"""
        current_step = self.viz_step_var.get()
        if current_step > 0:
            new_step = current_step - 1
            self.viz_step_var.set(new_step)
            if hasattr(self, 'viz_step_label') and self.viz_step_label.winfo_exists():
                self.viz_step_label.config(text=f"{new_step} / {self.max_viz_step}")
            self.update_visualization(step=new_step)
    
    def next_viz_step(self):
        """Avanza un paso en la visualización"""
        current_step = self.viz_step_var.get()
        if current_step < self.max_viz_step:
            new_step = current_step + 1
            self.viz_step_var.set(new_step)
            if hasattr(self, 'viz_step_label') and self.viz_step_label.winfo_exists():
                self.viz_step_label.config(text=f"{new_step} / {self.max_viz_step}")
            self.update_visualization(step=new_step)
    
    def clear_visualization(self):
        """Limpia la visualización"""
        try:
            if self.viz_canvas is not None:
                # Destruir el widget del canvas
                try:
                    self.viz_canvas.get_tk_widget().destroy()
                except:
                    pass
                self.viz_canvas = None
            
            if self.viz_fig is not None:
                import matplotlib.pyplot as plt
                plt.close(self.viz_fig)
                self.viz_fig = None
            
            # Limpiar solo el canvas de matplotlib, no los controles
            # Los controles (step_control_frame) deben permanecer
            if hasattr(self, 'viz_frame'):
                # Destruir solo los widgets que no son los controles
                for widget in list(self.viz_frame.winfo_children()):
                    # Preservar el step_control_frame
                    if hasattr(self, 'step_control_frame') and widget != self.step_control_frame:
                        try:
                            widget.destroy()
                        except:
                            pass
        except Exception as e:
            print(f"Error al limpiar visualización: {e}")
    
    def load_example(self):
        """Carga un ejemplo predefinido"""
        import random
        example = random.choice(EXAMPLE_PAIRS)
        
        self.initial_entry.delete(0, tk.END)
        self.initial_entry.insert(0, example[0])
        
        self.target_entry.delete(0, tk.END)
        self.target_entry.insert(0, example[1])
        
        self.clear_results()


if __name__ == "__main__":
    # Prueba del tab
    root = tk.Tk()
    root.title("Función 3 - Prueba")
    root.geometry("900x750")
    
    tab = Function3Tab(root)
    tab.pack(fill=tk.BOTH, expand=True)
    
    root.mainloop()
