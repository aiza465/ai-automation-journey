import discord
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq()
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

history = {}

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    user_id = message.author.id

    if user_id not in history:
        history[user_id] = [{"role": "system", "content": "You are a helpful assistant."}]

    history[user_id].append({"role": "user", "content": message.content})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=history[user_id]
    )

    reply = response.choices[0].message.content
    history[user_id].append({"role": "assistant", "content": reply})

    await message.channel.send(reply)

bot.run(os.getenv("DISCORD_BOT_TOKEN"))