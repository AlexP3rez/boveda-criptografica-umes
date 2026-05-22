from models.auth_manager import AuthManager
import os

class AppController:
    def __init__(self):
        # Inicializa la base de datos de usuarios
        self.auth = AuthManager("src/database/secure_users.db")
        self.motor_cripto = None
        self.usuario_actual = None
        
        # Registramos un usuario administrador por defecto para pruebas
        self.auth.register_user("admin", "Admin123!", access_level=1)

    def iniciar_sesion(self, usuario: str, contrasena: str) -> bool:
        """Intenta autenticar al usuario y generar el motor criptográfico."""
        try:
            # Exigimos nivel 2 o menor para operar el sistema
            self.motor_cripto = self.auth.get_crypto_engine(usuario, contrasena, min_level=2)
            self.usuario_actual = usuario
            return True
        except PermissionError as e:
            # Si falla (credenciales incorrectas o nivel insuficiente), propagamos el error
            raise e

    def cerrar_sesion(self):
        """Destruye la instancia del motor criptográfico por seguridad."""
        self.motor_cripto = None
        self.usuario_actual = None

    def procesar_archivo(self, modo: str, ruta_origen: str) -> str:
        """
        Orquesta el cifrado o descifrado de archivos.
        Devuelve la ruta del archivo resultante.
        """
        if not self.motor_cripto:
            raise PermissionError("Acceso denegado: No hay una sesión activa.")

        if modo == "cifrar":
            ruta_destino = ruta_origen + ".enc"
            self.motor_cripto.encrypt_file(ruta_origen, ruta_destino)
            return ruta_destino
            
        elif modo == "descifrar":
            if not ruta_origen.endswith(".enc"):
                raise ValueError("El archivo seleccionado no tiene la extensión cifrada (.enc).")
            # Quita la extensión .enc para restaurar el archivo
            ruta_destino = ruta_origen.rsplit(".enc", 1)[0]
            self.motor_cripto.decrypt_file(ruta_origen, ruta_destino)
            return ruta_destino
        else:
            raise ValueError("Modo de operación no válido.")