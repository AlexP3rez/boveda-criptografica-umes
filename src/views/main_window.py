import customtkinter as ctk
from tkinter import messagebox, filedialog
import os

# Configuración visual global
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")  # Estilo tecnológico/seguridad

class MainWindow:
    def __init__(self, root, controller):
        self.root = root
        self.root.title("Bóveda Digital Inviolable - UMES")
        self.root.geometry("550x450")
        self.controller = controller

        # --- PANEL DE INICIO DE SESIÓN ---
        self.frame_login = ctk.CTkFrame(self.root, corner_radius=20)
        self.frame_login.pack(pady=40, padx=40, fill="both", expand=True)

        self.label_titulo = ctk.CTkLabel(self.frame_login, text="CONTROL DE ACCESO", 
                                          font=("Urbanist", 24, "bold"), text_color="#DEFF9A")
        self.label_titulo.pack(pady=(30, 20))

        self.entry_usuario = ctk.CTkEntry(self.frame_login, placeholder_text="Nombre de Usuario", 
                                          width=250, height=40, corner_radius=10)
        self.entry_usuario.pack(pady=10)

        self.entry_password = ctk.CTkEntry(self.frame_login, placeholder_text="Contraseña", 
                                           show="*", width=250, height=40, corner_radius=10)
        self.entry_password.pack(pady=10)

        self.btn_login = ctk.CTkButton(self.frame_login, text="INGRESAR A LA BÓVEDA", 
                                        command=self.ejecutar_login, width=250, height=45, 
                                        corner_radius=10, font=("Urbanist", 14, "bold"))
        self.btn_login.pack(pady=30)

        # --- PANEL PRINCIPAL (OCULTO) ---
        self.frame_main = ctk.CTkFrame(self.root, corner_radius=20)

    def ejecutar_login(self):
        usuario = self.entry_usuario.get()
        password = self.entry_password.get()

        try:
            if self.controller.iniciar_sesion(usuario, password):
                self.mostrar_panel_principal()
        except PermissionError as e:
            messagebox.showerror("Seguridad UMES", str(e))

    def mostrar_panel_principal(self):
        self.frame_login.pack_forget()
        self.frame_main.pack(pady=40, padx=40, fill="both", expand=True)

        ctk.CTkLabel(self.frame_main, text="BÓVEDA CRIPTOGRÁFICA", 
                     font=("Urbanist", 22, "bold"), text_color="#DEFF9A").pack(pady=(20, 30))

        # Botón Cifrar
        self.btn_cifrar = ctk.CTkButton(self.frame_main, text="🔒 CIFRAR ARCHIVO", 
                                        command=lambda: self.seleccionar_archivo("cifrar"),
                                        width=300, height=50, corner_radius=15, fg_color="#2E4D2E")
        self.btn_cifrar.pack(pady=10)

        # Botón Descifrar
        self.btn_descifrar = ctk.CTkButton(self.frame_main, text="🔓 DESCIFRAR ARCHIVO", 
                                           command=lambda: self.seleccionar_archivo("descifrar"),
                                           width=300, height=50, corner_radius=15, fg_color="#1F2937")
        self.btn_descifrar.pack(pady=10)

        # Botón Salir
        self.btn_logout = ctk.CTkButton(self.frame_main, text="Cerrar Bóveda", 
                                         command=self.cerrar_sesion, width=150, 
                                         fg_color="transparent", border_width=1, text_color="gray")
        self.btn_logout.pack(pady=(40, 10))

    def seleccionar_archivo(self, modo):
        ruta = filedialog.askopenfilename(title=f"Seleccionar para {modo}")
        if not ruta: return

        try:
            ruta_final = self.controller.procesar_archivo(modo, ruta)
            messagebox.showinfo("Éxito Militar", f"Proceso de {modo} exitoso.\nDestino: {os.path.basename(ruta_final)}")
        except Exception as e:
            messagebox.showerror("Fallo de Integridad", str(e))

    def cerrar_sesion(self):
        self.controller.cerrar_sesion()
        self.frame_main.pack_forget()
        self.frame_login.pack(pady=40, padx=40, fill="both", expand=True)
        self.entry_password.delete(0, 'end')