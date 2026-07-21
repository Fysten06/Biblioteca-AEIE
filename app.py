from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
import os

from database import init_db

# Cargar variables del archivo .env
load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")

# Crear la base de datos si no existe
init_db()


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/publico")
def publico():
    return render_template("public.html")


@app.route("/admin", methods=["GET", "POST"])
def login_admin():

    if session.get("admin"):
        return render_template("admin.html")

    if request.method == "POST":

        password = request.form["password"]

        if password == os.getenv("ADMIN_PASSWORD"):

            session["admin"] = True

            return render_template("admin.html")

        else:

            return render_template(
                "login_admin.html",
                error="Contraseña incorrecta."
            )

    return render_template("login_admin.html")


@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("inicio"))


if __name__ == "__main__":
    app.run(debug=True)