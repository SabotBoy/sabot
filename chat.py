import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
# Replace with your real key

def chat():
    print("🤖 ChatGPT: Hello! I'm your assistant. Ask me anything. (Type 'exit' to quit)")
    
    messages = [
        {"role": "system", "content": "You are a helpful and friendly chatbot created to assist Andrew Henry with business ideas and automation."}
    ]

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("🤖 ChatGPT: See you next time, Andrew!")
            break

        messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        reply = response.choices[0].message.content.strip()
        messages.append({"role": "assistant", "content": reply})
        print("🤖 ChatGPT:", reply)

chat()
