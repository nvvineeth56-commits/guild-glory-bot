import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} is online!")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong! 🏓")
import os
bot.run(os.getenv("TOKEN"))
