import requests
from groq import Groq
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()
client=Groq()

url="https://news.ycombinator.com"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

headlines = []
for item in soup.select(".titleline a")[:10]:
    headlines.append(item.text)

print("Headlines found:")
for h in headlines:
    print("-", h)

ai_response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "system", "content": "You are a tech news analyst."},
        {"role": "user", "content": f"Here are today's top tech headlines: {headlines}. Which is most important and why? Also what are the top 3 trends you see?"}
    ]
)

print("\nAI Analysis:")
print(ai_response.choices[0].message.content)




