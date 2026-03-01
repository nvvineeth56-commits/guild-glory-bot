import discord
from discord.ext import commands
import os
import sqlite3

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Database setup
conn = sqlite3.connect("glory.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS glory (
    user_id TEXT PRIMARY KEY,
    points INTEGER
)
""")
conn.commit()

@bot.event
async def on_ready():
    print(f"{bot.user} is online!")

@bot.command()
@commands.has_permissions(administrator=True)
async def add(ctx, member: discord.Member, points: int):
    cursor.execute("SELECT points FROM glory WHERE user_id = ?", (str(member.id),))
    result = cursor.fetchone()

    if result:
        new_points = result[0] + points
        cursor.execute("UPDATE glory SET points = ? WHERE user_id = ?", (new_points, str(member.id)))
    else:
        new_points = points
        cursor.execute("INSERT INTO glory (user_id, points) VALUES (?, ?)", (str(member.id), points))

    conn.commit()
    await ctx.send(f"🔥 {member.mention} now has {new_points} glory points!")

@bot.command()
async def leaderboard(ctx):
    cursor.execute("SELECT user_id, points FROM glory ORDER BY points DESC")
    rows = cursor.fetchall()

    if not rows:
        await ctx.send("No glory data yet.")
        return

    message = "🏆 **Guild Glory Leaderboard** 🏆\n"
    for i, (user_id, points) in enumerate(rows[:10], start=1):
        user = await bot.fetch_user(int(user_id))
        message += f"{i}. {user.name} — {points} points\n"

    await ctx.send(message)

bot.run(os.getenv("TOKEN"))
