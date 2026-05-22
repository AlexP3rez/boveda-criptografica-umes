import sys
import os
import customtkinter as ctk

# Ruta src
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from controllers.app_controller import AppController
from views.main_window import MainWindow

if __name__ == "__main__":
    controlador = AppController()
    
    # IMPORTANTE: Usamos CTk en lugar de Tk para el estilo moderno
    root = ctk.CTk()
    
    app = MainWindow(root, controlador)
    root.mainloop()