# Biblioteca-AEIE
Este repositorio tiene como objetivo trabajar en el código para un sistema de biblioteca propio de la AEIE.

```text
biblioteca/
│
├── app.py                  # Archivo principal (main)
├── config.py               # Configuración general
├── requirements.txt        # Librerías del proyecto
├── README.md
│
├── database/
│   ├── database.py         # Conexión a SQLite
│   ├── models.py           # Tablas de la base de datos
│   └── biblioteca.db       # Base de datos (se crea automáticamente)
│
├── routes/
│   ├── home.py             # Página principal
│   ├── admin.py            # Panel de administrador
│   ├── public.py           # Panel público
│   └── books.py            # CRUD de libros
│
├── templates/
│   ├── base.html           # Plantilla base
│   ├── index.html          # Pantalla inicial
│   ├── admin.html          # Panel administrador
│   ├── public.html         # Panel público
│   ├── add_book.html       # Agregar libro
│   ├── edit_book.html      # Editar libro
│   ├── search.html         # Resultados de búsqueda
│   └── details.html        # Información del libro
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   ├── img/
│   │   ├── logo.png
│   │   └── default_book.png
│   └── uploads/
│       └── portadas/
│
├── services/
│   ├── book_service.py     # Funciones para manejar libros
│   └── search_service.py   # Lógica del buscador
│
└── utils/
    └── helpers.py          # Funciones auxiliares