# 🛡️ Bóveda Digital Inviolable | Sistema de Cifrado Empresarial

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Cryptography](https://img.shields.io/badge/Security-AES--256--GCM-red.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey.svg)
![UI](https://img.shields.io/badge/UI-CustomTkinter-green.svg)

## 📌 Descripción del Proyecto
Este repositorio contiene el código fuente de una aplicación de cifrado de grado empresarial. [cite_start]El sistema fue diseñado para resolver un caso arquitectónico estricto: garantizar que la información de una organización esté resguardada, que únicamente empleados con el nivel jerárquico adecuado tengan acceso a los datos [cite: 8, 9][cite_start], y que los archivos no puedan ser robados ni alterados por terceros.

[cite_start]Esta solución fue desarrollada como **Proyecto Final de Teoría de la Información** para la carrera de Ingeniería en Sistemas[cite: 4, 5, 6].

## ✨ Características Principales
* [cite_start]**Cifrado de Grado Militar:** Utiliza el estándar avanzado `AES-256` en modo `GCM` (Cifrado Autenticado), asegurando confidencialidad e integridad total.
* [cite_start]**Compatibilidad Multiformato:** Procesa archivos en modo binario, permitiendo cifrar y descifrar imágenes (JPG, PNG), documentos (PDF, DOCX) y archivos de texto plano[cite: 10, 11].
* [cite_start]**Control de Acceso Basado en Roles (RBAC):** Implementación de base de datos local (SQLite) para segmentar a los usuarios por niveles de acceso (Ej. Nivel 1 = Administrador, Nivel 5 = Operador básico)[cite: 9].
* **Defensa contra Fuerza Bruta:** Derivación de claves maestras utilizando `PBKDF2HMAC` con `SHA-256`, `salts` aleatorios y 600,000 iteraciones computacionales.
* **Interfaz Gráfica Moderna:** Construida sobre `CustomTkinter` para ofrecer una experiencia de usuario (UX) estilo "Dark Mode" fluida y profesional.

## 🏗️ Arquitectura de Software
El proyecto está rigurosamente estructurado bajo el patrón **MVC (Modelo-Vista-Controlador)** para garantizar la escalabilidad y el mantenimiento del código:
* `/src/models/`: Contiene el core criptográfico (`crypto_engine.py`) y el gestor de base de datos y roles (`auth_manager.py`).
* `/src/views/`: Contiene la interfaz gráfica interactiva y moderna (`main_window.py`).
* `/src/controllers/`: Orquesta la comunicación entre la interfaz de usuario y las validaciones de seguridad (`app_controller.py`).

## 🚀 Requisitos e Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/SU_USUARIO/boveda-criptografica-umes.git](https://github.com/SU_USUARIO/boveda-criptografica-umes.git)
   cd boveda-criptografica-umes
    ```

2. **Instalar dependencias:**
Se recomienda utilizar un entorno virtual. Para instalar el motor criptográfico y la librería gráfica 
    ejecute:
    ```bash
    pip install -r requirements.txt
    ```
3. **Ejecutar la aplicación:**
    ```bash
    python main.py
    ```

## 🔐 Uso y Credenciales de Prueba
Al iniciar la aplicación por primera vez, el sistema autogenerará la base de datos segura 
(src/database/secure_users.db) y creará un usuario administrador de Nivel 1.

Para evaluar la aplicación, inicie sesión con las siguientes credenciales:
**Usuario:** admin
**Contraseña:** Admin123!

Una vez dentro de la Bóveda Criptográfica, seleccione cualquier archivo local para cifrarlo. El sistema 
generará un nuevo archivo con la extensión .enc garantizando que es 100% confiable e inviolable. 
Seleccione el archivo .enc en la opción de descifrado para restaurarlo.  

## 🎓 Ficha AcadémicaUniversidad: 
Universidad Mesoamericana (UMES) - Sede Quetzaltenango.  
Facultad: Facultad de Ingeniería.  
Carrera: Ingeniería en Sistemas (7mo Semestre).  
Curso: Teoría de la Información.     