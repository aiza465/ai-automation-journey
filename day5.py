from groq import Groq
from dotenv import load_dotenv
import json
import csv

load_dotenv()

client = Groq()

# Read the CSV
with open("customer.csv") as f:
    reader = csv.DictReader(f)
    customers = list(reader)

results = []

for customer in customers:
    print(f"Processing {customer['name']}...")

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": """
            Analyze this customer message and reply in this exact JSON:
            {
                "category": "complaint/question/praise",
                "priority": "high/medium/low",
                "reply": "a short professional reply to the customer"
            }
            """},
            {"role": "user", "content": customer["message"]}
        ]
    )

    raw = response.choices[0].message.content
    data = json.loads(raw)

    results.append({
        "name": customer["name"],
        "message": customer["message"],
        "category": data["category"],
        "priority": data["priority"],
        "reply": data["reply"]
    })

# Save results to a new CSV
with open("results.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "message", "category", "priority", "reply"])
    writer.writeheader()
    writer.writerows(results)

print("\nDone! Check results.csv")



