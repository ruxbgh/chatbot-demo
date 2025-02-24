from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import openai
import os  # Permite folosirea variabilelor de mediu pentru siguranță

app = Flask(__name__, static_folder="static")
CORS(app)  # Activează CORS pentru toate cererile

# Încarcă API Key din variabila de mediu (Asigură-te că ai setat-o)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET"])
def home():
    """Returnează interfața frontend (index.html)"""
    return send_from_directory("static", "index.html")

def chatbot_response(user_input):
    """Funcția care interoghează OpenAI"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ești un chatbot pentru un restaurant."},
                {"role": "user", "content": user_input}
            ]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Eroare la interogarea OpenAI: {str(e)}"

@app.route("/chat", methods=["POST"])
def chat():
    """API endpoint pentru a primi mesaje de la utilizator și a răspunde"""
    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"response": "Mesajul nu poate fi gol."})

    response = chatbot_response(user_message)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
