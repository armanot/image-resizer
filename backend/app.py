from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
PDF_OUTPUT = "output.pdf"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/upload", methods=["POST"])
def upload_image():
    file = request.files["file"]
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)

        # Resize image and save it back
        resized_path = os.path.join(app.config["UPLOAD_FOLDER"], f"resized-{filename}")
        with Image.open(file_path) as img:
            img = img.resize((800, 600), Image.LANCZOS)
            img.save(resized_path)

        # Generate a PDF
        pdf = canvas.Canvas(PDF_OUTPUT, pagesize=letter)
        pdf.drawImage(resized_path, 50, 500, width=400, height=300)
        pdf.save()

        return jsonify({"message": "File uploaded and processed successfully!", "fileUrl": resized_path})

    return jsonify({"error": "No file provided!"}), 400

if __name__ == "__main__":
    app.run(debug=True)
