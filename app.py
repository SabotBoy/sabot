from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from openai import OpenAI
from datetime import datetime

import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat_history.db'
db = SQLAlchemy(app)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))



class ChatLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(10))  # 'user' or 'bot'
    message = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message']
    
    # Save user message
    user_log = ChatLog(sender='user', message=user_input)
    db.session.add(user_log)

    messages = [
        {"role": "system", "content": "You are a helpful assistant for Andrew Henry’s customers."},
        {"role": "user", "content": user_input}
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    reply = response.choices[0].message.content.strip()
    
    # Save bot response
    bot_log = ChatLog(sender='bot', message=reply)
    db.session.add(bot_log)

    db.session.commit()

    return jsonify({"reply": reply})

@app.route('/history')
def history():
    logs = ChatLog.query.order_by(ChatLog.timestamp.asc()).all()
    return render_template('history.html', logs=logs)



#if __name__ == '__main__':
    #app.run(debug=True)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
