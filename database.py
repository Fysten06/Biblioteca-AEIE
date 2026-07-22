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



    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prestamos (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            libro_id INTEGER NOT NULL,

            nombre TEXT NOT NULL,

            cedula TEXT NOT NULL,

            carnet TEXT NOT NULL,

            telefono TEXT NOT NULL,

            fecha_solicitud TEXT DEFAULT (datetime('now','-6 hours')),

            fecha_aprobacion TEXT,

            fecha_devolucion TEXT NOT NULL,

            fecha_real_devolucion TEXT,

            estado TEXT DEFAULT 'Pendiente',

            FOREIGN KEY(libro_id)
            REFERENCES libros(id)

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





def crear_prestamo(
    libro_id,
    nombre,
    cedula,
    carnet,
    telefono,
    fecha_devolucion
):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute("""
        INSERT INTO prestamos
        (
            libro_id,
            nombre,
            cedula,
            carnet,
            telefono,
            fecha_devolucion
        )

        VALUES (?, ?, ?, ?, ?, ?)

    """,
    (
        libro_id,
        nombre,
        cedula,
        carnet,
        telefono,
        fecha_devolucion
    ))


    conn.commit()

    conn.close()





def obtener_prestamos():

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute("""
        SELECT

            prestamos.*,

            libros.titulo,
            libros.autor

        FROM prestamos

        INNER JOIN libros

        ON prestamos.libro_id = libros.id

        ORDER BY prestamos.fecha_solicitud DESC

    """)


    prestamos = [
        dict(row)
        for row in cursor.fetchall()
    ]


    conn.close()


    return prestamos





def obtener_historial():

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute("""
        SELECT

            prestamos.*,

            libros.titulo,
            libros.autor

        FROM prestamos

        INNER JOIN libros

        ON prestamos.libro_id = libros.id

        WHERE estado = 'Devuelto'

        OR estado = 'Rechazado'

        ORDER BY fecha_real_devolucion DESC

    """)


    historial = [
        dict(row)
        for row in cursor.fetchall()
    ]


    conn.close()


    return historial





def obtener_prestamo_por_id(id):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute("""
        SELECT *
        FROM prestamos
        WHERE id = ?
    """,
    (id,))


    prestamo = cursor.fetchone()


    conn.close()


    if prestamo:

        return dict(prestamo)


    return None





def aprobar_prestamo(id):

    conn = get_connection()

    cursor = conn.cursor()


    prestamo = obtener_prestamo_por_id(id)


    if prestamo:


        cursor.execute("""
            UPDATE prestamos

            SET

                estado = 'Aprobado',

                fecha_aprobacion =
                datetime('now','-6 hours')

            WHERE id = ?

        """,
        (id,))



        cursor.execute("""
            UPDATE libros

            SET disponibles = disponibles - 1

            WHERE id = ?

            AND disponibles > 0

        """,
        (prestamo["libro_id"],))



    conn.commit()

    conn.close()





def rechazar_prestamo(id):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute("""
        UPDATE prestamos

        SET estado = 'Rechazado'

        WHERE id = ?

    """,
    (id,))


    conn.commit()

    conn.close()





def devolver_libro(id):

    conn = get_connection()

    cursor = conn.cursor()


    prestamo = obtener_prestamo_por_id(id)


    if prestamo:


        cursor.execute("""
            UPDATE prestamos

            SET

                estado = 'Devuelto',

                fecha_real_devolucion =
                datetime('now','-6 hours')

            WHERE id = ?

        """,
        (id,))



        cursor.execute("""
            UPDATE libros

            SET disponibles = disponibles + 1

            WHERE id = ?

        """,
        (prestamo["libro_id"],))



    conn.commit()

    conn.close()





def actualizar_atrasados():

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute("""
        UPDATE prestamos

        SET estado = 'Atrasado'

        WHERE estado = 'Aprobado'

        AND fecha_devolucion < date('now','-6 hours')

    """)


    conn.commit()

    conn.close()


def eliminar_prestamo(id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM prestamos
        WHERE id = ?
    """,
    (id,))

    conn.commit()

    conn.close()

def obtener_prestamo_por_id(id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM prestamos
        WHERE id = ?
    """,
    (id,))


    prestamo = cursor.fetchone()

    conn.close()


    if prestamo:

        return dict(prestamo)


    return None

def actualizar_atrasados():

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute("""
        UPDATE prestamos

        SET estado = 'Atrasado'

        WHERE estado = 'Aprobado'

        AND fecha_devolucion < date('now','-6 hours')

    """)


    conn.commit()

    conn.close()


def obtener_estadisticas():

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute("""
        SELECT COUNT(*) 
        FROM libros
    """)

    total_libros = cursor.fetchone()[0]



    cursor.execute("""
        SELECT COUNT(*)
        FROM prestamos
        WHERE estado = 'Pendiente'
    """)

    pendientes = cursor.fetchone()[0]



    cursor.execute("""
        SELECT COUNT(*)
        FROM prestamos
        WHERE estado = 'Aprobado'
    """)

    activos = cursor.fetchone()[0]



    cursor.execute("""
        SELECT COUNT(*)
        FROM prestamos
        WHERE estado = 'Atrasado'
    """)

    atrasados = cursor.fetchone()[0]



    conn.close()



    return {
        "total_libros": total_libros,
        "pendientes": pendientes,
        "activos": activos,
        "atrasados": atrasados
    }



def obtener_estadisticas():

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute("""
        SELECT COUNT(*)
        FROM libros
    """)

    total_libros = cursor.fetchone()[0]



    cursor.execute("""
        SELECT SUM(disponibles)
        FROM libros
    """)

    disponibles = cursor.fetchone()[0]

    if disponibles is None:

        disponibles = 0



    cursor.execute("""
        SELECT COUNT(*)
        FROM prestamos
        WHERE estado = 'Pendiente'
    """)

    pendientes = cursor.fetchone()[0]



    cursor.execute("""
        SELECT COUNT(*)
        FROM prestamos
        WHERE estado = 'Aprobado'
    """)

    activos = cursor.fetchone()[0]



    cursor.execute("""
        SELECT COUNT(*)
        FROM prestamos
        WHERE estado = 'Atrasado'
    """)

    atrasados = cursor.fetchone()[0]



    cursor.execute("""
        SELECT COUNT(*)
        FROM prestamos
    """)

    total_prestamos = cursor.fetchone()[0]



    conn.close()


    return {

        "total_libros": total_libros,

        "disponibles": disponibles,

        "pendientes": pendientes,

        "activos": activos,

        "atrasados": atrasados,

        "total_prestamos": total_prestamos

    }





def obtener_ultimos_prestamos():

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute("""
        SELECT

            prestamos.id,

            prestamos.nombre,

            prestamos.estado,

            prestamos.fecha_solicitud,

            libros.titulo


        FROM prestamos


        INNER JOIN libros


        ON prestamos.libro_id = libros.id


        ORDER BY prestamos.id DESC


        LIMIT 5

    """)


    prestamos = [

        dict(row)

        for row in cursor.fetchall()

    ]


    conn.close()


    return prestamos





def obtener_libros_mas_solicitados():

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute("""
        SELECT

            libros.titulo,

            COUNT(prestamos.id) AS cantidad


        FROM libros


        LEFT JOIN prestamos


        ON libros.id = prestamos.libro_id


        GROUP BY libros.id


        ORDER BY cantidad DESC


        LIMIT 5

    """)


    libros = [

        dict(row)

        for row in cursor.fetchall()

    ]


    conn.close()


    return libros