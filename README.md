# Sistema de Gestión Hospitalaria

Sistema web moderno para la gestión integral de hospitales, desarrollado con **Flask** y **MySQL**. Permite administrar pacientes, doctores, citas, tratamientos y más, con una interfaz atractiva y responsiva.

## Características

- **Gestión de Pacientes:** Registro, edición, consulta y eliminación.
- **Gestión de Doctores:** Administración completa de datos de médicos.
- **Gestión de Citas:** Programación, edición y control de citas médicas.
- **Gestión de Tratamientos:** Registro y seguimiento de tratamientos médicos.
- **Interfaz moderna:** Diseño responsivo, limpio y profesional.
- **Integración con MySQL:** Persistencia de datos robusta.
- **Arquitectura modular:** Separación por servicios y blueprints.

## Estructura del Proyecto

```
.
├── app.py                  # Punto de entrada principal (Flask)
├── config.py               # Configuración de la base de datos y claves
├── requirements.txt        # Dependencias del proyecto
├── .gitignore
├── templates/              # Vistas HTML (Jinja2)
│   ├── index.html
│   ├── pacientes.html
│   ├── doctores.html
│   ├── citas.html
│   └── tratamientos.html
├── static/
│   ├── css/
│   │   └── styles.css      # Estilos personalizados
│   ├── js/                 # Scripts JS para cada módulo
│   └── images/
│       └── hero.jpg        # Imagen principal del home
└── services/               # Lógica de negocio modularizada
    ├── pacientes/
    ├── doctores/
    ├── citas/
    └── tratamientos/
```

## Instalación

1. **Clona el repositorio:**
   ```bash
   git clone <URL-del-repo>
   cd Hospital
   ```

2. **Crea un entorno virtual (opcional pero recomendado):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura la base de datos:**
   - Crea una base de datos MySQL llamada `hospitaldb`.
   - Ajusta usuario y contraseña en `config.py` si es necesario.

5. **Ejecuta la aplicación:**
   ```bash
   python app.py
   ```
   Accede a [http://127.0.0.1:5000](http://127.0.0.1:5000) en tu navegador.

## Configuración

El archivo `config.py` contiene los parámetros de conexión a la base de datos y la clave secreta de Flask:

```python
class Config:
    SECRET_KEY = '...'
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'hospitaldb'
```

## Personalización

- **Estilos:** Modifica `static/css/styles.css` para adaptar colores y diseño.
- **Imágenes:** Cambia `static/images/hero.jpg` para personalizar la portada.
- **Lógica de negocio:** Cada módulo (pacientes, doctores, etc.) tiene su propia carpeta en `services/`.

## Créditos

Desarrollado por [Tu Nombre o Equipo].  
Inspirado en las mejores prácticas de desarrollo web y UI para salud. 