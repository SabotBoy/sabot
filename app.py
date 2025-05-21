from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from openai import OpenAI
from datetime import datetime
from calendar_utils import create_event

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
#from flask import Flask, render_template, request, jsonify
# openai import OpenAI
#from datetime import datetime, timedelta
#from calendar_utils import create_event

# ... your app setup code

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message']

    # 🔍 Check if user is requesting a booking (simple logic for now)
    if "book" in user_input.lower() and "meeting" in user_input.lower():
        # Just a test — book a meeting for tomorrow at 10am
        start_time = datetime.now() + timedelta(days=1)
        start_time = start_time.replace(hour=10, minute=0, second=0, microsecond=0)
        end_time = start_time + timedelta(hours=1)

        event_link = create_event("Meeting with Andrew", start_time, end_time)

        return jsonify({"reply": f"I've booked your meeting for tomorrow at 10AM. Here’s your calendar link: {event_link}"})

    # (Fallback) Continue to GPT as usual
    # Send to GPT if no match
    messages = [
        {"role": "system", "content": "You are a helpful assistant for Andrew Henry’s clients."},
        {"role": "user", "content": user_input}
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    reply = response.choices[0].message.content.strip()
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
