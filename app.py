from flask import Flask, render_template, request

# CREACIÓN DE LA APLICACIÓN

app = Flask(__name__)

# RUTAS

@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/admin", methods=["GET", "POST"])
def administrador():

    contraseña_correcta = "admin123"

    if request.method == "POST":

        contraseña = request.form["password"]

        if contraseña == contraseña_correcta:
            return render_template("admin.html")

        else:
            return render_template(
                "login_admin.html",
                error="Contraseña incorrecta"
            )

    return render_template("login_admin.html")


@app.route("/publico")
def publico():
    return render_template("public.html")


# EJECUTAR SERVIDOR

if __name__ == "__main__":
    app.run(debug=True)