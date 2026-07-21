from flask import Flask, render_template

# CREACIÓN DE LA APLICACIÓN

app = Flask(__name__)

# RUTAS

@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/admin")
def administrador():
    return render_template("admin.html")


@app.route("/publico")
def publico():
    return render_template("public.html")


# EJECUTAR SERVIDOR

if __name__ == "__main__":
    app.run(debug=True)