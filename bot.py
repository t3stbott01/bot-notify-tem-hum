import os
import discord
from discord.ext import commands
import asyncio
from flask import Flask, request
import threading

# ---- Config ----
DISCORD_CHANNEL_ID = 123456789012345678  # ID channel Discord
TOKEN = os.getenv("DISCORD_TOKEN")      # Lấy token từ biến môi trường

# ---- Discord Bot setup ----
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot đã đăng nhập: {bot.user}")

@bot.command()
async def hello(ctx):
    await ctx.send(f"Xin chào {ctx.author.mention} 👋!")

# ---- Flask app ----
app = Flask(__name__)

@app.route("/notify", methods=["POST"])
def notify():
    data = request.json
    print("📩 Nhận từ ThingSpeak:", data)

    temperature = data.get("field1")
    humidity = data.get("field2")

    channel = bot.get_channel(DISCORD_CHANNEL_ID)
    if channel:
        asyncio.run_coroutine_threadsafe(
            channel.send(f"⚡ Cảnh báo! 🌡 {temperature}°C - 💧 {humidity}%"),
            bot.loop
        )
    return {"status": "ok"}, 200

# ---- Chạy Flask song song với bot ----
def run_flask():
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))

threading.Thread(target=run_flask).start()

# ---- Run Discord bot ----
if __name__ == "__main__":
    if not TOKEN:
        print("❌ Chưa có DISCORD_TOKEN trong Environment Variable!")
    else:
        bot.run(TOKEN)
