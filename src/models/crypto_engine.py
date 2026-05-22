import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidTag

class CryptoEngine:
    """
    Motor criptográfico empresarial para cifrar y descifrar archivos
    utilizando el estándar AES-256 en modo GCM (Cifrado Autenticado).
    """

    def __init__(self, password: str) -> None:
        """
        Inicializa el motor criptográfico.
        
        Args:
            password (str): Contraseña utilizada para derivar la clave maestra.
        """
        self._password_bytes: bytes = password.encode('utf-8')
        self._salt_size: int = 16
        self._nonce_size: int = 12

    def _derive_key(self, salt: bytes) -> bytes:
        """
        Deriva una clave de 32 bytes (256 bits) usando PBKDF2HMAC.
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=600000,
        )
        return kdf.derive(self._password_bytes)

    def encrypt_file(self, input_path: str, output_path: str) -> None:
        """
        Cifra un archivo en modo binario y guarda el salt y el nonce en la cabecera.
        """
        salt = os.urandom(self._salt_size)
        key = self._derive_key(salt)
        aesgcm = AESGCM(key)
        nonce = os.urandom(self._nonce_size)

        with open(input_path, 'rb') as f:
            plaintext = f.read()

        ciphertext = aesgcm.encrypt(nonce, plaintext, None)

        with open(output_path, 'wb') as f:
            f.write(salt)
            f.write(nonce)
            f.write(ciphertext)

    def decrypt_file(self, input_path: str, output_path: str) -> None:
        """
        Descifra un archivo validando su integridad mediante la etiqueta GCM.
        """
        with open(input_path, 'rb') as f:
            file_data = f.read()

        if len(file_data) < self._salt_size + self._nonce_size:
            raise ValueError("El archivo está corrupto o tiene un tamaño inválido.")

        salt = file_data[:self._salt_size]
        nonce = file_data[self._salt_size : self._salt_size + self._nonce_size]
        ciphertext = file_data[self._salt_size + self._nonce_size:]

        key = self._derive_key(salt)
        aesgcm = AESGCM(key)

        try:
            plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        except InvalidTag:
            raise ValueError("Integridad comprometida: El archivo ha sido modificado, la etiqueta GCM es inválida o la contraseña es incorrecta.")

        with open(output_path, 'wb') as f:
            f.write(plaintext)