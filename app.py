from flask import Flask, request, jsonify, Response
import openai
import os

app = Flask(__name__)

# Lấy OpenAI API key từ biến môi trường
openai.api_key = os.getenv("OPENAI_API_KEY")

# Webhook để nhận tin nhắn từ Zalo
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

# Route kiểm tra server
@app.route('/', methods=['GET'])
def index():
    return "Kirin AI Server đang hoạt động!", 200

# Route xác thực domain Zalo (trả về đúng định dạng text/plain)
@app.route('/verify-domain', methods=['GET'])
def verify_domain():
    return Response(
        "zalo-platform-site-verification=Ujs1DQBHEYjWyQ0Lcyy1DKEzgMk1otysDZ8q",
        status=200,
        mimetype='text/plain'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
