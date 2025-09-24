from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__, static_folder="static", static_url_path="")
CORS(app)

client = OpenAI(api_key="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")

chats = {}

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/new_chat", methods=["POST"])
def new_chat():
    data = request.json
    name = data.get("name", "Новый чат")
    chat_id = str(len(chats) + 1)
    chats[chat_id] = {"name": name, "messages": []}
    return jsonify({"chat_id": chat_id, "name": name})

@app.route("/rename_chat/<chat_id>", methods=["POST"])
def rename_chat(chat_id):
    data = request.json
    new_name = data.get("name", "Без названия")
    if chat_id in chats:
        chats[chat_id]["name"] = new_name
    return jsonify({"chat_id": chat_id, "name": new_name})

@app.route("/get_chats")
def get_chats():
    return jsonify(chats)

@app.route("/send_message/<chat_id>", methods=["POST"])
def send_message(chat_id):
    data = request.json
    user_msg = data.get("message", "")
    if chat_id not in chats:
        return jsonify({"error": "chat not found"}), 404

    chats[chat_id]["messages"].append({"role": "user", "content": user_msg})

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "Ты — ALit, отвечай кратко."}]
                     + chats[chat_id]["messages"]
        )
        answer = resp.choices[0].message.content.strip()
    except Exception as e:
        answer = f"Ошибка: {e}"

    chats[chat_id]["messages"].append({"role": "assistant", "content": answer})

    return jsonify({"reply": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=14579)
