from flask import Flask, request, jsonify
import openai
import os  # Permite folosirea variabilelor de mediu pentru siguranță

app = Flask(__name__)

# Încarcă API Key din variabila de mediu (Mai sigur decât să o pui în cod!)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET"])
def home():
    return "Chatbotul este activ! Trimite o cerere POST la /chat."


def chatbot_response(user_input):
    try:
        client = openai.OpenAI()  # Inițializare client OpenAI

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ești un chatbot pentru un restaurant."},
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Eroare la interogarea OpenAI: {str(e)}"


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    response = chatbot_response(user_message)  # APELARE CORECTĂ A AI-ULUI
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
