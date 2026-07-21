from flask import Flask, render_template, request, jsonify, session
from database.database import init_db, buscar_libros, obtener_categorias

app = Flask(__name__)
app.secret_key = "aeie-biblioteca-secret"

init_db()


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/admin", methods=["GET", "POST"])
def administrador():
    contraseña_correcta = "admin123"

    if request.method == "POST":
        contraseña = request.form["password"]
        if contraseña == contraseña_correcta:
            session["admin"] = True
            return render_template("admin.html")
        else:
            return render_template("login_admin.html", error="Contraseña incorrecta")

    return render_template("login_admin.html")


@app.route("/publico")
def publico():
    categorias = obtener_categorias()
    return render_template("public.html", categorias=categorias)


@app.route("/buscar")
def buscar():
    termino = request.args.get("q", "").strip()
    categoria = request.args.get("categoria")
    disponibilidad = request.args.get("disponible")
    orden = request.args.get("orden")

    if disponibilidad == "disponible":
        disp = True
    elif disponibilidad == "agotado":
        disp = False
    else:
        disp = None

    if not termino and not categoria:
        return render_template("public.html",
                            resultados=None,
                            categorias=obtener_categorias())

    resultados = buscar_libros(termino, categoria, disp, orden)
    return render_template("public.html",
                         resultados=resultados,
                         categorias=obtener_categorias(),
                         termino=termino)


@app.route("/api/buscar")
def api_buscar():
    termino = request.args.get("q", "").strip()
    categoria = request.args.get("categoria")
    orden = request.args.get("orden")

    if not termino:
        return jsonify([])

    resultados = buscar_libros(termino, categoria if categoria else None, None, orden)
    return jsonify(resultados)


@app.route("/api/categorias")
def api_categorias():
    return jsonify(obtener_categorias())


@app.route("/logout")
def logout():
    session.pop("admin", None)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
