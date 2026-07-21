import sqlite3
import os


# CONFIGURACIÓN

DB_PATH = os.path.join(os.path.dirname(__file__), "database", "biblioteca.db")

# CONEXIÓN


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# CREAR BASE DE DATOS

def init_db():

    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS libros (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            titulo TEXT NOT NULL,

            autor TEXT NOT NULL,

            editorial TEXT,

            categoria TEXT NOT NULL DEFAULT 'General',

            anio INTEGER,

            isbn TEXT,

            descripcion TEXT,

            cantidad INTEGER NOT NULL DEFAULT 1,

            disponibles INTEGER NOT NULL DEFAULT 1

        )
    """)

    conn.commit()
    conn.close()


# FUNCIONES PÚBLICO

def obtener_libros():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM libros
        ORDER BY titulo ASC
    """)

    libros = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return libros


def buscar_libros(termino="", categoria=None):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT *
        FROM libros
        WHERE
            titulo LIKE ?
            OR autor LIKE ?
            OR categoria LIKE ?
    """

    parametros = [
        f"%{termino}%",
        f"%{termino}%",
        f"%{termino}%"
    ]

    if categoria:

        query += " AND categoria = ?"
        parametros.append(categoria)

    query += " ORDER BY titulo ASC"

    cursor.execute(query, parametros)

    libros = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return libros


def obtener_categorias():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DISTINCT categoria
        FROM libros
        ORDER BY categoria
    """)

    categorias = [row["categoria"] for row in cursor.fetchall()]

    conn.close()

    return categorias


# FUNCIONES ADMINISTRADOR

def agregar_libro(
    titulo,
    autor,
    editorial,
    categoria,
    anio,
    isbn,
    descripcion,
    cantidad
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO libros(

            titulo,
            autor,
            editorial,
            categoria,
            anio,
            isbn,
            descripcion,
            cantidad,
            disponibles

        )

        VALUES(?,?,?,?,?,?,?,?,?)

    """, (

        titulo,
        autor,
        editorial,
        categoria,
        anio,
        isbn,
        descripcion,
        cantidad,
        cantidad

    ))

    conn.commit()
    conn.close()


def obtener_libro_por_id(id_libro):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT *
        FROM libros
        WHERE id = ?

    """, (id_libro,))

    libro = cursor.fetchone()

    conn.close()

    if libro:
        return dict(libro)

    return None


def editar_libro(

    id_libro,
    titulo,
    autor,
    editorial,
    categoria,
    anio,
    isbn,
    descripcion,
    cantidad,
    disponibles

):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        UPDATE libros

        SET

            titulo = ?,
            autor = ?,
            editorial = ?,
            categoria = ?,
            anio = ?,
            isbn = ?,
            descripcion = ?,
            cantidad = ?,
            disponibles = ?

        WHERE id = ?

    """, (

        titulo,
        autor,
        editorial,
        categoria,
        anio,
        isbn,
        descripcion,
        cantidad,
        disponibles,
        id_libro

    ))

    conn.commit()
    conn.close()


def eliminar_libro(id_libro):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        DELETE FROM libros
        WHERE id = ?

    """, (id_libro,))

    conn.commit()
    conn.close()