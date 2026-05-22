import sqlite3
import hashlib
import hmac
import os
from typing import Optional

class AuthManager:
    """
    Gestor de autenticación y roles utilizando SQLite.
    Asegura que solo usuarios con niveles permitidos puedan operar el motor.
    """

    def __init__(self, db_path: str = "enterprise_auth.db") -> None:
        """
        Inicializa la conexión y prepara la base de datos si no existe.
        """
        self._db_path = db_path
        self._initialize_db()

    def _initialize_db(self) -> None:
        """Crea la tabla de usuarios si no existe."""
        with sqlite3.connect(self._db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    salt TEXT NOT NULL,
                    access_level INTEGER NOT NULL
                )
            """)
            conn.commit()

    def _hash_password(self, password: str, salt: bytes) -> str:
        """Hashea la contraseña de manera segura iterando algoritmos hash."""
        return hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            200000
        ).hex()

    def register_user(self, username: str, password: str, access_level: int) -> bool:
        """
        Registra un nuevo usuario en la base de datos.
        """
        salt = os.urandom(16)
        pwd_hash = self._hash_password(password, salt)
        
        try:
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (username, password_hash, salt, access_level) VALUES (?, ?, ?, ?)",
                    (username, pwd_hash, salt.hex(), access_level)
                )
                conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # El usuario ya existe en el sistema

    def authenticate(self, username: str, password: str) -> Optional[int]:
        """
        Verifica el inicio de sesión de un usuario de forma segura.
        Retorna el nivel de acceso (access_level) si es exitoso, o None en caso de fallo.
        """
        with sqlite3.connect(self._db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT password_hash, salt, access_level FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()

        if row is None:
            return None

        stored_hash, stored_salt_hex, access_level = row
        salt = bytes.fromhex(stored_salt_hex)
        
        computed_hash = self._hash_password(password, salt)
        
        # Previene ataques de tiempo (Timing Attacks)
        if hmac.compare_digest(computed_hash, stored_hash):
            return access_level
        
        return None

    def get_crypto_engine(self, username: str, password: str, min_level: int = 2):
        """
        Autentica al usuario y, si cumple con el nivel mínimo, retorna una instancia de CryptoEngine.
        """
        level = self.authenticate(username, password)
        if level is None:
            raise PermissionError("Autenticación fallida. Credenciales incorrectas.")
        
        if level > min_level:
            raise PermissionError(f"Acceso denegado. Se requiere Nivel {min_level} pero el usuario es Nivel {level}.")
            
        from models.crypto_engine import CryptoEngine
        return CryptoEngine(password)