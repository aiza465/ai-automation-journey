from groq import Groq
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from datetime import date

load_dotenv()

client = Groq()

# Read your interests
with open("interests.txt") as f:
    interests = f.read()

# Scrape headlines
url = "https://news.ycombinator.com"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
headlines = [item.text for item in soup.select(".titleline a")[:5]]

# Send to AI
ai_response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "system", "content": "You are a personal briefing assistant. Be concise."},
        {"role": "user", "content": f"""
        My interests: {interests}

        Today's headlines: {headlines}

        Pick the most relevant headline for me and write a 3 sentence briefing about why it matters to me personally.
        """}
    ]
)

briefing = ai_response.choices[0].message.content

# Save to dated file
filename = f"briefing_{date.today()}.txt"
with open(filename, "w") as f:
    f.write(f"Daily Briefing — {date.today()}\n\n")
    f.write(f"Headlines analyzed: {len(headlines)}\n\n")
    f.write(briefing)

print(f"Briefing saved to {filename}")
print("\n" + briefing)