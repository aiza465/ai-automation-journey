# import discord
# from groq import Groq
# from dotenv import load_dotenv
# import os
# import json
# import asyncio
# import csv
#
# load_dotenv()
#
# client = Groq()
# intents = discord.Intents.default()
# intents.message_content = True
# bot = discord.Client(intents=intents)
#
# def result(message):
#         response = client.chat.completions.create(
#         model="llama-3.3-70b-versatile",
#         messages=[
#             {"role": "system", "content": """
#             Analyze this customer message and reply in this exact JSON:
#             {
#                 "category": "complaint/question/praise",
#                 "priority": "high/medium/low",
#                 "reply": "a short professional reply to the customer"
#             }
#             """},
#             {"role": "user", "content":message}
#         ]
#     )
#         return json.loads(response.choices[0].message.content)
#
# @bot.event
# async def on_ready():
#     print(f'logged in as {bot.user}')
#     channel= bot.get_channel(int(os.getenv("DISCORD_CHANNEL_ID")))
#
#     with open("customer.csv") as f:
#         reader = csv.DictReader(f)
#         customers=list(reader)
#     high_prio=[]
#     for customer in customers:
#         reply=result(customer['message'])
#         if reply['priority']=='high':
#             high_prio.append(customer['name'])
#             await channel.send(
#                 f"customer name: {customer['name']}\n"
#                 f"customer category: {reply['category']}\n"
#                 f"customer priority: {reply['priority']}\n"
#                 f"ai reply: {reply['reply']}"
#             )
#     await channel.send(
#         f"Analysis complete! High priority customers: {', '.join(high_prio) if high_prio else 'None'}")
#
#     await bot.close()
#
#
# bot.run(os.getenv("DISCORD_BOT_TOKEN"))
#=--------------------------------------------------------------------------
import discord
from groq import Groq
from dotenv import load_dotenv
import os
import json
import csv

load_dotenv()

client = Groq()
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

def analyze(message):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": """
            Analyze this customer message and reply in this exact JSON:
            {
                "category": "complaint/question/praise",
                "priority": "high/medium/low",
                "reply": "a short professional reply"
            }
            """},
            {"role": "user", "content": message}
        ]
    )
    return json.loads(response.choices[0].message.content)

@bot.event
async def on_ready():
    print(f"Bot online as {bot.user}")
    channel = bot.get_channel(int(os.getenv("DISCORD_CHANNEL_ID")))

    with open("customers.csv") as f:
        reader = csv.DictReader(f)
        customers = list(reader)

    await channel.send("🔍 Analyzing customers...")

    all_results = []
    high_prio = []

    for customer in customers:
        result = analyze(customer["message"])

        all_results.append({
            "name": customer["name"],
            "message": customer["message"],
            "category": result["category"],
            "priority": result["priority"],
            "reply": result["reply"]
        })

        if result["priority"] == "high":
            high_prio.append(customer["name"])
            await channel.send(
                f"🚨 **HIGH PRIORITY — {customer['name']}**\n"
                f"Message: {customer['message']}\n"
                f"Category: {result['category']}\n"
                f"Suggested Reply: {result['reply']}\n"
            )

    # Save everything to CSV
    with open("results.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "message", "category", "priority", "reply"])
        writer.writeheader()
        writer.writerows(all_results)

    await channel.send(
        f"✅ Done! {len(customers)} customers analyzed.\n"
        f"High priority: {', '.join(high_prio) if high_prio else 'None'}\n"
        f"Full report saved to results.csv"
    )

    await bot.close()

bot.run(os.getenv("DISCORD_BOT_TOKEN"))