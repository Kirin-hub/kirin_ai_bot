from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    message = data.get("message", "")

    if "kirin ai" in message.lower():
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message}]
        )
        reply = response.choices[0].message.content
        return jsonify({"reply": reply})

    return jsonify({"message": "Không nhắc đến Kirin AI, không phản hồi."})


@app.route('/', methods=['GET'])
def index():
    return "Kirin AI Server đang hoạt động!", 200


@app.route('/verify-domain', methods=['GET'])
def verify_domain():
    return "zalo-platform-site-verification=Ujs1DQBHEYjWQ0LcyyIDKEzgMk1otysDZ8q", 200


if __name__ == '__main__':
    app.run()
