from flask import Flask,request
import pdfplumber
app=Flask(__name__)


@app.route("/upload",methods=["POST"])
def upload():
    text=""
    file=request.files["file"]
    filename=file.filename
    if "file" not in request.files:
        return jsonify({"error": "Aucun fichier envoyé"}), 400
    if filename.endswith(".pdf"):
        text=""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text=page.extract_text()
                if page_text:
                    text+=page_text + "\n"
    elif filename.endswith(".txt"):
            text = file.read().decode("utf-8")
    else :
        return jsonify({"error": "Format non supporté (PDF ou TXT uniquement)"}), 400
    return jsonify({"filename": filename, "text_preview": text[:500]})

if __name__ == "__main__":
    app.run(debug=True, port=5000)