from flask import Flask, request, jsonify
import os
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# Configuration
app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
DEST_FOLDER = "resized"
PDF_FILE = "resized_images.pdf"
TARGET_WIDTH = 800
TARGET_HEIGHT = 600

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DEST_FOLDER, exist_ok=True)

@app.route("/resize", methods=["POST"])
def resize_images():
    uploaded_files = request.files.getlist("images")
    if not uploaded_files:
        return jsonify({"error": "No files provided"}), 400

    report = []
    pdf = canvas.Canvas(PDF_FILE, pagesize=letter)
    pdf.setTitle("Resized Images")

    for uploaded_file in uploaded_files:
        try:
            file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
            resized_path = os.path.join(DEST_FOLDER, uploaded_file.filename)
            uploaded_file.save(file_path)

            with Image.open(file_path) as img:
                img = img.resize((TARGET_WIDTH, TARGET_HEIGHT), Image.LANCZOS)
                img.save(resized_path)

            # Add resized image to PDF
            pdf.drawImage(resized_path, 50, 500, width=400, height=300)
            pdf.showPage()

            report.append({"file": uploaded_file.filename, "status": "resized"})
        except Exception as e:
            report.append({"file": uploaded_file.filename, "status": f"error: {str(e)}"})

    pdf.save()
    return jsonify({"message": "Resizing complete", "report": report})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
