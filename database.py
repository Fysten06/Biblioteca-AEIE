import sqlite3
import os


DB_PATH = os.path.join(
    os.path.dirname(__file__),
    "biblioteca.db"
)


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

            cantidad INTEGER DEFAULT 1,

            disponibles INTEGER DEFAULT 1,

            descripcion TEXT,

            imagen TEXT,

            fecha_agregado TEXT DEFAULT (datetime('now','-6 hours'))

        )
    """)


    conn.commit()

    conn.close()



def agregar_libro(
    titulo,
    autor,
    editorial,
    categoria,
    anio,
    isbn,
    descripcion,
    cantidad,
    imagen
):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute("""
        INSERT INTO libros
        (
            titulo,
            autor,
            editorial,
            categoria,
            anio,
            isbn,
            cantidad,
            disponibles,
            descripcion,
            imagen
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

    """,
    (
        titulo,
        autor,
        editorial,
        categoria,
        anio,
        isbn,
        cantidad,
        cantidad,
        descripcion,
        imagen
    ))


    conn.commit()

    conn.close()



def obtener_libros():

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute("""
        SELECT *
        FROM libros
        ORDER BY titulo ASC
    """)


    libros = [
        dict(row)
        for row in cursor.fetchall()
    ]


    conn.close()


    return libros



def obtener_libro_por_id(id):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute("""
        SELECT *
        FROM libros
        WHERE id = ?
    """,
    (id,))


    libro = cursor.fetchone()


    conn.close()


    if libro:

        return dict(libro)


    return None



def eliminar_libro(id):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute("""
        DELETE FROM libros
        WHERE id = ?
    """,
    (id,))


    conn.commit()

    conn.close()



def editar_libro(
    id,
    titulo,
    autor,
    editorial,
    categoria,
    anio,
    isbn,
    descripcion,
    cantidad,
    disponibles,
    imagen
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

            disponibles = ?,

            imagen = ?

        WHERE id = ?

    """,
    (
        titulo,
        autor,
        editorial,
        categoria,
        anio,
        isbn,
        descripcion,
        cantidad,
        disponibles,
        imagen,
        id
    ))


    conn.commit()

    conn.close()



def buscar_libros(termino):

    conn = get_connection()

    cursor = conn.cursor()


    busqueda = f"%{termino}%"


    cursor.execute("""
        SELECT *
        FROM libros

        WHERE titulo LIKE ?

        OR autor LIKE ?

        OR categoria LIKE ?

        OR isbn LIKE ?

        ORDER BY titulo ASC

    """,
    (
        busqueda,
        busqueda,
        busqueda,
        busqueda
    ))


    libros = [
        dict(row)
        for row in cursor.fetchall()
    ]


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


    categorias = [
        row["categoria"]
        for row in cursor.fetchall()
    ]


    conn.close()


    return categorias