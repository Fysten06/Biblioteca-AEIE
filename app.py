from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import os

from database import (
    init_db,
    obtener_libros,
    buscar_libros,
    agregar_libro,
    eliminar_libro,
    obtener_libro_por_id,
    editar_libro
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



@app.route("/")
def inicio():

    return render_template(
        "index.html"
    )



@app.route("/publico")
def publico():

    termino = request.args.get("buscar")


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



@app.route("/admin", methods=["GET", "POST"])
def login_admin():

    if session.get("admin"):

        return redirect(
            url_for("panel_admin")
        )


    if request.method == "POST":

        password = request.form["password"]


        if password == os.getenv("ADMIN_PASSWORD"):

            session["admin"] = True


            return redirect(
                url_for("panel_admin")
            )


        return render_template(
            "login_admin.html",
            error="Contraseña incorrecta."
        )


    return render_template(
        "login_admin.html"
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


    eliminar_libro(
        id
    )


    return redirect(
        url_for("panel_admin")
    )



@app.route("/admin/editar/<int:id>", methods=["GET", "POST"])
def editar(id):

    if not session.get("admin"):

        return redirect(
            url_for("login_admin")
        )


    libro = obtener_libro_por_id(
        id
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


        disponibles = int(
            request.form["disponibles"]
        )


        if disponibles > cantidad:

            disponibles = cantidad


        if disponibles < 0:

            disponibles = 0



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



@app.route("/logout")
def logout():

    session.clear()


    return redirect(
        url_for("inicio")
    )



if __name__ == "__main__":

    app.run(
        debug=True
    )