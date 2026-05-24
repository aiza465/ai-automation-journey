from groq import Groq
from dotenv import load_dotenv
load_dotenv()
client = Groq()

while True:
    user_input = input("You: ")

    if user_input=='quit':
        break

    response=client.chat.completions.create(
        model="llama-3.3-70b-versatile",
    messages=[
        {"role": "system", "content":"You are an assistant that only replies like a pirate."},
         {"role":"user","content":user_input}
    ]
    )

    reply = response.choices[0].message.content

    print(f"AI: {reply}\n")


