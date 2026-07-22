from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import os
import re

from database import (
    init_db,
    obtener_libros,
    buscar_libros,
    agregar_libro,
    eliminar_libro,
    obtener_libro_por_id,
    editar_libro,
    crear_prestamo,
    obtener_prestamos,
    obtener_prestamo_por_id,
    aprobar_prestamo,
    rechazar_prestamo,
    devolver_libro,
    eliminar_prestamo,
    actualizar_atrasados,
    obtener_estadisticas,
    obtener_ultimos_prestamos,
    obtener_libros_mas_solicitados
)

load_dotenv()


app = Flask(__name__)


app.secret_key = os.getenv("SECRET_KEY")


UPLOAD_FOLDER = "static/uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg"
}


init_db()



def archivo_permitido(nombre):

    return "." in nombre and \
    nombre.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS



def validar_cedula(cedula):

    return bool(
        re.fullmatch(
            r"\d{9}",
            cedula
        )
    )



def validar_telefono(telefono):

    return bool(
        re.fullmatch(
            r"\d{8}",
            telefono
        )
    )



@app.route("/")
def inicio():

    return render_template(
        "index.html"
    )



@app.route("/publico")
def publico():

    termino = request.args.get(
        "buscar"
    )


    if termino:

        libros = buscar_libros(
            termino
        )

    else:

        libros = obtener_libros()


    return render_template(
        "public.html",
        libros=libros,
        buscar=termino
    )



@app.route("/solicitar/<int:id>", methods=["GET", "POST"])
def solicitar_prestamo(id):

    libro = obtener_libro_por_id(id)


    if not libro:

        return redirect(
            url_for("publico")
        )



    if request.method == "POST":


        nombre = request.form["nombre"].strip()

        cedula = request.form["cedula"].strip()

        carnet = request.form["carnet"].strip()

        telefono = request.form["telefono"].strip()

        fecha_devolucion = request.form["fecha_devolucion"]



        if not validar_cedula(cedula):

            return render_template(
                "solicitar_prestamo.html",
                libro=libro,
                error="La cédula debe tener 9 números sin guiones."
            )



        if not validar_telefono(telefono):

            return render_template(
                "solicitar_prestamo.html",
                libro=libro,
                error="El teléfono debe tener 8 números sin guiones."
            )



        crear_prestamo(
            id,
            nombre,
            cedula,
            carnet,
            telefono,
            fecha_devolucion
        )


        return redirect(
            url_for("publico")
        )


    return render_template(
        "solicitar_prestamo.html",
        libro=libro
    )



@app.route("/admin", methods=["GET", "POST"])
def login_admin():


    if session.get("admin"):

        return redirect(
            url_for("dashboard")
        )



    if request.method == "POST":


        password = request.form["password"]


        if password == os.getenv(
            "ADMIN_PASSWORD"
        ):

            session["admin"] = True


            return redirect(
                url_for("dashboard")
            )


        return render_template(
            "login_admin.html",
            error="Contraseña incorrecta."
        )



    return render_template(
        "login_admin.html"
    )



@app.route("/admin/dashboard")
def dashboard():

    if not session.get("admin"):

        return redirect(
            url_for("login_admin")
        )


    estadisticas = obtener_estadisticas()


    ultimos_prestamos = obtener_ultimos_prestamos()


    libros_populares = obtener_libros_mas_solicitados()



    return render_template(
        "dashboard.html",
        estadisticas=estadisticas,
        ultimos_prestamos=ultimos_prestamos,
        libros_populares=libros_populares
    )


@app.route("/admin/panel")
def panel_admin():


    if not session.get("admin"):

        return redirect(
            url_for("login_admin")
        )


    libros = obtener_libros()


    return render_template(
        "admin.html",
        libros=libros
    )



@app.route("/admin/agregar", methods=["GET", "POST"])
def agregar():


    if not session.get("admin"):

        return redirect(
            url_for("login_admin")
        )



    if request.method == "POST":


        titulo = request.form["titulo"]

        autor = request.form["autor"]

        editorial = request.form["editorial"]

        categoria = request.form["categoria"]

        anio = request.form["anio"]

        isbn = request.form["isbn"]

        descripcion = request.form["descripcion"]

        cantidad = int(
            request.form["cantidad"]
        )


        imagen = None


        archivo = request.files.get(
            "imagen"
        )


        if archivo and archivo_permitido(
            archivo.filename
        ):


            nombre = secure_filename(
                archivo.filename
            )


            ruta = os.path.join(
                app.config["UPLOAD_FOLDER"],
                nombre
            )


            archivo.save(
                ruta
            )


            imagen = ruta



        agregar_libro(
            titulo,
            autor,
            editorial,
            categoria,
            anio,
            isbn,
            descripcion,
            cantidad,
            imagen
        )


        return redirect(
            url_for("panel_admin")
        )


    return render_template(
        "add_book.html"
    )



@app.route("/admin/eliminar/<int:id>")
def eliminar(id):


    if not session.get("admin"):

        return redirect(
            url_for("login_admin")
        )


    eliminar_libro(id)


    return redirect(
        url_for("panel_admin")
    )



@app.route("/admin/editar/<int:id>", methods=["GET", "POST"])
def editar(id):


    if not session.get("admin"):

        return redirect(
            url_for("login_admin")
        )


    libro = obtener_libro_por_id(id)



    if request.method == "POST":


        titulo = request.form["titulo"]

        autor = request.form["autor"]

        editorial = request.form["editorial"]

        categoria = request.form["categoria"]

        anio = request.form["anio"]

        isbn = request.form["isbn"]

        descripcion = request.form["descripcion"]

        cantidad = int(
            request.form["cantidad"]
        )

        disponibles = int(
            request.form["disponibles"]
        )


        if disponibles > cantidad:

            disponibles = cantidad



        imagen = libro["imagen"]


        archivo = request.files.get(
            "imagen"
        )


        if archivo and archivo_permitido(
            archivo.filename
        ):


            nombre = secure_filename(
                archivo.filename
            )


            ruta = os.path.join(
                app.config["UPLOAD_FOLDER"],
                nombre
            )


            archivo.save(
                ruta
            )


            imagen = ruta



        editar_libro(
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
        )


        return redirect(
            url_for("panel_admin")
        )



    return render_template(
        "edit_book.html",
        libro=libro
    )



@app.route("/admin/prestamos")
def admin_prestamos():


    if not session.get("admin"):

        return redirect(
            url_for("login_admin")
        )


    actualizar_atrasados()


    prestamos = obtener_prestamos()


    return render_template(
        "admin_prestamos.html",
        prestamos=prestamos
    )


@app.route("/admin/prestamo/aprobar/<int:id>")
def aceptar_prestamo(id):


    if not session.get("admin"):

        return redirect(
            url_for("login_admin")
        )


    aprobar_prestamo(id)


    return redirect(
        url_for("admin_prestamos")
    )



@app.route("/admin/prestamo/rechazar/<int:id>")
def rechazar(id):


    if not session.get("admin"):

        return redirect(
            url_for("login_admin")
        )


    rechazar_prestamo(id)


    return redirect(
        url_for("admin_prestamos")
    )



@app.route("/admin/prestamo/devolver/<int:id>")
def devolver(id):


    if not session.get("admin"):

        return redirect(
            url_for("login_admin")
        )


    devolver_libro(id)


    return redirect(
        url_for("admin_prestamos")
    )


@app.route("/admin/prestamo/eliminar/<int:id>")
def eliminar_prestamo_admin(id):

    if not session.get("admin"):

        return redirect(
            url_for("login_admin")
        )


    prestamo = obtener_prestamo_por_id(id)


    if prestamo and prestamo["estado"] in ["Devuelto", "Rechazado"]:

        eliminar_prestamo(id)


    return redirect(
        url_for("admin_prestamos")
    )


@app.route("/logout")
def logout():

    session.clear()


    return redirect(
        url_for("inicio")
    )



if __name__ == "__main__":

    app.run()