from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq()

message = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", "content": "Say hello and tell me one fun fact about AI."}
    ]
)

response=message.choices[0].message.content

with open("output.txt",'w') as file:
    file.write(response)

print("done")
