from groq import Groq
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests
load_dotenv()
client=Groq()

def give(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for tag in soup(['script', 'style']):
        tag.decompose()
    text=soup.get_text()
    lines=[]
    for line in text.splitlines():
        if line.strip()!='':
            lines.append(line)
    return '\n'.join(lines)[:5000]

url=input("Enter url: ")
ai_input=give(url)
history=[{"role": "system", "content": f"""You are a helpful assistant that responses from the {ai_input} if it doesnt exist in this just say it doesnt exist"""}]

while True:
    question=input("Enter your question: ")
    if question=="quit":
        break
    history.append({"role": "user", "content": question})
    response = client.chat.completions.create(
        model='llama-3.1-8b-instant',
        messages=history
    )
    reply=response.choices[0].message.content
    history.append({"role": "assistant", "content": reply})
    print(f"AI: {reply}\n")



