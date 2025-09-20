import discord
from discord.ext import commands
from flask import Flask, request, jsonify
import threading
import os

# Cấu hình bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Cấu hình Flask
app = Flask(__name__)

# Channel ID để gửi thông báo
NOTIFY_CHANNEL_ID = "YOUR_CHANNEL_ID_HERE"  # Thay bằng ID channel Discord

# Khi bot sẵn sàng
@bot.event
async def on_ready():
    print(f'Bot đã sẵn sàng với tên: {bot.user.name}')
    channel = bot.get_channel(NOTIFY_CHANNEL_ID)
    if channel:
        await channel.send("Bot đã khởi động và sẵn sàng nhận thông báo từ ThingSpeak!")

# Endpoint webhook từ ThingSpeak
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if data and 'nhietdo' in data:
        nhietdo = float(data['nhietdo'])
        if nhietdo > 32:  # Ngưỡng nhiệt độ
            channel = bot.get_channel(NOTIFY_CHANNEL_ID)
            if channel:
                embed = discord.Embed(
                    title="Cảnh báo từ ThingSpeak!",
                    description=f"Nhiệt độ: {nhietdo}°C vượt ngưỡng!",
                    color=discord.Color.red()
                )
                bot.loop.create_task(channel.send(embed=embed))
    return jsonify({"status": "received"})

# Chạy bot và Flask
if __name__ == "__main__":
    bot_thread = threading.Thread(target=bot.run, args=("os.environ.get('DISCORD_TOKEN')",))
    bot_thread.start()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

