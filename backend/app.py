backend/app.py

from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, flash import os from werkzeug.utils import secure_filename

app = Flask(name) app.secret_key = os.environ.get("FLASK_SECRET_KEY", "default_secret")

Configuration

UPLOAD_FOLDER = os.path.join("static", "images") ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"} USERNAME = "abhisilks" PASSWORD = "asilk@7777"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

Ensure image folders exist

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

Check allowed file extensions

def allowed_file(filename): return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

Login page

@app.route("/login", methods=["GET", "POST"]) def login(): if request.method == "POST": user = request.form["username"] pwd = request.form["password"] if user == USERNAME and pwd == PASSWORD: session["admin"] = True return redirect(url_for("admin")) else: flash("Invalid credentials", "danger") return render_template("login.html")

Admin panel

@app.route("/admin", methods=["GET", "POST"]) def admin(): if not session.get("admin"): return redirect(url_for("login"))

categories = os.listdir(app.config["UPLOAD_FOLDER"])
images = {}
for cat in categories:
    cat_path = os.path.join(app.config["UPLOAD_FOLDER"], cat)
    if os.path.isdir(cat_path):
        images[cat] = os.listdir(cat_path)
return render_template("admin.html", images=images)

Upload endpoint

@app.route("/upload", methods=["POST"]) def upload(): if not session.get("admin"): return redirect(url_for("login"))

category = request.form["category"]
file = request.files["file"]

if file and allowed_file(file.filename):
    filename = secure_filename(file.filename)
    cat_path = os.path.join(app.config["UPLOAD_FOLDER"], category)
    os.makedirs(cat_path, exist_ok=True)
    file.save(os.path.join(cat_path, filename))
return redirect(url_for("admin"))

Delete endpoint

@app.route("/delete", methods=["POST"]) def delete(): if not session.get("admin"): return redirect(url_for("login"))

category = request.form["category"]
filename = request.form["filename"]
filepath = os.path.join(app.config["UPLOAD_FOLDER"], category, filename)
if os.path.exists(filepath):
    os.remove(filepath)
return redirect(url_for("admin"))

Logout

@app.route("/logout") def logout(): session.pop("admin", None) return redirect(url_for("login"))

Serve images

@app.route("/static/images/<category>/<filename>") def serve_image(category, filename): return send_from_directory(os.path.join(app.config["UPLOAD_FOLDER"], category), filename)

if name == "main": app.run(host="0.0.0.0", port=5000)


