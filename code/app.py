from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import requests
import os
import json

# changes needed here
UPLOAD_FOLDER = 'static/uploads/'

app = Flask(__name__)
app.secret_key = "secretkeysomething"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def save_file(file):
    # file = request.files["file"]
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
    return True

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html", fruit_name="", fruit_disease="", disease_description="", fruit_image="")
    elif request.method == "POST":
        fileUpload = save_file(request.files["file"])

        # posting the picture and getting the fruit_disease and detection
        response = requests.post("http://127.0.0.1:5000/model", files={"file": open(UPLOAD_FOLDER+request.files["file"].filename, "rb")})
        response = response.json()

        fruit_name = response["disease"].split('_')[0]
        fruit_disease = response["disease"]
        disease_description = response["description"]
        return render_template("index.html", fruit_name=fruit_name, fruit_disease=fruit_disease, disease_description=disease_description, fruit_image=request.files["file"].filename)

if __name__ == "__main__":
    app.run(debug=True, port=8080)