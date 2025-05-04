from flask import Flask, request, jsonify, Response
import os
import openai

app = Flask(__name__)

# Lấy GPT API key từ biến môi trường
openai.api_key = os.getenv("OPENAI_API_KEY")

# Trang chủ kiểm tra server
@app.route("/", methods=["GET"])
def home():
    return "Kirin AI Server is running!", 200

# Route mặc định để xác thực domain Zalo
@app.route("/verify-domain", methods=["GET"])
def verify_domain():
    return Response(
        "zalo-platform-site-verification=Ujs1DQBHEYjWyQ0Lcyy1DKEzgMk1otysDZ8q",
        mimetype="text/plain"
    )

# Route bổ sung nếu /verify-domain không xác thực được
@app.route("/zalo-verify", methods=["GET"])
def zalo_verify():
    return Response(
        "zalo-platform-site-verification=Ujs1DQBHEYjWyQ0Lcyy1DKEzgMk1otysDZ8q",
        mimetype="text/plain"
    )

# Webhook xử lý tin nhắn Zalo
@app.route("/webhook", methods=["POST"])
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
