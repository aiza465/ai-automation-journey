from groq import Groq
from dotenv import load_dotenv
import json
load_dotenv()
client = Groq()
history = []
system_prompt="""
You are an assistant that analyzes any message the user sends.
Always reply in this exact JSON format, nothing else:
{
    "reply": "your normal reply here",
    "mood": "happy/sad/angry/neutral",
    "topic": "what the message is about in one word"
}
"""
history.append({"role": "system", "content": system_prompt})
while True:
    user_input=input("you: ")
    if user_input=='quit':
        break

    history.append({"role": "user", "content": user_input})
    response=client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=history
    )
    raw = response.choices[0].message.content
    data = json.loads(raw)

    history.append({"role": "assistant", "content": raw})

    print(f"AI: {data['reply']}")
    print(f"Your mood: {data['mood']}")
    print(f"Topic: {data['topic']}\n")