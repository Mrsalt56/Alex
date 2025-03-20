import discord
from discord.ext import commands, tasks 
import os
import asyncio
from itertools import cycle
import logging
import sqlite3
from dotenv import load_dotenv

load_dotenv(".env")
TOKEN: str = os.getenv("TOKEN")


intents = discord.Intents.default()
intents.message_content = True 
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True

logging.basicConfig(level=logging.INFO)

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

bot_statuses = cycle(["Seige", "Hello from Mrsalt56", "Status Code 123", "Minecraft"])

@tasks.loop(seconds=120)
async def change_bot_status():
    await bot.change_presence(activity=discord.Game(next(bot_statuses)))

@bot.event
async def on_ready():
    print("Bot ready!")
    change_bot_status.start()
    try:
        synced_commands = await bot.tree.sync()
        print(f"Synced {len(synced_commands)} commands.")
    except Exception as e:
        print("An error with syncing application commands has occurred: ", e)
            
@bot.event
async def on_guild_join(guild):
    conn = sqlite3.connect("cogs/main.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Guilds (guild_id) VALUES (?)", (guild.id,))
    conn.commit()
    conn.close()
    
@bot.event
async def on_guild_remove(guild):
    conn = sqlite3.connect("cogs/main.db")
    cursor = conn.cursor()
    cursor.execute("DELETE * FROM Guilds WHERE guild_id = ?", (guild.id,))
    conn.commit()
    conn.close()

async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            
class MyModal(discord.ui.Modal, title="Report User"):
    user_id = discord.ui.TextInput(label="User ID", style=discord.TextStyle.short, placeholder="Enter User ID (ex: 89237482374834)")
    reason = discord.ui.TextInput(label="Reason", style=discord.TextStyle.paragraph, placeholder="Enter the reason for the report")

    async def on_submit(self, interaction: discord.Interaction):
        if len(str(self.user_id)) > 15:
            await interaction.response.send_message("User ID is invalid", ephemeral=True)
            return

        await interaction.response.send_message(
            f"Thank you for reporting {self.user_id} for {self.reason}!", ephemeral=True)
        
        reports_channel = discord.utils.get(interaction.guild.channels, name="reports")
        
        if reports_channel:
            await reports_channel.send(f"User {self.user_id} has been reported for: {self.reason}")
        else:
            await interaction.followup.send("Reports channel not found.", ephemeral=True)

@bot.tree.command(name="report", description="Report a user for a specific reason.")
async def report(interaction: discord.Interaction):
    modal = MyModal()
    await interaction.response.send_modal(modal)

async def main():
    async with bot:
        await load()
        await bot.start(TOKEN)

asyncio.run(main())
