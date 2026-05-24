#saving chat in memory.json
from groq import Groq
from dotenv import load_dotenv
import json
import os

load_dotenv()

client = Groq()

# Load history from file if it exists, otherwise start fresh
if os.path.exists("memory.json"):
    with open("memory.json") as f:
        history = json.load(f)
    print("Welcome back! I remember our last conversation.\n")
else:
    history = []
    print("Chatbot ready!\n")

while True:
    user_input = input("You: ")

    if user_input == "quit":
        # Save history before exiting
        with open("memory.json", "w") as f:
            json.dump(history, f)
        print("Memory saved. Bye!")
        break

    history.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=history
    )

    reply = response.choices[0].message.content
    history.append({"role": "assistant", "content": reply})

    print(f"AI: {reply}\n")