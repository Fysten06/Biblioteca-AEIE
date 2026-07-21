import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "biblioteca.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS libros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            categoria TEXT NOT NULL DEFAULT 'General',
            anio INTEGER,
            editorial TEXT,
            isbn TEXT,
            disponible INTEGER DEFAULT 1,
            descripcion TEXT,
            fecha_agregado TEXT DEFAULT (datetime('now','-6 hours'))
        )
    """)

    # Datos de ejemplo si la tabla está vacía
    cursor.execute("SELECT COUNT(*) FROM libros")
    if cursor.fetchone()[0] == 0:
        ejemplos = [
            ("Circuitos Eléctricos", "James W. Nilsson", "Circuitos", 2020, "Pearson", "978-0133760033"),
            ("Análisis Básico de Circuitos", "David E. Johnson", "Circuitos", 2018, "Prentice Hall", "978-0130606017"),
            ("Fundamentos de Circuitos Eléctricos", "Charles K. Alexander", "Circuitos", 2021, "McGraw-Hill", "978-0078028229"),
            ("Electrónica: Teoría de Circuitos", "Robert L. Boylestad", "Electrónica", 2019, "Pearson", "978-0134982461"),
            ("Microelectrónica", "Adel S. Sedra", "Electrónica", 2020, "Oxford", "978-0197505392"),
            ("Máquinas Eléctricas", "Stephen J. Chapman", "Máquinas Eléctricas", 2018, "McGraw-Hill", "978-1260590937"),
            ("Máquinas Eléctricas Rotativas", "Jesús Fraile Mora", "Máquinas Eléctricas", 2017, "Ibergarceta", "978-8417289201"),
            ("Sistemas Eléctricos de Potencia", "John J. Grainger", "Potencia", 2019, "McGraw-Hill", "978-1259850622"),
            ("Matemáticas Avanzadas para Ingeniería", "Erwin Kreyszig", "Matemáticas", 2020, "Wiley", "978-0470458365"),
            ("Ecuaciones Diferenciales", "Dennis G. Zill", "Matemáticas", 2018, "Cengage", "978-1337552220"),
        ]
        for libro in ejemplos:
            cursor.execute("""
                INSERT INTO libros (titulo, autor, categoria, anio, editorial, isbn, disponible)
                VALUES (?, ?, ?, ?, ?, ?, 1)
            """, libro)

    conn.commit()
    conn.close()


def buscar_libros(termino, categoria=None, disponible=None, orden=None):
    conn = get_connection()
    query = """
        SELECT * FROM libros
        WHERE (titulo LIKE ? OR autor LIKE ? OR categoria LIKE ?)
    """
    params = [f"%{termino}%", f"%{termino}%", f"%{termino}%"]

    if categoria:
        query += " AND categoria = ?"
        params.append(categoria)

    if disponible is not None:
        query += " AND disponible = ?"
        params.append(1 if disponible else 0)

    if orden == "nombre":
        query += " ORDER BY titulo ASC"
    elif orden == "autor":
        query += " ORDER BY autor ASC"
    elif orden == "anio":
        query += " ORDER BY anio DESC"
    else:
        query += " ORDER BY titulo ASC"

    cursor = conn.cursor()
    cursor.execute(query, params)
    resultados = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return resultados


def obtener_categorias():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT categoria FROM libros ORDER BY categoria")
    categorias = [row["categoria"] for row in cursor.fetchall()]
    conn.close()
    return categorias
