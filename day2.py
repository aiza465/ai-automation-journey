from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq()

history = []

print("Chatbot ready! Type 'quit' to exit\n")

while True:
    user_input = input("You: ")

    if user_input == 'quit':
        break

    history.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=history
    )

    reply = response.choices[0].message.content
    history.append({"role": "assistant", "content": reply})

    print(f"AI: {reply}\n")
    #------------------------------------
    from groq import Groq
    from dotenv import load_dotenv
    import json

    load_dotenv()

    client = Groq()

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are an assistant that only replies in JSON format. No extra text."},
            {"role": "user", "content": "Give me 3 programming tips. Return as JSON with a 'tips' list."}
        ]
    )

    raw = response.choices[0].message.content
    data = json.loads(raw)

    for tip in data["tips"]:
        print("-", tip)