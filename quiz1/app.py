import requests
import os
from dotenv import load_dotenv
from flask import Flask,request,jsonify,render_template
import pdfplumber
app=Flask(__name__)
import json

load_dotenv()
GROQ_API_KEY=os.getenv("GROQ_API_KEY")

@app.route("/")
def home():
    return render_template("index.html")

def genere_question(text):
    url="https://api.groq.com/openai/v1/chat/completions"

    headers={
        "Authorization":f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt=f""" Voici un texte : {text}

    Génère 7 questions à choix multiples (4 réponses chacune) basées sur ce texte.
    Réponds UNIQUEMENT en JSON, sans aucun texte avant ou après, dans ce format exact :
    {{"questions": [{{"question": "...", "choix": ["A", "B", "C", "D"], "reponse_correcte": "A"}}]}}
    """

    data={
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "response_format": {"type":"json_object"}
    }
    reponse=requests.post(url,headers=headers,json=data)
    resultat=reponse.json()
    contenu = resultat["choices"][0]["message"]["content"]
    quiz_json = json.loads(contenu)
    return quiz_json


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

    quiz=genere_question(text)
    return jsonify(quiz)

if __name__ == "__main__":
    app.run(debug=True, port=5000)