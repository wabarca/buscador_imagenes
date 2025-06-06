from flask import Flask, render_template, request, jsonify, send_from_directory, send_file
import os
from datetime import datetime
import io
import zipfile

app = Flask(__name__)
BASE_DIR = "/DATA/geonetcast/Output"

@app.route("/")
def index():
    satelites = sorted(os.listdir(BASE_DIR))
    return render_template("index.html", satelites=satelites, productos=[], imagenes=[])

@app.route("/productos")
def productos():
    sat = request.args.get("satelite")
    sat_path = os.path.join(BASE_DIR, sat)
    if not os.path.isdir(sat_path):
        return jsonify([])

    try:
        productos = sorted([d for d in os.listdir(sat_path) if os.path.isdir(os.path.join(sat_path, d))])
    except Exception:
        productos = []

    return jsonify(productos)

@app.route("/buscar", methods=["POST"])
def buscar():
    satelite = request.form["satelite"]
    producto = request.form.get("producto", "")
    fecha_inicio = request.form["fecha_inicio"]
    fecha_fin = request.form["fecha_fin"]
    hora_inicio = request.form.get("hora_inicio", "")
    hora_fin = request.form.get("hora_fin", "")

    path_base = os.path.join(BASE_DIR, satelite)
    productos = sorted([d for d in os.listdir(path_base) if os.path.isdir(os.path.join(path_base, d))])

    imagenes = []

    for prod in productos:
        if producto and prod != producto:
            continue

        prod_path = os.path.join(path_base, prod)

        if not os.path.isdir(prod_path):
            continue

        for archivo in os.listdir(prod_path):
            if archivo.endswith(".webp"):
                try:
                    timestamp = archivo.split("_")[-1].replace(".webp", "")
                    try:
                        dt = datetime.strptime(timestamp, "%Y%m%d%H%M")
                    except ValueError:
                        dt = datetime.strptime(timestamp, "%Y%m%d%H%M%S")

                    dt_str = dt.strftime("%Y-%m-%d")
                    if dt_str < fecha_inicio or dt_str > fecha_fin:
                        continue

                    if hora_inicio and dt.strftime("%H:%M") < hora_inicio:
                        continue
                    if hora_fin and dt.strftime("%H:%M") > hora_fin:
                        continue

                    rel_path = os.path.join(satelite, prod, archivo)
                    imagenes.append({
                        "ruta": rel_path.replace("\\", "/"),
                        "fecha": dt.strftime("%d/%m/%Y %H:%M")
                    })
                except Exception:
                    continue

    imagenes.sort(key=lambda x: datetime.strptime(x["fecha"], "%d/%m/%Y %H:%M"))

    return render_template("index.html",
                           satelites=sorted(os.listdir(BASE_DIR)),
                           productos=productos,
                           selected_satelite=satelite,
                           selected_producto=producto,
                           fecha_inicio=fecha_inicio,
                           fecha_fin=fecha_fin,
                           hora_inicio=hora_inicio,
                           hora_fin=hora_fin,
                           imagenes=imagenes)

@app.route("/Output/<path:filename>")
def output_file(filename):
    return send_from_directory(BASE_DIR, filename)

@app.route("/descargar_zip", methods=["POST"])
def descargar_zip():
    imagenes = request.json.get("imagenes", [])
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for img in imagenes:
            ruta = os.path.join(BASE_DIR, img["ruta"])
            if os.path.isfile(ruta):
                arcname = os.path.basename(ruta)
                zip_file.write(ruta, arcname=arcname)

    zip_buffer.seek(0)
    return send_file(zip_buffer, mimetype="application/zip", as_attachment=True, download_name="imagenes.zip")

if __name__ == "__main__":
    app.run(debug=True)
